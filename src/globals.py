from map.format.sspm import SSPM
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coordinator import Coordinator
    # So I can see the class types!

coordinator: "Coordinator" = None
sspm_map: SSPM = None