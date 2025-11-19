import pyray as rl
import game.player as player
from sceneenum import SceneEnum
from game.notemanager import NoteManager
from game.syncmanager import SyncManager
import globals
# import pysspm_rhythia as sspm_parser
import os

class PlayScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
    
    def awake(self):
        self.sspm_map = globals.sspm_map
        self.syncmgr = SyncManager(self.sspm_map)
        self.syncmgr.start()
        self.notemgr = NoteManager()
    def update(self):
        # 3D Scene

        player.update_camera()
        self.syncmgr.update()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.draw_fps(50,50)

        rl.begin_mode_3d(player.camera)

        # rl.draw_plane([0.0,-2.0,0.0], [32.0,32.0], rl.DARKGRAY)
        self.notemgr.update_notes(self.syncmgr)

        rl.end_mode_3d()
        rl.end_drawing()