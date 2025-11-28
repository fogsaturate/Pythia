import pyray as rl
import math
from map.format.sspm import Note
import globals

note_settings = globals.settings.note_settings
speed = globals.settings.player_settings.speed

class NoteManager:
    def __init__(self):
        self.note_model = rl.load_model(note_settings.mesh_path)

        mesh_rotation = note_settings.mesh_rotation_offset
        model_rotate = rl.Vector3(math.radians(mesh_rotation[0]), math.radians(mesh_rotation[1]), math.radians(mesh_rotation[2]))

        # # self.note_model.materials[0].maps[rl.MATERIAL_MAP_DIFFUSE].color = rl.WHITE
        # self.transform = rl.matrix_scale(0.875,0.875,0.875)
        # self.transform = rl.matrix_multiply(self.transform, rl.matrix_rotate_y(rotate_y))
        
        self.transform = rl.matrix_rotate_xyz(model_rotate)

        self.approach_rate = note_settings.approach_rate / speed
        self.approach_distance = note_settings.approach_distance
        self.approach_time = self.approach_distance / self.approach_rate

        self.hit_window: float = 0.055 * speed

        self.next_note: int = 0
        self.visible_notes: list[Note] = []

        self.start_from_time: float = globals.settings.audio_settings.start_from_time
        self.coordinator = globals.coordinator

        self.colors = self.load_colors(note_settings.color_set)

        # Start From Logic
        i = 0
        while i < len(globals.sspm_map.note_list):
            if globals.sspm_map.note_list[i].time < self.start_from_time:
                globals.sspm_map.note_list.pop(i)
            else:
                i+= 1

    def update_notes(self):
        map_time = globals.coordinator.syncmgr.get_sync_time()

        # Note Visibility Logic
        while self.next_note < len(globals.sspm_map.note_list):
            note = globals.sspm_map.note_list[self.next_note]

            # If the note is ahead of the map time by how much approach time, then skip
            if note.time > map_time + self.approach_time:
                break

            self.visible_notes.append(note)
            self.next_note += 1

        # Note Rendering Logic
        for note in reversed(self.visible_notes):
            
            note_color: rl.Color = self.colors[note.index % len(self.colors)]

            time_difference = note.time - map_time
            progress = time_difference / self.approach_time

            z_time = progress * self.approach_distance
            position = [note.x * 2, note.y * 2, -z_time]

            self.note_model.transform = self.transform

            
            fade_in = None
            fade_out = None

            if note_settings.fade_in != 0:
                fade_in = max((1 - progress) / note_settings.fade_in, 1)
            else:
                fade_in = 1.0
            

            if note_settings.half_ghost:
                # im copying ssplus i dont care
                fade_out_base = 0.8
                fade_out_start = 0.24
                fade_out_end = 0.06

                fade_out = ((1 - fade_out_base) + (pow(self.linear_step(fade_out_end,fade_out_start, progress), 1.3) * fade_out_base))
            else:
                fade_out = 1.0

            alpha = min(fade_in, fade_out)
            # I can just use the same color here since the fade function just changes the alpha
            note_color.a = int(alpha * 255)

            # If note is past the border and pushback is off, then skip rendering
            if time_difference > 0 and not note_settings.note_pushback:
                rl.draw_model(self.note_model, position, 1.0, note_color)
            elif note_settings.note_pushback:
                rl.draw_model(self.note_model, position, 1.0, note_color)

        # Hit Detection Logic
        for note in self.visible_notes:
            # Skip this note if it hasn't passed the border yet
            if map_time < note.time:
                break

            aabb: float = max(
                abs((note.x * 2) - globals.coordinator.playermgr.clamped_cursor_position.x),
                abs((note.y * 2) - globals.coordinator.playermgr.clamped_cursor_position.y)
            )

            if aabb <= 1.1375:
                note.hit = True
        
        # Note Removal/Miss Detection Logic

        visible_notes_cont = []
        for note in self.visible_notes:
            if note.hit:
                globals.coordinator.scoremgr.add_hit()
                continue
            elif map_time >= note.time + self.hit_window:
                globals.coordinator.scoremgr.add_miss()
                continue
            else:
                visible_notes_cont.append(note)
        self.visible_notes = visible_notes_cont



    # Conversion Library

    def str_to_color(self, hex: str) -> rl.Color:
        hex_str: str = ""

        if "#" in hex:
            hex_str = hex.replace("#", "") # Get rid of the optional # character
        else:
            hex_str = hex

        r: int = int(hex_str[0:2], 16)
        g: int = int(hex_str[2:4], 16)
        b: int = int(hex_str[4:6], 16)

        return rl.Color(r,g,b,255)

    def load_colors(self, string_list: list[str]) -> list[rl.Color]:
        color_list: list[rl.Color] = []
        
        for color in string_list:
            color_list.append(self.str_to_color(color))

        return color_list

    def clamp(self, v, mn, mx):
        return max(min(v, mx), mn)
    
    def linear_step(self, mn, mx, step):
        return self.clamp((step - mn) / (mx - mn), 0, 1)


