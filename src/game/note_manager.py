import pyray as rl
import math
from map.format.sspm import Note
import globals

class NoteManager:
    def __init__(self):
        self.note_model = rl.load_model("assets/meshes/Square.obj")
        rotate_y: float = math.radians(90)

        # # self.note_model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].color = rl.WHITE
        # self.transform = rl.matrix_scale(0.875,0.875,0.875)
        # self.transform = rl.matrix_multiply(self.transform, rl.matrix_rotate_y(rotate_y))
        
        self.transform = rl.matrix_rotate_y(rotate_y)

        self.approach_rate = 20
        self.approach_distance = 10
        self.approach_time = self.approach_distance / self.approach_rate

        self.hit_window: float = 0.055

        self.next_note: int = 0
        self.visible_notes: list[Note] = []
        self.coordinator = globals.coordinator


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

        # Note Rendering Logic
        for note in self.visible_notes:
            time_difference = note.time - map_time
            progress = time_difference / self.approach_time

            z_time = progress * self.approach_distance
            position = [note.x * 2, note.y * 2, -z_time]

            self.note_model.transform = self.transform
            rl.draw_model(self.note_model, position, 1.0, rl.WHITE)
        
        # Hit Detection Logic
        hits: list[Note] = []
        for note in self.visible_notes:
            # Skip this note if it hasn't passed the border yet
            if map_time < note.time:
                break

            aabb: float = max(
                abs((note.x * 2) - globals.coordinator.playermgr.clamped_cursor_position.x),
                abs((note.y * 2) - globals.coordinator.playermgr.clamped_cursor_position.y)
            )

            if aabb <= 1.1375:
                hits.append(note)
                globals.coordinator.scoremgr.add_hit()
        
        # Made a new list so it doesn't cycle in itself
        for note in hits:
            self.visible_notes.remove(note)
        
        # Miss Detection Logic
        # If there are visible notes on-screen, continue
        while len(self.visible_notes) > 0:
            note = self.visible_notes[0]

            # If the note hasn't passed the border AND the hit window, then skip
            if map_time < note.time + self.hit_window:
                break

            globals.coordinator.scoremgr.add_miss()
            self.visible_notes.pop(0)


