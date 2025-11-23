# This will be for camera, and game logic
# So for how accuracy is calculated, settings, camera lock, spin, etc.

import pyray as rl
import math

class PlayerManager:
    def __init__(self):
        self.camera = rl.Camera3D()

        self.camera.position = [0.0, 0.0, 7.5]
        self.camera.target = [0.0, 0.0, 1.0]
        self.camera.up = [0.0, 1.0, 0.0]
        self.camera.fovy = 70
        self.camera.projection = 0
        self.camera_pivot = self.camera.position
        self.parallax = 1.0

        self.sensitivity = 5 / 500

        self.spin: bool = True

        self.cursor_texture = rl.load_texture("assets/images/cursorz.png")
        self.cursor_plane = rl.load_model_from_mesh(rl.gen_mesh_plane(0.525,0.525,1,1))
        self.cursor_plane.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.cursor_texture
        self.transform = rl.matrix_rotate_x(math.radians(90))
        self.cursor_plane.transform = self.transform
        
        self.cursor_position = rl.Vector2()
        self.clamped_cursor_position = rl.Vector2()
        self.spin_rotation = rl.Vector2()

    # Input Update
    def update(self):
        mouse_delta = rl.Vector2(rl.get_mouse_delta().x, -rl.get_mouse_delta().y)
        motion = rl.vector2_scale(mouse_delta, self.sensitivity)

        # self.camera.target = rl.Vector3(self.spin_rotation.x, self.spin_rotation.y, 0)

        # Simulation of Godot's Basis.Z
        look = rl.vector3_subtract(self.camera.target, self.camera.position)

        # Input/Cursor Movement Logic

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

        self.camera.position = rl.vector3_add(pivot, rl.Vector3(
            self.clamped_cursor_position.x * (self.parallax / 4) + (look.x / 2),
            self.clamped_cursor_position.y * (self.parallax / 4) + (look.y / 2),
            0
        ))

        # End of Parallax Calculation


    # Draw Update (for cursor textures n such)
    def draw(self):
        rl.draw_model(self.cursor_plane, [self.clamped_cursor_position.x, self.clamped_cursor_position.y, 0.0], 1.0, rl.WHITE)
    
    def update_spin(self, motion: rl.Vector2):

        rl.update_camera_pro(self.camera, [0,0,0], [motion.x * 7.5, -motion.y * 7.5, 0.0], 0.0)

        look = rl.vector3_subtract(self.camera.target, self.camera.position)
        if look.z != 0:
            self.cursor_position = rl.Vector2(
                self.camera.position.x - look.x * self.camera.position.z / look.z,
                self.camera.position.y - look.y * self.camera.position.z / look.z
            )
            
    
    def update_lock(self, motion: rl.Vector2):
        self.camera.target = rl.vector3_zero()
        self.cursor_position = rl.vector2_add(self.cursor_position, motion)

    def clamp(self, v, mn, mx):
        return max(min(v, mx), mn)