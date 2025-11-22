import pyray as rl
import scenemanager

def main():

    screen_width: int = 1600
    screen_height: int = 900

    rl.set_config_flags(rl.FLAG_MSAA_4X_HINT)

    rl.init_window(screen_width, screen_height, "pySpace")
    rl.init_audio_device()

    rl.set_target_fps(60)
    rl.disable_cursor()

    SceneManager = scenemanager.SceneManager()

    while not rl.window_should_close():


        if rl.is_key_pressed(rl.KeyboardKey.KEY_ENTER) and rl.is_key_down(rl.KeyboardKey.KEY_LEFT_ALT):

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