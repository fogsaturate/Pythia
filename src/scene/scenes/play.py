import pyray as rl
from scene.scene_enum import SceneEnum
from game.note_manager import NoteManager
from game.sync_manager import SyncManager
from game.player_manager import PlayerManager
from game.coordinator import Coordinator
import globals
# import pysspm_rhythia as sspm_parser
import math

class PlayScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
    
    def awake(self):
        globals.coordinator = Coordinator()

        self.coordinator = globals.coordinator

        globals.coordinator.init_syncmgr(globals.sspm_map)
        globals.coordinator.syncmgr.start(-1.0)
        globals.coordinator.init_notemgr()
        globals.coordinator.init_playermgr()
        globals.coordinator.init_scoremgr()

        print(self.coordinator.playermgr)

        # Border/Grid Texture
        self.border_texture = rl.load_texture("assets/images/grid.png")
        self.border_plane = rl.load_model_from_mesh(rl.gen_mesh_plane(6.0,6.0,1,1))
        self.border_plane.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.border_texture
        self.transform = rl.matrix_rotate_x(math.radians(90))
        self.border_plane.transform = self.transform


    def update(self):
        # 3D Scene

        self.coordinator.playermgr.update()
        self.coordinator.syncmgr.update()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.draw_fps(50,50)

        rl.draw_text(f"Hits: {str(self.coordinator.scoremgr.hits)}", 50, 75, 20, rl.WHITE)
        rl.draw_text(f"Misses: {str(self.coordinator.scoremgr.misses)}", 50, 100, 20, rl.RED)
        rl.draw_text(f"{self.coordinator.scoremgr.accuracy * 100:.2f}%", int(rl.get_screen_width() / 2), 50, 24, rl.YELLOW)

        rl.begin_mode_3d(self.coordinator.playermgr.camera)

        self.coordinator.notemgr.update_notes(self.coordinator.syncmgr)
        self.coordinator.playermgr.draw()
        rl.draw_model(self.border_plane, [0.0,0.0,0.0], 1.0, rl.WHITE)

        rl.end_mode_3d()
        rl.end_drawing()