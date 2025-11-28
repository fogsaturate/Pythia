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

        # self.coordinator.playermgr.update()
        self.coordinator.syncmgr.update()

        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        rl.draw_fps(20,20)

        # no need for health calculations if no health to be generated!
        if self.coordinator.scoremgr.health != 0:
            self.draw_health(self.coordinator.scoremgr.health)

        # Statistics -------
        rl.draw_text(f"Hits: {str(self.coordinator.scoremgr.hits)}", 50, 75, 30, rl.WHITE)
        rl.draw_text(f"Misses: {str(self.coordinator.scoremgr.misses)}", 50, 115, 30, rl.RED)
        rl.draw_text(f"x{str(self.coordinator.scoremgr.combo)}", 30, rl.get_screen_height() - 65, 55, rl.WHITE)

        # Time Bar -------
        time_bar_padding = 5
        rl.draw_rectangle_v([0,rl.get_screen_height() - time_bar_padding], [rl.get_screen_width(), time_bar_padding], rl.GRAY)
        time_normalized = rl.normalize(self.coordinator.syncmgr.get_sync_time(), 0, self.coordinator.syncmgr.song_length)
        rl.draw_rectangle_v([0,rl.get_screen_height() - time_bar_padding], [time_normalized * rl.get_screen_width(), time_bar_padding], rl.WHITE)

        # Accuracy -------
        acc: str = f"{self.coordinator.scoremgr.accuracy * 100:.2f}%"
        acc_width = rl.measure_text(acc, 35)
        x_center = (rl.get_screen_width() / 2) - (acc_width / 2)
        rl.draw_text(acc, int(x_center), 50, 35, rl.WHITE)

        # 3D Manager Draw -------

        rl.begin_mode_3d(self.coordinator.playermgr.camera)

        self.coordinator.notemgr.update_notes()
        self.coordinator.playermgr.draw()
        self.coordinator.playermgr.update()


        # Grid
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
        health_progress = self.coordinator.syncmgr.get_sync_time() - self.coordinator.scoremgr.health_time
        # Stop the health progress at duration
        step = self.clamp(health_progress / tween_duration, 0, 1)

        # Get last health so we know what to ease to and from
        last_health_normalized = self.normalize(self.coordinator.scoremgr.last_health, 0, 40)
        # Ease method will always be 1, so do linear interpolation from the last health to the current health, but tweened
        ease = pytweening.easeOutCubic(step)
        tweened_health = last_health_normalized + (normalized_health - last_health_normalized) * ease

        rec_pos: rl.Vector2 = rl.Vector2(0,0) # x, y
        # Multiply to 1920 to stretch it across the screen
        rec_size: rl.Vector2 = rl.Vector2(tweened_health * rl.get_screen_width(), 8) # width, height

        rl.draw_rectangle_v(rec_pos, rec_size, health_color)

    def normalize(self, x, mn, mx):
        x = self.clamp(x, mn, mx)
        return (x - mn) / (mx - mn)

    def clamp(self, v, mn, mx):
        return max(min(v, mx), mn)