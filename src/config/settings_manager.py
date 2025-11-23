from config.settings_dataclass import Settings
import json
import os

# Can

class SettingsManager:
    def __init__(self):
        # Init Default
        self.settings = Settings()
        self.settings_path = "settings.json"

    # Main Function

    def read_settings(self):
        if not os.path.exists(self.settings_path):
            print("Settings not found! Creating settings.json...")
            self.create_default_settings()

        try:
            with open(self.settings_path, 'r') as file:
                json_obj = json.load(file)

            self.load_settings(json_obj)
            print("Settings loaded!")

        except Exception as err:
            print(f"Error loading settings. {err}")

    # Side Functions
    
    def create_default_settings(self):

        json_string = json.dumps(self.settings.as_dict(), indent=4)

        with open(self.settings_path, 'w') as file:
            file.write(json_string)
    
    def load_settings(self, json_obj):

        # General Settings
        self.settings.width = json_obj["width"]
        self.settings.height = json_obj["height"]
        self.settings.fullscreen = json_obj["fullscreen"]

        # Note Settings
        note_obj = json_obj["note_settings"]

        self.settings.note_settings.approach_rate = note_obj["approach_rate"]
        self.settings.note_settings.approach_distance = note_obj["approach_distance"]
        self.settings.note_settings.fade_in = note_obj["fade_in"]
        self.settings.note_settings.note_pushback = note_obj["note_pushback"]
        self.settings.note_settings.color_set = note_obj["color_set"]
        self.settings.note_settings.half_ghost = note_obj["half_ghost"]

        # Player Settings
        player_obj = json_obj["player_settings"]

        self.settings.player_settings.sensitivity = player_obj["sensitivity"]
        self.settings.player_settings.absolute_mode = player_obj["absolute_mode"]
        self.settings.player_settings.parallax = player_obj["parallax"]
        self.settings.player_settings.spin = player_obj["spin"]
        self.settings.player_settings.cursor_drift = player_obj["cursor_drift"]

        # Audio Settings
        audio_obj = json_obj["audio_settings"]

        self.settings.audio_settings.song_volume = audio_obj["song_volume"]
        self.settings.audio_settings.hit_volume = audio_obj["hit_volume"]
        self.settings.audio_settings.warm_up_time = audio_obj["warm_up_time"]
        self.settings.audio_settings.start_from_time = audio_obj["start_from_time"]