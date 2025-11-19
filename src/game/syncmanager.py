from map.format.sspm import SSPM
import pyray as rl

class SyncManager:
    def __init__(self, sspm: SSPM):
        audio_data = sspm.audio_data
        self.music_stream: rl.Music = rl.load_music_stream_from_memory(".mp3", audio_data, len(audio_data))

        self.start_time = 0.0
        self.time = 0.0 # Will be counted in update()

        self.seeked = False

    def start(self):
        rl.set_music_volume(self.music_stream, 0.2)
        rl.play_music_stream(self.music_stream)
        self.start_time = rl.get_time()

    def update(self):
        rl.update_music_stream(self.music_stream)
        self.time = rl.get_time()

        syncmgr_time = self.get_sync_time()
        music_time = rl.get_music_time_played(self.music_stream)

        threshold = 0.150 # offsync threshold in seconds

        if abs(syncmgr_time - music_time) > threshold:
            print(f"Resynced, offsync difference was {abs(syncmgr_time - music_time)}!")
            rl.seek_music_stream(self.music_stream, syncmgr_time)


        # print(f"Music: {music_time}, Sync: {syncmgr_time}")

    def get_sync_time(self):
        return self.time - self.start_time