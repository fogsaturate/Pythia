import pyray as rl
import scene.scene_manager as scene_manager
from globals import settings

def main():

    screen_width = settings.width
    screen_height = settings.height

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)

    rl.init_window(screen_width, screen_height, "Pythia")
    rl.init_audio_device()

    SceneManager = scene_manager.SceneManager()

    while not rl.window_should_close():


        if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER) and rl.is_key_down(rl.KeyboardKey.KEY_LEFT_ALT) or rl.is_key_down(rl.KeyboardKey.KEY_RIGHT_ALT) and rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER):

            display = rl.get_current_monitor()

            if rl.is_window_fullscreen():
                rl.set_window_size(screen_width, screen_height)
            else:
                rl.set_window_size(rl.get_monitor_width(display), rl.get_monitor_height(display))

            rl.toggle_fullscreen()

        SceneManager.render_scene()
        
    rl.close_window()


if __name__ == "__main__":
    main()