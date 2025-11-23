from map.format.sspm import SSPM
from typing import TYPE_CHECKING
from config.settings_manager import SettingsManager, Settings

if TYPE_CHECKING:
    from game.coordinator import Coordinator
    # So I can see the class types!

coordinator: "Coordinator" = None
sspm_map: SSPM = None

settingsmgr = SettingsManager()
settingsmgr.read_settings()

settings = settingsmgr.settings
