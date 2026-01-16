from gdpc import Editor, Block

# It is recommended to use buffering, especially for larger structures.
editor = Editor(buffering=True)

# === Constants ===
# Define the dimensions for each modular room of the house.
ROOM_WIDTH = 12
ROOM_LENGTH = 12
ROOM_HEIGHT = 6

# Define building materials based on the provided JSON for easy access and modification.
MATERIALS = {
    "foundation": "polished_andesite",
    "frame": "dark_oak_log",
    "walls": "white_wool",
    "windows": "glass_pane",
    "shutters": "spruce_trapdoor",
    "roof": "deepslate_tiles",
    "roof_stairs": "deepslate_tile_stairs",
    "roof_slab": "deepslate_tile_slab",
    "flooring": "polished_andesite",
    "door": "dark_oak_door",
    "ceiling": "dark_oak_wood",
    "stair_material": "dark_oak_stairs",
    "fence": "dark_oak_fence"
}

# === Utility Functions ===
# These functions are general-purpose tools for building structures.
# They are retained from the example code to maintain consistency and functionality.

def place_filled_room(x1, y1, z1, width, length, height, wall, floor, ceiling):
    """Builds a hollow room with specified materials for walls, floor, and roof."""
    if ceiling == "air":
        ceiling = "glass"

    # Place floor
    for x in range(width):
        for z in range(length):
            editor.placeBlock((x1 + x, y1, z1 + z), Block(floor))
            editor.placeBlock((x1 + x, y1 + height - 1, z1 + z), Block(ceiling))

    # Place walls
    for y in range(1, height - 1):
        for x in range(width):
            editor.placeBlock((x1 + x, y1 + y, z1), Block(wall))
            editor.placeBlock((x1 + x, y1 + y, z1 + length - 1), Block(wall))
        for z in range(1, length - 1):
            editor.placeBlock((x1, y1 + y, z1 + z), Block(wall))
            editor.placeBlock((x1 + width - 1, y1 + y, z1 + z), Block(wall))


def place_wall_section(x1, y1, z1, width, height, material, direction, length=1):
    """Replaces a section of a wall with a different material, ideal for windows."""
    for w in range(width):
        for h in range(height):
            for l in range(length):
                if direction == 'north':
                    editor.placeBlock((x1 + w, y1 + h, z1 - l), Block(material))
                elif direction == 'south':
                    editor.placeBlock((x1 + w, y1 + h, z1 + l), Block(material))
                elif direction == 'west':
                    editor.placeBlock((x1 - l, y1 + h, z1 + w), Block(material))
                elif direction == 'east':
                    editor.placeBlock((x1 + l, y1 + h, z1 + w), Block(material))


def place_3x3_arch(x, y, z, width, length, direction):
    """Creates a 3x3 'air' opening in a wall to serve as a passage."""
    # Calculate starting position based in the center of the specified wall.
    if direction == 'north':
        x, y, z = x + width // 2 - 1, y + 1, z
    elif direction == 'south':
        x, y, z = x + width // 2 - 1, y + 1, z + length - 1
    elif direction == 'west':
        x, y, z = x, y + 1, z + length // 2 - 1
    elif direction == 'east':
        x, y, z = x + width - 1, y + 1, z + length // 2 - 1
    else:
        return  # Invalid direction

    # Create the 3x3 opening by placing air blocks.
    for i in range(3):
        for j in range(3):
            if direction in ['north', 'south']:
                editor.placeBlock((x + i, y + j, z), Block("air"))
            elif direction in ['west', 'east']:
                editor.placeBlock((x, y + j, z + i), Block("air"))


def place_door(x, y, z, facing, door_type="dark_oak_door"):
    """Places a two-block high door."""
    editor.placeBlock((x, y, z), Block(door_type, {"half": "lower", "facing": facing, "hinge": "left"}))
    editor.placeBlock((x, y + 1, z), Block(door_type, {"half": "upper", "facing": facing, "hinge": "left"}))


def place_stairs(x, y, z, width, length, height, facing, material):
    """
    Places a straight staircase within a module.
    This function's logic is preserved as per the requirements.
    The stair orientation will be consistent throughout the build.
    """
    base_point_x = (width - height) // 2
    base_point_z = (length - height) // 2
    if facing == 'north':
        x_start = x + width // 2
        y_start = y + 1
        z_start = z + base_point_z + height - 2
        for i in range(height - 1):
            for j in range(height - 1):
                editor.placeBlock((x_start, y_start + 1 + j, z_start - i), Block("air"))
            editor.placeBlock((x_start, y_start + i, z_start - i), Block(material, {"half": "bottom", "facing": facing}))
    elif facing == 'south':
        x_start = x + width // 2
        y_start = y + 1
        z_start = z + base_point_z
        for i in range(height - 1):
            for j in range(height - 1):
                editor.placeBlock((x_start, y_start + 1 + j, z_start + i), Block("air"))
            editor.placeBlock((x_start, y_start + i, z_start + i), Block(material, {"half": "bottom", "facing": facing}))
    elif facing == 'west':
        x_start = x + base_point_x + height - 2
        y_start = y + 1
        z_start = z + length // 2
        for i in range(height - 1):
            for j in range(height - 1):
                editor.placeBlock((x_start - i, y_start + 1 + j, z_start), Block("air"))
                editor.placeBlock((x_start - i, y_start + 1 + j, z_start - 1), Block("air"))
                editor.placeBlock((x_start - i, y_start + 1 + j, z_start + 1), Block("air"))
            editor.placeBlock((x_start - i, y_start + i, z_start), Block(material, {"half": "bottom", "facing": facing}))
    elif facing == 'east':
        x_start = x + base_point_x
        y_start = y + 1
        z_start = z + length // 2
        for i in range(height - 1):
            for j in range(height - 1):
                editor.placeBlock((x_start + i, y_start + 1 + j, z_start), Block("air"))
                editor.placeBlock((x_start + i, y_start + 1 + j, z_start - 1), Block("air"))
                editor.placeBlock((x_start + i, y_start + 1 + j, z_start + 1), Block("air"))
            editor.placeBlock((x_start + i, y_start + i, z_start), Block(material, {"half": "bottom", "facing": facing}))

def make_stair_passage_on_floor(x, y, z, width, length, height, direction):
    """
    Clears a path on a floor for a staircase.
    This function's logic is preserved as per the requirements.
    """
    base_point_x = (width - height) // 2
    base_point_z = (length - height) // 2
    if direction == 'north' or direction == 'south':
        x_start = x + width // 2
        z_start = z + base_point_z
        for i in range(height - 1):
            editor.placeBlock((x_start, y, z_start + i), Block("air"))
    elif direction == 'east' or direction == 'west':
        x_start = x + base_point_x
        z_start = z + length // 2
        for i in range(height - 1):
            editor.placeBlock((x_start + i, y, z_start), Block("air"))

# === Custom Helper Functions ===

def place_frame(x, y, z, width, length, height, material):
    """Places the dark_oak_log frame for a module."""
    for i in range(height):
        editor.placeBlock((x, y + i, z), Block(material))
        editor.placeBlock((x + width - 1, y + i, z), Block(material))
        editor.placeBlock((x, y + i, z + length - 1), Block(material))
        editor.placeBlock((x + width - 1, y + i, z + length - 1), Block(material))
    for i in range(width):
        editor.placeBlock((x + i, y + height - 1, z), Block(material))
        editor.placeBlock((x + i, y + height - 1, z + length - 1), Block(material))
    for i in range(length):
        editor.placeBlock((x, y + height - 1, z + i), Block(material))
        editor.placeBlock((x + width - 1, y + height - 1, z + i), Block(material))

def place_windows(x, y, z, width, length, direction):
    """Places a 2x2 window with shutters on a wall."""
    win_y = y + 2
    if direction == 'north':
        win_x, win_z = x + width // 2 - 1, z
        place_wall_section(win_x, win_y, win_z, 2, 2, MATERIALS["windows"], 'north')
        for i in range(2):
            editor.placeBlock((win_x - 1, win_y + i, win_z), Block(MATERIALS["shutters"], {"facing": "west", "open": "true"}))
            editor.placeBlock((win_x + 2, win_y + i, win_z), Block(MATERIALS["shutters"], {"facing": "east", "open": "true"}))
    elif direction == 'south':
        win_x, win_z = x + width // 2 - 1, z + length - 1
        place_wall_section(win_x, win_y, win_z, 2, 2, MATERIALS["windows"], 'south')
        for i in range(2):
            editor.placeBlock((win_x - 1, win_y + i, win_z), Block(MATERIALS["shutters"], {"facing": "west", "open": "true"}))
            editor.placeBlock((win_x + 2, win_y + i, win_z), Block(MATERIALS["shutters"], {"facing": "east", "open": "true"}))
    elif direction == 'west':
        win_x, win_z = x, z + length // 2 - 1
        place_wall_section(win_x, win_y, win_z, 2, 2, MATERIALS["windows"], 'west', length=2)
        for i in range(2):
            editor.placeBlock((win_x, win_y + i, win_z - 1), Block(MATERIALS["shutters"], {"facing": "north", "open": "true"}))
            editor.placeBlock((win_x, win_y + i, win_z + 2), Block(MATERIALS["shutters"], {"facing": "south", "open": "true"}))
    elif direction == 'east':
        win_x, win_z = x + width - 1, z + length // 2 - 1
        place_wall_section(win_x, win_y, win_z, 2, 2, MATERIALS["windows"], 'east', length=2)
        for i in range(2):
            editor.placeBlock((win_x, win_y + i, win_z - 1), Block(MATERIALS["shutters"], {"facing": "north", "open": "true"}))
            editor.placeBlock((win_x, win_y + i, win_z + 2), Block(MATERIALS["shutters"], {"facing": "south", "open": "true"}))

def place_lighting(x, y, z, width, length, height):
    """Places lanterns in the corners of a room for adequate lighting."""
    editor.placeBlock((x + 1, y + height - 2, z + 1), Block("lantern", {"hanging": "true"}))
    editor.placeBlock((x + width - 2, y + height - 2, z + 1), Block("lantern", {"hanging": "true"}))
    editor.placeBlock((x + 1, y + height - 2, z + length - 2), Block("lantern", {"hanging": "true"}))
    editor.placeBlock((x + width - 2, y + height - 2, z + length - 2), Block("lantern", {"hanging": "true"}))
    editor.placeBlock((x + width // 2, y + height - 2, z + length // 2), Block("lantern", {"hanging": "true"}))

# === Module Functions ===

def build_andesite_hearth_commons(x, y, z):  # Module A
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')
    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT)

    # Hearth
    editor.placeBlock((x + 5, y + 1, z + 5), Block("campfire", {"lit": "true"}))
    for i in range(3):
        editor.placeBlock((x + 4 + i, y, z + 4), Block("polished_andesite"))
        editor.placeBlock((x + 4 + i, y, z + 6), Block("polished_andesite"))
    editor.placeBlock((x + 4, y, z + 5), Block("polished_andesite"))
    editor.placeBlock((x + 6, y, z + 5), Block("polished_andesite"))
    for i in range(4):
        editor.placeBlock((x + 5, y + i + 1, z + 4), Block("iron_bars"))
        editor.placeBlock((x + 5, y + i + 1, z + 6), Block("iron_bars"))
    
    # Furniture
    editor.placeBlock((x + 2, y + 1, z + 2), Block("dark_oak_stairs", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("dark_oak_stairs", {"facing": "east"}))
    editor.placeBlock((x + 9, y + 1, z + 8), Block("flower_pot"))
    editor.placeBlock((x + 9, y + 2, z + 8), Block("poppy"))
    for i in range(4):
        editor.placeBlock((x + 2 + i, y + 1, z + 9), Block("white_carpet"))
        editor.placeBlock((x + 9, y + 1, z + 2 + i), Block("white_carpet"))

def build_dark_oak_framed_galley(x, y, z):  # Module B
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT)
    
    # Main entrance door
    place_door(x + ROOM_WIDTH // 2, y + 1, z + ROOM_LENGTH - 1, 'south', MATERIALS["door"])

    # Kitchen furniture
    editor.placeBlock((x + 2, y + 1, z + 2), Block("smoker", {"facing": "south"}))
    editor.placeBlock((x + 3, y + 1, z + 2), Block("furnace", {"facing": "south"}))
    editor.placeBlock((x + 4, y + 1, z + 2), Block("crafting_table"))
    editor.placeBlock((x + 5, y + 1, z + 2), Block("cauldron"))
    for i in range(4):
        editor.placeBlock((x + 2 + i, y + 2, z + 2), Block("dark_oak_trapdoor", {"facing": "south", "half": "bottom"}))
    editor.placeBlock((x + 8, y + 1, z + 2), Block("barrel", {"facing": "up"}))
    editor.placeBlock((x + 9, y + 1, z + 2), Block("barrel", {"facing": "up"}))
    editor.placeBlock((x + 8, y + 2, z + 2), Block("potted_fern"))

    # Flat roof
    for i in range(ROOM_WIDTH):
        for j in range(ROOM_LENGTH):
            editor.placeBlock((x + i, y + ROOM_HEIGHT, z + j), Block(MATERIALS["roof"]))

def build_lantern_lit_reading_nook(x, y, z):  # Module C
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')
    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT)

    # Reading Nook Furniture
    for i in range(5):
        editor.placeBlock((x + 2, y + 1 + i, z + 8), Block("bookshelf"))
        editor.placeBlock((x + 3, y + 1 + i, z + 8), Block("bookshelf"))
    editor.placeBlock((x + 5, y + 1, z + 7), Block("dark_oak_stairs", {"facing": "west"}))
    editor.placeBlock((x + 5, y + 1, z + 6), Block("dark_oak_stairs", {"facing": "west"}))
    editor.placeBlock((x + 4, y + 1, z + 4), Block(MATERIALS["fence"]))
    editor.placeBlock((x + 4, y + 2, z + 4), Block("dark_oak_pressure_plate"))
    editor.placeBlock((x + 4, y + 3, z + 4), Block("lantern"))
    editor.placeBlock((x + 8, y + 1, z + 2), Block("flower_pot"))
    editor.placeBlock((x + 8, y + 2, z + 2), Block("azure_bluet"))
    for i in range(3):
        for j in range(3):
            editor.placeBlock((x + 7 + i, y + 1, z + 7 + j), Block("white_carpet"))

    # Flat roof
    for i in range(ROOM_WIDTH):
        for j in range(ROOM_LENGTH):
            editor.placeBlock((x + i, y + ROOM_HEIGHT, z + j), Block(MATERIALS["roof"]))

def build_vaulted_woolen_bedroom(x, y, z):  # Module D
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')
    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT)

    # Bedroom Furniture
    editor.placeBlock((x + 4, y + 1, z + 2), Block("white_bed", {"part": "foot", "facing": "south"}))
    editor.placeBlock((x + 4, y + 1, z + 3), Block("white_bed", {"part": "head", "facing": "south"}))
    editor.placeBlock((x + 5, y + 1, z + 2), Block("white_bed", {"part": "foot", "facing": "south"}))
    editor.placeBlock((x + 5, y + 1, z + 3), Block("white_bed", {"part": "head", "facing": "south"}))
    editor.placeBlock((x + 3, y + 1, z + 2), Block("dark_oak_planks"))
    editor.placeBlock((x + 3, y + 2, z + 2), Block("dark_oak_trapdoor"))
    editor.placeBlock((x + 8, y + 1, z + 8), Block("chest"))
    editor.placeBlock((x + 9, y + 1, z + 8), Block("chest"))
    editor.placeBlock((x + 2, y + 1, z + 8), Block("barrel"))
    editor.placeBlock((x + 2, y + 1, z + 9), Block("potted_allium"))
    for i in range(4):
        for j in range(4):
            editor.placeBlock((x + 4 + i, y + 1, z + 5 + j), Block("white_carpet"))

def build_deepslate_spire_loft(x, y, z):  # Module E
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')
    place_windows(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')
    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT)

    # Loft Furniture
    editor.placeBlock((x + 2, y + 1, z + 2), Block("cartography_table"))
    editor.placeBlock((x + 3, y + 1, z + 2), Block("loom"))
    editor.placeBlock((x + 4, y + 1, z + 2), Block("grindstone"))
    editor.placeBlock((x + 8, y + 1, z + 8), Block("chest"))
    editor.placeBlock((x + 9, y + 1, z + 8), Block("barrel"))
    editor.placeBlock((x + 8, y + 1, z + 9), Block("gray_shulker_box"))
    editor.placeBlock((x + 5, y + 1, z + 5), Block("dark_oak_slab", {"type": "bottom"}))
    editor.placeBlock((x + 5, y + 1, z + 6), Block("dark_oak_stairs", {"facing": "north"}))

def build_stair_room(x, y, z):  # Module $
    # 1F Stair Room
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT)

    # 2F Stair Room
    place_filled_room(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_frame(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_lighting(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT)

    # Stairs
    place_stairs(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'south', MATERIALS["stair_material"])
    place_stairs(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'south', MATERIALS["stair_material"])

    # Railings
    stair_z = z + (ROOM_LENGTH - ROOM_HEIGHT) // 2
    for i in range(ROOM_HEIGHT - 1):
        editor.placeBlock((x + ROOM_WIDTH // 2 - 1, y + 1, z + stair_z + i), Block(MATERIALS["fence"]))
        editor.placeBlock((x + ROOM_WIDTH // 2 + 1, y + 1, z + stair_z + i), Block(MATERIALS["fence"]))
        editor.placeBlock((x + ROOM_WIDTH // 2 - 1, y + ROOM_HEIGHT + 1, z + stair_z + i), Block(MATERIALS["fence"]))
        editor.placeBlock((x + ROOM_WIDTH // 2 + 1, y + ROOM_HEIGHT + 1, z + stair_z + i), Block(MATERIALS["fence"]))

def build_end_stair_room(x, y, z):  # Module @
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT)

    # Create opening for stairs from below
    make_stair_passage_on_floor(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'south')

    # Railings
    stair_z = z + (ROOM_LENGTH - ROOM_HEIGHT) // 2
    for i in range(ROOM_HEIGHT - 1):
        editor.placeBlock((x + ROOM_WIDTH // 2 - 1, y + 1, z + stair_z + i), Block(MATERIALS["fence"]))
        editor.placeBlock((x + ROOM_WIDTH // 2 + 1, y + 1, z + stair_z + i), Block(MATERIALS["fence"]))
    for i in range(3):
        editor.placeBlock((x + ROOM_WIDTH // 2 - 1 + i, y + 1, z + stair_z - 1), Block(MATERIALS["fence"]))

def build_conical_roof(x, y, z, width, length):
    """Builds the main conical roof over the top floor."""
    roof_height = max(width, length) // 2
    for i in range(roof_height + 1):
        # Current layer dimensions
        curr_width = width - 2 * i
        curr_length = length - 2 * i
        
        if curr_width <= 0 or curr_length <= 0:
            break

        # Place solid roof base
        for ix in range(curr_width):
            for iz in range(curr_length):
                editor.placeBlock((x + i + ix, y + i, z + i + iz), Block(MATERIALS["roof"]))

        # Place stair outline for smoother look
        if curr_width > 2 and curr_length > 2:
            for ix in range(curr_width):
                editor.placeBlock((x + i + ix, y + i, z + i), Block(MATERIALS["roof_stairs"], {"facing": "north"}))
                editor.placeBlock((x + i + ix, y + i, z + i + curr_length - 1), Block(MATERIALS["roof_stairs"], {"facing": "south"}))
            for iz in range(1, curr_length - 1):
                editor.placeBlock((x + i, y + i, z + i + iz), Block(MATERIALS["roof_stairs"], {"facing": "west"}))
                editor.placeBlock((x + i + curr_width - 1, y + i, z + i + iz), Block(MATERIALS["roof_stairs"], {"facing": "east"}))

# === Master Build Function ===
def build_shepherds_spire(x, y, z):
    """Constructs the entire house by calling the module functions based on the layout."""
    # 1F Layout
    # ΦAΦ
    # B$C
    build_andesite_hearth_commons(x + ROOM_WIDTH, y, z)
    build_dark_oak_framed_galley(x, y, z + ROOM_LENGTH)
    build_lantern_lit_reading_nook(x + 2 * ROOM_WIDTH, y, z + ROOM_LENGTH)
    
    # 2F Layout
    # ΦDΦ
    build_vaulted_woolen_bedroom(x + ROOM_WIDTH, y + ROOM_HEIGHT, z)
    
    # 3F Layout
    # ΦEΦ
    # Φ@Φ
    build_deepslate_spire_loft(x + ROOM_WIDTH, y + 2 * ROOM_HEIGHT, z)
    build_end_stair_room(x + ROOM_WIDTH, y + 2 * ROOM_HEIGHT, z + ROOM_LENGTH)

    # Stairwell connecting all floors
    build_stair_room(x + ROOM_WIDTH, y, z + ROOM_LENGTH)

    # Main conical roof for the spire
    roof_base_y = y + 3 * ROOM_HEIGHT
    build_conical_roof(x + ROOM_WIDTH, roof_base_y, z, ROOM_WIDTH, 2 * ROOM_LENGTH)

    print(f"Shepherd's Spire construction initiated at ({x}, {y}, {z}).")

# === Main Execution Block ===
if __name__ == '__main__':
    try:
        start_x, start_y, start_z = 14000, -60, -261

        # Call the master function to build the entire house.
        build_shepherds_spire(start_x, start_y, start_z)

        # Flush the buffer to apply all the changes to the world.
        editor.flushBuffer()
        print("Build complete! Your Shepherd's Spire is ready.")

    except Exception as e:
        print(f"An error occurred during the build process: {e}")
        if "flushBuffer" in dir(editor):
            editor.flushBuffer()