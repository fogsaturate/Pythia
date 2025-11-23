import pyray as rl
from scene.scene_enum import SceneEnum
from tkinter import filedialog as fd
from map.format.sspm import SSPMParser
import globals
import os
import threading

class InitScene:
    def __init__(self, scene_manager):
        self.decoding_finished: bool = False
        self.scene_manager = scene_manager
    
    def awake(self):
        appdata_roaming = os.getenv("APPDATA")
        self.ssp_folder = os.path.join(appdata_roaming, "SoundSpacePlus")
        self.map_folder = os.path.join(self.ssp_folder, "maps")

        self.filename = None

        thread = threading.Thread(target=self.decoding_thread)
        thread.start()

        # self.scene_manager.switch_scene(SceneEnum.PLAY)
    
    def decoding_thread(self):
        if os.path.isdir(self.ssp_folder):
            self.filename = fd.askopenfilename(initialdir=self.map_folder)
        else:
            self.filename = fd.askopenfilename()
        
        current_time = rl.get_time()
        parser = SSPMParser()
        globals.sspm_map = parser.SSPMDecoder(self.filename)
        self.decoding_finished = True
        finished_time = rl.get_time()
        print(f"Decoded {self.filename}! Finished in {finished_time - current_time}.")

    def update(self):
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.draw_text("Pythia", int(rl.get_screen_width() / 2), int(rl.get_screen_height() / 2), 50, rl.RAYWHITE)

        rl.end_drawing()

        if self.decoding_finished:
            if globals.settings.fullscreen:
                rl.toggle_fullscreen()
            self.scene_manager.switch_scene(SceneEnum.PLAY)
