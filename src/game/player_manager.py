# This will be for camera, and game logic
# So for how accuracy is calculated, settings, camera lock, spin, etc.

import pyray as rl
import math
import globals

player_settings = globals.settings.player_settings

class PlayerManager:
    def __init__(self):
        self.camera = rl.Camera3D()

        self.camera.position = [0.0, 0.0, 7.5]
        self.camera.target = [0.0, 0.0, 0.0]
        self.camera.up = [0.0, 1.0, 0.0]
        self.camera.fovy = 70
        self.camera.projection = 0

        self.parallax = player_settings.parallax
        self.sensitivity = math.radians(player_settings.sensitivity)

        self.spin: bool = player_settings.spin

        self.cursor_texture = rl.load_texture("assets/images/cursor.png")
        self.cursor_plane = rl.load_model_from_mesh(rl.gen_mesh_plane(0.525,0.525,1,1))
        self.cursor_plane.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.cursor_texture
        self.transform = rl.matrix_rotate_x(math.radians(90))
        self.cursor_plane.transform = self.transform
        
        self.cursor_position = rl.Vector2()
        self.clamped_cursor_position = rl.Vector2()

        if player_settings.absolute_mode:
            # Hidden Cursor
            rl.hide_cursor()
        else:
            # Captured Cursor
            rl.disable_cursor()

    # Input Update
    def update(self):

        # Input/Cursor Movement Logic

        relative = rl.Vector2(rl.get_mouse_delta().x, rl.get_mouse_delta().y)
        window_size: rl.Vector2 = rl.Vector2(rl.get_screen_width(), rl.get_screen_height())

        if player_settings.absolute_mode:
            position: rl.Vector2 = rl.get_mouse_position()
            center: rl.Vector2 = rl.Vector2(window_size.x / 2, window_size.y / 2)
            relative = rl.vector2_subtract(position, center)
            self.camera.target = rl.vector3_zero()
            self.cursor_position = rl.vector2_zero()
        
        motion = rl.vector2_scale(rl.Vector2(relative.x, -relative.y), self.sensitivity)

        if self.spin == True:
            self.update_spin(motion)
        else:
            self.update_lock(motion)
            
        # Parallax Calculation (Direct translation of kermeet's math, thank you)
        self.clamped_cursor_position = rl.Vector2(
            self.clamp(self.cursor_position.x, -2.7375, 2.7375),
            self.clamp(self.cursor_position.y, -2.7375, 2.7375)
        )
        pivot = rl.Vector3(0.0, 0.0, 7.0)

        # Simulation of Godot's Basis.Z
        look = rl.vector3_subtract(self.camera.target, self.camera.position)

        self.camera.position = rl.vector3_add(pivot, rl.Vector3(
            (self.clamped_cursor_position.x * self.parallax / 4),
            (self.clamped_cursor_position.y * self.parallax / 4),
            0
        ))
        # End of Parallax Calculation

        if player_settings.cursor_drift:
            self.cursor_position = self.clamped_cursor_position
        
        if not self.spin:
            self.camera.target = rl.Vector3(self.camera.position.x, self.camera.position.y, 0)


    # Draw Update (for cursor textures n such)

    def draw(self):
        rl.draw_model(self.cursor_plane, [self.clamped_cursor_position.x, self.clamped_cursor_position.y, 0.0], 1.0, rl.WHITE)

        if self.cursor_position.x != self.clamped_cursor_position.x or self.cursor_position.y != self.clamped_cursor_position.y:
            if player_settings.buffer_cursor_fade_distance != 0.0:
                over_clamp_pos: rl.Vector2 = rl.Vector2(
                    max(0.0, abs(self.cursor_position.x) - 2.7375),
                    max(0.0, abs(self.cursor_position.y) - 2.7375)
                )

                over_clamp = max(over_clamp_pos.x, over_clamp_pos.y)

                alpha = min(over_clamp / player_settings.buffer_cursor_fade_distance, 1)

                ghost_cursor_color = rl.Color(255,255,255, int(alpha * 255))

                # ghost_cursor_color.a = self.range_normalized(abs_distance, 2.7375, 2.7375 + abs(player_settings.buffer_cursor_fade_distance))
                rl.draw_model(self.cursor_plane, [self.cursor_position.x, self.cursor_position.y, 0.0], 1.0, ghost_cursor_color)
            else:
                print("not drawing")
                rl.draw_model(self.cursor_plane, [self.cursor_position.x, self.cursor_position.y, 0.0], 1.0, rl.WHITE)

    # Input Handling

    def update_spin(self, motion: rl.Vector2):

        # for now, this shall be the solution for low FPS spazzes
        self.cursor_position = rl.vector2_add(self.cursor_position, motion)
        self.camera.target = rl.Vector3(self.cursor_position.x, self.cursor_position.y, 0)

        # rl.update_camera_pro(self.camera, [0,0,0], [motion.x * 7.5, -motion.y * 7.5, 0.0], 0.0)

        # look = rl.vector3_subtract(self.camera.target, self.camera.position)

        # look_vector2 = rl.Vector2(look.x, look.y)
        # camera_vector2 = rl.Vector2(self.camera.position.x, self.camera.position.y)
        
        # if look.z != 0:
        #     z_correction = rl.Vector2(
        #         look_vector2.x * abs(self.camera.position.z / look.z),
        #         look_vector2.y * abs(self.camera.position.z / look.z)
        #     )
        #     self.cursor_position = rl.vector2_add(camera_vector2, z_correction)
    
    def update_lock(self, motion: rl.Vector2):
        self.camera.target = rl.Vector3(self.camera.position.x, self.camera.position.y, 0)
        self.cursor_position = rl.vector2_add(self.cursor_position, motion)

    # Math Functions

    def clamp(self, v, mn, mx):
        return max(min(v, mx), mn)
    
    def max_abs(self, v1, v2):
        return max(abs(v1), abs(v2))

    def range_normalized(self, x, mn, mx):
        x = self.clamp(x, mn, mx)
        return int((x - mn) / (mx - mn) * 255)