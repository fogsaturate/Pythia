import math
from map.format.sspm import SSPM

class ScoreManager:
    def __init__(self, sspm_map: SSPM):
        self.hits: int = 0
        self.misses: int = 0
        self.total: int = sspm_map.total_note_count

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
        self.accuracy: float = round(1.0 if self.hits <= 0 else (self.total - self.misses) / self.total, 4)