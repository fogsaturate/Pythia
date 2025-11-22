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

        self.sensitivity = 0.05

        self.spin: bool = False

        self.cursor_texture = rl.load_texture("assets/images/cursor.png")
        self.cursor_plane = rl.load_model_from_mesh(rl.gen_mesh_plane(0.525,0.525,1,1))
        self.cursor_plane.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.cursor_texture
        self.transform = rl.matrix_rotate_x(math.radians(90))
        self.cursor_plane.transform = self.transform

        # The Z axis is always the same for the cursor position
        self.cursor_x = 0.0
        self.cursor_y = 0.0

        self.cursor_position = rl.Vector2()

    # Input Update
    def update(self):
        mouse_movement_x = rl.get_mouse_delta().x * self.sensitivity
        mouse_movement_y = rl.get_mouse_delta().y * self.sensitivity
        rl.update_camera_pro(self.camera, [0.0,0.0,0.0], [mouse_movement_x, mouse_movement_y, 0.0], 0.0)

        cam_pos = self.camera.position

        # Simulation of Godot's Basis.Z
        look = rl.vector3_subtract(self.camera.target, self.camera.position)
        
        z_correction = rl.vector2_scale(rl.Vector2(look.x, look.y), abs(cam_pos.z / look.z))

        self.cursor_position = z_correction


        
    # Draw Update (for cursor textures n such)
    def draw(self):
        rl.draw_model(self.cursor_plane, [self.cursor_position.x,self.cursor_position.y,0.0], 1.0, rl.WHITE)