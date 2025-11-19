# This will be for camera, and game logic
# So for how accuracy is calculated, settings, camera lock, spin, etc.

import pyray as rl

camera = rl.Camera3D()

camera.position = [0.0, 0.0, 7.5]
camera.target = [0.0, 0.0, 0.0]
camera.up = [0.0, 1.0, 0.0]
camera.fovy = 70
camera.projection = 0

sensitivity = 0.05


def update_camera() -> None:
    mouse_movement_x = rl.get_mouse_delta().x * sensitivity
    mouse_movement_y = rl.get_mouse_delta().y * sensitivity
    rl.update_camera_pro(camera, [0.0,0.0,0.0], [mouse_movement_x, mouse_movement_y, 0.0], 0.0)
