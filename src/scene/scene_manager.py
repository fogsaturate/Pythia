from scene.scene_enum import SceneEnum
from scene.scenes.init import InitScene
from scene.scenes.play import PlayScene
import cProfile

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