from map.format.sspm import SSPM
import pyray as rl
import globals

audio_settings = globals.settings.audio_settings
speed = globals.settings.player_settings.speed

class SyncManager:
    def __init__(self, sspm: SSPM):
        audio_data = sspm.audio_data

        audio_extension: str = sspm.CheckAudioFormat(audio_data)

        match audio_extension:
            case "oga":
                audio_extension = ".ogg"
            case "mp3":
                audio_extension = ".mp3"
            case _:
                print(f"Unknown Extension!: {audio_extension}")
                audio_extension = ".mp3"

        self.music_stream: rl.Music = rl.load_music_stream_from_memory(audio_extension, audio_data, len(audio_data))
        rl.set_music_pitch(self.music_stream, speed)

        self.start_time = 0.0
        self.time = 0.0 # Will be counted in update()

        self.started = False
        self.song_length = rl.get_music_time_length(self.music_stream)

        # This gets a minimum to prevent it from being negative
        self.from_time = min(audio_settings.start_from_time, 0.0)
        # This gets an absolute since people might mistake it for being opposite
        self.warm_up_time = abs(audio_settings.warm_up_time)

        self.finished = False

    def start(self):
        rl.set_music_volume(self.music_stream, audio_settings.song_volume)
        rl.play_music_stream(self.music_stream)

        self.start_time = rl.get_time() - (self.from_time - self.warm_up_time)

    def update(self):
        self.time = rl.get_time()

        syncmgr_time = self.get_sync_time() * speed
        music_time = rl.get_music_time_played(self.music_stream) * speed

        threshold = 0.150 # Offsync Threshold in seconds

        if syncmgr_time >= self.from_time:
            if not self.started:
                rl.play_music_stream(self.music_stream)
                rl.seek_music_stream(self.music_stream, syncmgr_time)
                self.started = True
            elif self.get_sync_time() < self.song_length:
                # Re-syncs the map, but only after it starts
                if abs(syncmgr_time - music_time) > threshold:
                    print(f"Resynced, offsync difference was {abs(syncmgr_time - music_time)}!")
                    rl.seek_music_stream(self.music_stream, syncmgr_time)
            elif self.get_sync_time() > self.song_length:
                self.finished = True
                rl.stop_music_stream(self.music_stream)
                rl.unload_music_stream(self.music_stream)
            
            rl.update_music_stream(self.music_stream)

    def get_sync_time(self):
        return (self.time - self.start_time) * speed
