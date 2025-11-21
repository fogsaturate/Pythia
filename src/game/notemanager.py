import pyray as rl
import math
import globals
# from syncmanager import SyncManager
from map.format.sspm import Note

class NoteManager:
    def __init__(self):
        self.note_model = rl.load_model("assets/meshes/Square.obj")
        rotate_y: float = math.radians(90)
        # # self.note_model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].color = rl.WHITE

        # self.transform = rl.matrix_scale(0.5,0.5,0.5)
        # self.transform = rl.matrix_multiply(self.transform, rl.matrix_rotate_y(rotate_y))
        self.transform = rl.matrix_rotate_y(rotate_y)

        self.approach_rate = 20
        self.approach_distance = 10
        self.approach_time = self.approach_distance / self.approach_rate

        self.hit_window: float = 1.75 / 30

        self.next_note: int = 0
        self.visible_notes: list[Note] = []

    def update_notes(self, syncmanager):
        map_time = syncmanager.get_sync_time()

        # Note Visibility Logic
        while self.next_note < len(globals.sspm_map.note_list):
            note = globals.sspm_map.note_list[self.next_note]

            # If the note is ahead of the map time by how much approach time
            if note.time > map_time + self.approach_time:
                break

            self.visible_notes.append(note)
            self.next_note += 1

        # Miss Note Logic
        while len(self.visible_notes) > 0:
            note = self.visible_notes[0]
            if map_time < note.time + self.hit_window:
                break
            
            
            self.visible_notes.pop(0)

        # Note Rendering Logic
        for note in self.visible_notes:
            time_difference = note.time - map_time

            progress = time_difference / self.approach_time
            # inverse_progress = 1 - progress

            z_time = progress * self.approach_distance
            position = [note.x * 2, note.y * 2, -z_time]

            # if visible:
            self.note_model.transform = self.transform
            rl.draw_model(self.note_model, position, 1.0, rl.WHITE)
            