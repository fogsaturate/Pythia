from typing import BinaryIO
from map.binary_reader import BinaryReader
from enum import Enum
from dataclasses import dataclass, field

class Difficulty(Enum):
    NA = 0
    EASY = 1
    MEDIUM = 2
    HARD = 3
    LOGIC = 4
    TASUKETE = 5

@dataclass
class Note:
    x: float = 0.0
    y: float = 0.0
    time: float = 0.0 # in seconds
    index: int = 0

@dataclass
class SSPM:
    header: str = ""
    version: int = 0

    last_ms: int = 0
    total_note_count: int = 0
    total_marker_count: int = 0

    difficulty: int = 0
    star_rating: int = 0

    audio_exists: bool = False
    cover_exists: bool = False
    mod_chart_exists: bool = False

    map_id: str = ""
    map_name: str = ""
    song_name: str = ""
    mappers: list = field(default_factory=list)

    custom_data: dict = field(default_factory=dict)

    audio_data: bytes | None = None
    cover_data: bytes | None = None

    marker_definitions: dict = field(default_factory=dict)

    markers: dict = field(default_factory=dict)
    note_list: list[Note] = field(default_factory=list)

class SSPMParser:
    def __init__(self):
        self.header: str = ""
        self.version: int = 0

        self.last_ms: int = 0
        self.total_note_count: int = 0
        self.total_marker_count: int = 0

        self.difficulty: int = 0
        self.star_rating: int = 0

        self.audio_exists: bool = False
        self.cover_exists: bool = False
        self.mod_chart_exists: bool = False

        self.custom_data_offset: int = 0
        self.custom_data_length: int = 0
        self.audio_data_offset: int = 0
        self.audio_data_length: int = 0
        self.cover_data_offset: int = 0
        self.cover_data_length: int = 0
        self.marker_definition_offset: int = 0
        self.marker_definition_length: int = 0
        self.marker_section_offset: int = 0
        self.marker_section_length: int = 0

        self.map_id: str = ""
        self.map_name: str = ""
        self.song_name: str = ""
        self.mappers: list = []

        self.custom_data: dict = {}

        self.audio_data = None
        self.cover_data = None

        self.marker_definitions: dict = {}

        self.markers: dict = {}
        self.note_list: list[Note] = [] # for actual in-game parsing

    def data_types(self, file: BinaryIO, data_type: int):
        binary_reader = BinaryReader(file)
        match data_type:
            case 1: # 1 byte int
                return binary_reader.read_uint8()
            case 2: # 2 byte int
                return binary_reader.read_uint16()
            case 3: # 4 byte int
                return binary_reader.read_uint32()
            case 4: # 8 byte int
                return binary_reader.read_uint64()
            case 5: # 4 byte float
                return binary_reader.read_single()
            case 6: # 8 byte float
                return binary_reader.read_double()
            case 7: # note
                note_storage_type = bool(binary_reader.read_uint8()) # quantum bool

                if not note_storage_type:
                    x = binary_reader.read_uint8()
                    y = binary_reader.read_uint8()
                    return x, y
                else:
                    x = binary_reader.read_single()
                    y = binary_reader.read_single()
                    return x, y

            case 8: # short buffer
                buffer_length = binary_reader.read_uint16()
                return file.read(buffer_length)
            case 9: # short string
                return binary_reader.read_string_buffer(2)
            case 10: # long buffer
                long_buffer_length = binary_reader.read_uint32()
                return file.read(long_buffer_length)
            case 11: # long string
                return binary_reader.read_string_buffer(4)
            case 12: # array
                data_type_array = []

                array_data_type_length = binary_reader.read_uint32() # not even i know what this means
                array_object_count = binary_reader.read_uint16()

                array_data_type = binary_reader.read_uint8()
                for i in range(array_object_count):
                    data_type_array.append(self.data_types(file, array_data_type))
                return data_type_array



    def SSPMDecoder(self, sspm_map: str) -> SSPM:
        # try:
        with open(sspm_map, "rb") as file:
            binary_reader = BinaryReader(file)

            self.header = file.read(4).decode('utf-8')
            if self.header != "SS+m":
                raise ValueError(f"Invalid Header: {self.header}")

            self.version = binary_reader.read_uint16()

            sspm_file: SSPM | None = None
            if self.version == 2:
                sspm_file = self.SSPMv2(file)
            else:
                raise ValueError(f"Unsupported Version! This SSPM file is v{self.version}")
        # except:
        #     raise ValueError("Invalid file! Make sure it is a proper SSPM file.")

        return sspm_file

    def SSPMv1(self):

        pass

    def SSPMv2(self, file: BinaryIO) -> SSPM:
        binary_reader = BinaryReader(file)

        file.read(4)
        file.read(20) # reserved space
        # --- Parsing Metadata ---
        self.last_ms = binary_reader.read_uint32()
        self.total_note_count = binary_reader.read_uint32()
        self.total_marker_count = binary_reader.read_uint32()

        self.difficulty = binary_reader.read_uint8()

        self.star_rating = binary_reader.read_uint16() # Never Used

        self.audio_exists = bool(binary_reader.read_uint8())
        self.cover_exists = bool(binary_reader.read_uint8())
        self.mod_chart_exists = bool(binary_reader.read_uint8())

        # --- Pointers ---
        self.custom_data_offset = binary_reader.read_uint64()
        self.custom_data_length = binary_reader.read_uint64()
        self.audio_data_offset = binary_reader.read_uint64()
        self.audio_data_length = binary_reader.read_uint64()
        self.cover_data_offset = binary_reader.read_uint64()
        self.cover_data_length = binary_reader.read_uint64()
        self.marker_definition_offset = binary_reader.read_uint64()
        self.marker_definition_length = binary_reader.read_uint64()
        self.marker_section_offset = binary_reader.read_uint64()
        self.marker_section_length = binary_reader.read_uint64()

        # --- Song Metadata ---
        self.map_id = binary_reader.read_string_buffer(2)
        self.map_name = binary_reader.read_string_buffer(2)
        self.song_name = binary_reader.read_string_buffer(2)

        mapper_count = binary_reader.read_uint16()
        for i in range(mapper_count): # for every mapper in mapper_count,
            self.mappers.append(binary_reader.read_string_buffer(2))

        # --- Custom Data ---
        custom_data_object_count = binary_reader.read_uint16()

        custom_data_dict = {
            "custom_data_object_count": custom_data_object_count,
            "custom_data": []
        }
        try:
            for i in range(custom_data_object_count):
                custom_data_field_indicator = binary_reader.read_string_buffer(2) # usually going to be difficulty_name
                custom_data_object_data_type = binary_reader.read_uint8()
                custom_data_object_value = self.data_types(file, custom_data_object_data_type)

                custom_data_object = {
                    "field_indicator": custom_data_field_indicator,
                    "data_type": custom_data_object_data_type,
                    "value": custom_data_object_value
                }
                custom_data_dict["custom_data"].append(custom_data_object)

            self.custom_data = custom_data_dict
        except ValueError as e:
            print("Custom Data corrupted!")
            print(f"Error: {e}")
            print("skipping...")
            file.seek(self.audio_data_offset)

        # -- File Data --
        if self.audio_exists:
            self.audio_data = file.read(self.audio_data_length)
        if self.cover_exists:
            self.cover_data = file.read(self.cover_data_length)

        # -- Marker Definitions ---
        marker_definition_count = binary_reader.read_uint8()
        marker_definition_dict = {
            "marker_definition_count": custom_data_object_count,
            "marker_definition_data": []
        }
        for i in range(marker_definition_count):
            marker_definition_field_indicator = binary_reader.read_string_buffer(2)
            marker_definition_data_type_count = binary_reader.read_uint8()
            marker_definition_object = {
                "field_indicator": marker_definition_field_indicator,
                "data_type_count": marker_definition_data_type_count,
                "data_types": []
            }

            for j in range(marker_definition_data_type_count):
                marker_definition_data_type = binary_reader.read_uint8()
                marker_definition_object["data_types"].append(marker_definition_data_type)

            marker_definition_dict["marker_definition_data"].append(marker_definition_object)
            file.read(1)  # marker definitions must end in 0x00
        self.marker_definitions = marker_definition_dict

        # --- Markers ---

        marker_dict = {
            "marker_count": self.total_marker_count,
            "marker_data": []
        }
        for i in range(self.total_marker_count):
            time = binary_reader.read_uint32()
            marker_type = binary_reader.read_uint8() # what definition it is a part of (usually going to be 0)
            # marker_data_type = self.marker_definitions["marker_definition_data"][marker_type]["data_types"]
            for data_type in self.marker_definitions["marker_definition_data"][marker_type]["data_types"]:
                marker_data_dict = {
                    "time": time,
                    "marker_type": marker_type,
                    "marker_data_type": data_type,
                    "marker_object_data" : []
                }

                if data_type == 7:
                    marker_value = self.data_types(file, data_type)
                    marker_value_x, marker_value_y = marker_value
                    x = marker_value_x - 1
                    y = -marker_value_y + 1
                    marker_data_dict["marker_object_data"].append({"x": x, "y": y})

                    new_note = Note()
                    new_note.x = x
                    new_note.y = y
                    new_note.time = time / 1000

                    self.note_list.append(new_note)
                else:
                    marker_value = self.data_types(file, data_type)
                    marker_data_dict["marker_object_data"].append({"marker_value": marker_value})

                marker_dict["marker_data"].append(marker_data_dict)

        self.markers = marker_dict

        sorted_note_list = sorted(self.note_list, key=lambda Note: Note.time)

        # Indexes will also be out of order, so we need to fix that!
        for i in range(len(sorted_note_list)):
            note = sorted_note_list[i]

            note.index = i

        self.note_list = sorted_note_list

        return SSPM(
            self.header,
            self.version,

            self.last_ms,
            self.total_note_count,
            self.total_marker_count,

            self.difficulty,
            self.star_rating,

            self.audio_exists,
            self.cover_exists,
            self.mod_chart_exists,

            self.map_id,
            self.map_name,
            self.song_name,
            self.mappers,

            self.custom_data, # this is where difficulty names would go

            self.audio_data,
            self.cover_data,

            self.marker_definitions,

            self.markers,
            self.note_list # this is for easier parsing reasons
        )