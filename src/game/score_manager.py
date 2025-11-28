import math
from map.format.sspm import SSPM
import pyray as rl
import globals

class ScoreManager:
    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.total: int = 0

        self.accuracy: float = 1.0

        self.combo: int = 0
        self.max_combo: int = 0

        self.health: int = 40
        self.last_health: int = 40
        self.health_time: float = 0 # will be used for easing
        self.failed = False

        self.syncmgr = globals.coordinator.syncmgr
    
    def add_hit(self):
        self.hits += 1
        self.combo += 1
        self.max_combo = max(self.combo, self.max_combo)
        self.update_accuracy()

        if self.health < 40 and not self.failed:
            self.last_health = self.health
            self.health = min(self.health + 5, 40)
            self.health_time = self.syncmgr.get_sync_time()

    def add_miss(self):
        self.misses += 1
        self.combo = 0
        self.update_accuracy()

        if not self.failed:
            self.last_health = self.health
            self.health = max(self.health - 8, 0)
            self.health_time = self.syncmgr.get_sync_time()
            if self.health == 0: self.failed = True
    
    def update_accuracy(self):
        self.total: int = self.hits + self.misses
        if self.misses == 0:
            return 1.0
        elif self.hits == 0:
            return 0.0
        self.accuracy: float = round(1.0 if self.hits <= 0 else self.hits / self.total, 4)
