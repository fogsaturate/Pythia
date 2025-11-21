import pyray as rl
import game.player as player
from sceneenum import SceneEnum
from game.notemanager import NoteManager
from game.syncmanager import SyncManager
import globals
# import pysspm_rhythia as sspm_parser
import math

class PlayScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
    
    def awake(self):
        self.sspm_map = globals.sspm_map
        self.syncmgr = SyncManager(self.sspm_map)
        self.syncmgr.start()
        self.notemgr = NoteManager()

        # Border/Grid Texture
        self.border_texture = rl.load_texture("assets/images/grid.png")
        self.plane = rl.load_model_from_mesh(rl.gen_mesh_plane(7.5,7.5,1,1))
        self.plane.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].texture = self.border_texture
        self.transform = rl.matrix_rotate_x(math.radians(90))
        self.plane.transform = self.transform


    def update(self):
        # 3D Scene

        player.update_camera()
        self.syncmgr.update()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.draw_fps(50,50)
        # rl.draw_texture(self.border_texture, 20,20, rl.WHITE)

        rl.begin_mode_3d(player.camera)



        self.notemgr.update_notes(self.syncmgr)
        rl.draw_model(self.plane, [0.0,0.0,0.0], 1.0, rl.WHITE)

        rl.end_mode_3d()
        rl.end_drawing()