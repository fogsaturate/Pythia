import pyray as rl
from scene.scene_enum import SceneEnum
from game.note_manager import NoteManager
from game.sync_manager import SyncManager
from game.player_manager import PlayerManager
from game.coordinator import Coordinator
import globals
import math
import pytweening

class PlayScene:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
    
    def awake(self):
        globals.coordinator = Coordinator()

        self.coordinator = globals.coordinator

        globals.coordinator.init_syncmgr(globals.sspm_map)
        globals.coordinator.syncmgr.start()
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

        # health_color: rl.Color = rl.GREEN
        # if self.coordinator.scoremgr.health == 0:
        #     health_color = rl.GRAY
        # elif self.coordinator.scoremgr.health < 10:
        #     health_color = rl.RED
        # elif self.coordinator.scoremgr.health < 20:
        #     health_color = rl.YELLOW
        # elif self.coordinator.scoremgr.health < 30:
        #     health_color = rl.GREEN
        # rl.draw_text(f"Health: {str(self.coordinator.scoremgr.health)}", 50, 125, 40, health_color)
        self.draw_health(self.coordinator.scoremgr.health)

        rl.draw_text(f"Hits: {str(self.coordinator.scoremgr.hits)}", 50, 75, 20, rl.WHITE)
        rl.draw_text(f"Misses: {str(self.coordinator.scoremgr.misses)}", 50, 100, 20, rl.RED)

        rl.draw_text(f"x{str(self.coordinator.scoremgr.combo)}", 30, rl.get_screen_height() - 65, 55, rl.WHITE)

        rl.draw_text(f"{self.coordinator.scoremgr.accuracy * 100:.2f}%", int(rl.get_screen_width() / 2), 50, 24, rl.YELLOW)

        rl.begin_mode_3d(self.coordinator.playermgr.camera)

        self.coordinator.notemgr.update_notes()
        self.coordinator.playermgr.draw()
        rl.draw_model(self.border_plane, [0.0,0.0,0.0], 1.0, rl.WHITE)

        rl.end_mode_3d()
        rl.end_drawing()
    
    def draw_health(self, health: int):
        health_color: rl.Color = rl.GREEN
        if health == 0:
            health_color = rl.GRAY
        elif health < 10:
            health_color = rl.RED
        elif health < 20:
            health_color = rl.YELLOW
        elif health < 30:
            health_color = rl.GREEN
        
        # I will heavily comment this because even this confuses me but it works lol
        normalized_health = self.normalize(health, 0, 40)

        # How long the tween lasts
        tween_duration = 0.1
        # Time since last health hit
        health_progress = rl.get_time() - self.coordinator.scoremgr.health_time
        # Stop the health progress at duration
        step = self.clamp(health_progress / tween_duration, 0, 1)

        # Get last health so we know what to ease to and from
        last_health_normalized = self.normalize(self.coordinator.scoremgr.last_health, 0, 40)
        # Ease method will always be 1, so do linear interpolation from the last health to the current health, but tweened
        ease = pytweening.easeOutCubic(step)
        tweened_health = last_health_normalized + (normalized_health - last_health_normalized) * ease

        rec_pos: rl.Vector2 = rl.Vector2(0,0) # x, y
        # Multiply to 1920 to fill it back up!
        rec_size: rl.Vector2 = rl.Vector2(tweened_health * 1920, 8) # width, height

        rl.draw_rectangle_v(rec_pos, rec_size, health_color)

    def normalize(self, x, mn, mx):
        x = self.clamp(x, mn, mx)
        return (x - mn) / (mx - mn)

    def clamp(self, v, mn, mx):
        return max(min(v, mx), mn)