import math
from map.format.sspm import SSPM

class ScoreManager:
    def __init__(self):
        self.hits: int = 0
        self.misses: int = 0
        self.total: int = 0

        self.accuracy: float = 1.0

        self.combo: int = 0
        self.max_combo: int = 0
    
    def add_hit(self):
        self.hits += 1
        self.combo += 1
        self.max_combo = max(self.combo, self.max_combo)
        self.update_accuracy()

    def add_miss(self):
        self.misses += 1
        self.combo = 0
        self.update_accuracy()
    
    def update_accuracy(self):
        self.total: int = self.hits + self.misses
        if self.misses == 0:
            return 1.0
        self.accuracy: float = round(1.0 if self.hits <= 0 else self.hits / self.total, 4)