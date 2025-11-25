from dataclasses import dataclass, field

@dataclass
class NoteSettings:
    approach_rate: float = 20
    approach_distance: float = 12
    fade_in: float = 0.25

    note_pushback: bool = True
    color_set: list[str] = field(default_factory=lambda: ["#00ffed", "ff8ff9"])

    half_ghost: bool = False # Unused

    def as_dict(self):
        return {
            "approach_rate": self.approach_rate,
            "approach_distance": self.approach_distance,
            "fade_in": self.fade_in,
            "note_pushback": self.note_pushback,
            "color_set": self.color_set,
            "half_ghost": self.half_ghost
        }

@dataclass
class PlayerSettings:
    sensitivity: float = 0.8
    absolute_mode: bool = False

    parallax: float = 1.0

    spin: bool = False
    cursor_drift: bool = False
    buffer_cursor_fade_distance: float = 5.0 # How long until the cursor is completely opaque
    speed: float = 1.0

    def as_dict(self):
        return {
            "sensitivity": self.sensitivity,
            "absolute_mode": self.absolute_mode,
            "parallax": self.parallax,
            "spin": self.spin,
            "cursor_drift": self.cursor_drift,
            "buffer_cursor_fade_distance": self.buffer_cursor_fade_distance,
            "speed": 1.0
        }

@dataclass
class AudioSettings:
    song_volume: float = 1.0 # 0.0 - 1.0 normalized
    hit_volume: float = 1.0 # hit sounds, [unused]

    warm_up_time: float = 1.0 # seconds before the song starts
    start_from_time: float = 0.0 # currently used as warm up time

    def as_dict(self):
        return {
            "song_volume": self.song_volume,
            "hit_volume": self.hit_volume,
            "warm_up_time": self.warm_up_time,
            "start_from_time": self.start_from_time
        }

@dataclass
class Settings:

    # General Settings

    width: int = 1920
    height: int = 1080

    fullscreen: bool = False

    fps = 0 # 0 = Uncapped

    note_settings: NoteSettings = field(default_factory=NoteSettings)
    player_settings: PlayerSettings = field(default_factory=PlayerSettings)
    audio_settings: AudioSettings = field(default_factory=AudioSettings)

    def as_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "fullscreen": self.fullscreen,
            "fps": 0,
            "note_settings": self.note_settings.as_dict(),
            "player_settings": self.player_settings.as_dict(),
            "audio_settings": self.audio_settings.as_dict()
        }