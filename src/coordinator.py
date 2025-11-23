from map.format.sspm import SSPM
from game.notemanager import NoteManager
from game.player import PlayerManager
from game.syncmanager import SyncManager
from game.score import ScoreManager

class Coordinator:
    def __init__(self):
        self.notemgr: NoteManager = None
        self.playermgr: PlayerManager = None
        self.syncmgr: SyncManager = None
        self.scoremgr: ScoreManager = None

        self.sspm_map: SSPM = None
    
    def init_notemgr(self):
        self.notemgr = NoteManager()

    def init_playermgr(self):
        self.playermgr = PlayerManager()

    def init_syncmgr(self, sspm_map):
        self.syncmgr = SyncManager(sspm_map)
    
    def init_scoremgr(self):
        self.scoremgr = ScoreManager()
        print(self.scoremgr.total)