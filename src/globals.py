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

# Module Stuff head

def clamp(v, mn, mx):
    return max(min(v, mx), mn)

def linear_step(mn, mx, step):
    return clamp((step - mn) / (mx - mn), 0, 1)

class Node:
    def __init__(self, data: any):
        self.data = data
        self.next = None
        self.previous = None

class DoublyLinkedList:
    def __init__(self):
        self.head: Node | None = None # Start of List
        self.tail: Node | None = None # End of List
        
    def add_first(self, data):
        new_node = Node(data)
        new_node.next = self.head

        if self.head:
            self.head.previous = new_node
        else:
            self.tail = new_node
        
        self.head = new_node
    
    def add_last(self, data):
        new_node = Node(data)

        # Make a new list
        if self.tail == None:
            self.head = new_node
            self.tail = new_node

        self.tail.next = new_node
        new_node.previous = self.tail
        self.tail = new_node