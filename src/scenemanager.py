import pyray as rl
from sceneenum import SceneEnum
from scene.init import InitScene
from scene.play import PlayScene

import map.format.sspm as sspm
from map.format.sspm import SSPM

# This will also be used as my global variables container

class SceneManager:
    def __init__(self):
        self.scene_int: SceneEnum = SceneEnum.INIT
        self.init_scene = InitScene(self)
        self.play_scene = PlayScene(self)

        self.get_scene_int().awake()

    def get_scene_int(self):
        match self.scene_int:
            case SceneEnum.INIT:
                return self.init_scene
            case SceneEnum.PLAY:
                return self.play_scene

    def render_scene(self):
        self.get_scene_int().update()
    
    def switch_scene(self, switch_int: SceneEnum):
        self.scene_int = switch_int
        self.get_scene_int().awake()