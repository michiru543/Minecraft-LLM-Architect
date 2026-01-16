from gdpc import Editor, Block

# It is recommended to use buffering, especially for larger structures.
editor = Editor(buffering=True)

# === Constants ===
# Define the dimensions for each modular room of the house.
# Adjusting these will change the scale of the entire building.
ROOM_WIDTH = 12
ROOM_LENGTH = 12
ROOM_HEIGHT = 6

# Define building materials based on the provided JSON for easy access and modification.
MATERIALS = {
    "foundation": "cobbled_deepslate",
    "walls": "stone_bricks",
    "roof_stairs": "dark_oak_stairs",
    "roof_beams": "stripped_spruce_log",
    "flooring": "spruce_planks",
    "stair_material": "spruce_stairs",
    "door": "dark_oak_door"
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
            editor.placeBlock((x_start + 1, y_start, z_start - i), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - 1, y_start, z_start - i), Block("light_gray_stained_glass_pane"))
    elif facing == 'south':
        x_start = x + width // 2
        y_start = y + 1
        z_start = z + base_point_z
        for i in range(height - 1):
            for j in range(height - 1):
                editor.placeBlock((x_start, y_start + 1 + j, z_start + i), Block("air"))
            editor.placeBlock((x_start, y_start + i, z_start + i), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start + 1, y_start, z_start + i), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - 1, y_start, z_start + i), Block("light_gray_stained_glass_pane"))
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
            editor.placeBlock((x_start - i, y_start, z_start + 1), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - i, y_start, z_start - 1), Block("light_gray_stained_glass_pane"))
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
            editor.placeBlock((x_start + i, y_start, z_start + 1), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start + i, y_start, z_start - 1), Block("light_gray_stained_glass_pane"))

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
            editor.placeBlock((x_start + 1, y + 1, z_start + i), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - 1, y + 1, z_start + i), Block("light_gray_stained_glass_pane"))
    elif direction == 'east' or direction == 'west':
        x_start = x + base_point_x
        z_start = z + length // 2
        for i in range(height - 1):
            editor.placeBlock((x_start + i, y, z_start), Block("air"))
            editor.placeBlock((x_start + i, y + 1, z_start + 1), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start + i, y + 1, z_start - 1), Block("light_gray_stained_glass_pane"))

def place_roof(x, y, z, width, length, material_stairs, material_beams):
    """Builds a solid, pitched roof on top of a module."""
    gable_height = width // 2
    # Place gables (solid walls at the ends)
    for i in range(gable_height):
        for j in range(i, width - i):
            editor.placeBlock((x + j, y + i, z), Block(MATERIALS["walls"]))
            editor.placeBlock((x + j, y + i, z + length - 1), Block(MATERIALS["walls"]))

    # Place the roof stairs
    for i in range(gable_height):
        for j in range(length):
            editor.placeBlock((x + i, y + i, z + j), Block(material_stairs, {"facing": "east", "half": "bottom"}))
            editor.placeBlock((x + width - 1 - i, y + i, z + j), Block(material_stairs, {"facing": "west", "half": "bottom"}))

    # Fill the peak of the roof to ensure it is solid
    if width % 2 == 0:
        for j in range(length):
            editor.placeBlock((x + gable_height - 1, y + gable_height - 1, z + j), Block(material_stairs, {"facing": "east", "half": "top"}))
            editor.placeBlock((x + gable_height, y + gable_height - 1, z + j), Block(material_stairs, {"facing": "west", "half": "top"}))
    else:
        for j in range(length):
            editor.placeBlock((x + gable_height, y + gable_height, z + j), Block(material_beams))

# === Module Functions ===

def build_greatroom_A(x, y, z):
    """Builds the Stone & Spruce Greatroom (1F, West)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "spruce_planks")
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_door(x + ROOM_WIDTH // 2, y + 1, z + ROOM_LENGTH - 1, 'south', MATERIALS["door"])

    # Fireplace
    for i in range(4):
        editor.placeBlock((x + 1, y + 1 + i, z + 4), Block("stone_bricks"))
        editor.placeBlock((x + 1, y + 1 + i, z + 7), Block("stone_bricks"))
    for i in range(2):
        editor.placeBlock((x + 1, y + 1, z + 5 + i), Block("stone_bricks"))
        editor.placeBlock((x + 1, y + 4, z + 5 + i), Block("stone_brick_stairs", {"facing": "west"}))
    editor.placeBlock((x + 1, y + 1, z + 5), Block("campfire"))
    editor.placeBlock((x + 2, y + 1, z + 5), Block("air"))

    # Seating area
    for i in range(4):
        editor.placeBlock((x + 5, y + 1, z + 4 + i), Block("spruce_stairs", {"facing": "west"}))
    for i in range(3):
        for j in range(4):
            editor.placeBlock((x + 6 + i, y + 1, z + 4 + j), Block("gray_carpet"))

    # Decoration
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 2), Block("bookshelf"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 2, z + 2), Block("bookshelf"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 3), Block("barrel", {"facing": "up"}))
    editor.placeBlock((x + 2, y + 1, z + 2), Block("flower_pot"))
    editor.placeBlock((x + 2, y + 2, z + 2), Block("fern"))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block("chain"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 3, z + 1), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block("chain"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 3, z + 1), Block("lantern"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("chain"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 3, z + ROOM_LENGTH - 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("chain"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 3, z + ROOM_LENGTH - 2), Block("lantern"))

def build_master_chamber_B(x, y, z):
    """Builds the Deepslate Master Chamber (1F, East)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "stripped_spruce_log")
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')

    # Bed area
    editor.placeBlock((x + 4, y + 1, z + 2), Block("gray_bed", {"part": "head", "facing": "south"}))
    editor.placeBlock((x + 4, y + 1, z + 3), Block("gray_bed", {"part": "foot", "facing": "south"}))
    editor.placeBlock((x + 5, y + 1, z + 2), Block("gray_bed", {"part": "head", "facing": "south"}))
    editor.placeBlock((x + 5, y + 1, z + 3), Block("gray_bed", {"part": "foot", "facing": "south"}))
    for i in range(4):
        editor.placeBlock((x + 3 + i, y + 1, z + 1), Block("polished_deepslate"))
    for i in range(6):
        for j in range(5):
            editor.placeBlock((x + 3 + i, y + 1, z + 2 + j), Block("black_carpet"))

    # Storage
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 5), Block("chest"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 6), Block("ender_chest"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 7), Block("chest"))

    # Lighting
    editor.placeBlock((x + 1, y + 1, z + 1), Block("soul_lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 1), Block("soul_lantern"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("chain"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 3, z + ROOM_LENGTH - 2), Block("soul_lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("chain"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 3, z + ROOM_LENGTH - 2), Block("soul_lantern"))

    place_roof(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_stairs"], MATERIALS["roof_beams"])

def build_kitchen_C(x, y, z):
    """Builds the Stone Hearth Kitchen (1F, North)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "spruce_planks")
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')

    # Counters
    for i in range(5):
        editor.placeBlock((x + 2, y + 1, z + 2 + i), Block("polished_andesite"))
        editor.placeBlock((x + 2, y + 2, z + 2 + i), Block("iron_trapdoor"))
    for i in range(4):
        editor.placeBlock((x + 3 + i, y + 1, z + 2), Block("polished_andesite"))
        editor.placeBlock((x + 3 + i, y + 2, z + 2), Block("iron_trapdoor"))

    # Appliances
    editor.placeBlock((x + 2, y + 1, z + 2), Block("blast_furnace", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("furnace", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 4), Block("smoker", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 6), Block("cauldron"))
    editor.placeBlock((x + 1, y + 2, z + 6), Block("tripwire_hook", {"facing": "east"}))
    editor.placeBlock((x + 6, y + 1, z + 2), Block("crafting_table"))

    # Storage
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 2), Block("barrel", {"facing": "up"}))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 2, z + 2), Block("barrel", {"facing": "up"}))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 3), Block("composter"))

    # Lighting
    editor.placeBlock((x + 1, y + 1, z + 1), Block("torch"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 1), Block("torch"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("torch"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("torch"))

def build_stair_room_dollar(x, y, z):
    """Builds the stair_room (1F, Center)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "spruce_planks")
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')

    # Place stairs going up to the second floor
    place_stairs(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'north', MATERIALS["stair_material"])

    # Support pillars
    editor.placeBlock((x + 2, y + 1, z + 2), Block("stripped_spruce_log"))
    editor.placeBlock((x + 2, y + 2, z + 2), Block("stripped_spruce_log"))
    editor.placeBlock((x + 2, y + 3, z + 2), Block("stone_brick_wall"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 2), Block("stripped_spruce_log"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 2, z + 2), Block("stripped_spruce_log"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 3, z + 2), Block("stone_brick_wall"))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block("torch"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block("torch"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("torch"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("torch"))

def build_refectory_D(x, y, z):
    """Builds the Exposed Beam Refectory (2F, West)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "stripped_spruce_log")
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')

    # Dining Table
    for i in range(6):
        editor.placeBlock((x + 3 + i, y + 1, z + 5), Block("dark_oak_trapdoor", {"half": "top"}))
        editor.placeBlock((x + 3 + i, y + 1, z + 6), Block("dark_oak_trapdoor", {"half": "top"}))
        editor.placeBlock((x + 3 + i, y + 1, z + 4), Block("dark_oak_stairs", {"facing": "south"}))
        editor.placeBlock((x + 3 + i, y + 1, z + 7), Block("dark_oak_stairs", {"facing": "north"}))
    editor.placeBlock((x + 3, y + 1, z + 5), Block("spruce_fence"))
    editor.placeBlock((x + 3, y + 1, z + 6), Block("spruce_fence"))
    editor.placeBlock((x + 8, y + 1, z + 5), Block("spruce_fence"))
    editor.placeBlock((x + 8, y + 1, z + 6), Block("spruce_fence"))

    # Decoration
    editor.placeBlock((x + 2, y + 1, z + 2), Block("potted_azalea_bush"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 2), Block("potted_azalea_bush"))

    # Lighting
    editor.placeBlock((x + 5, y + 2, z + 5), Block("candle"))
    editor.placeBlock((x + 6, y + 2, z + 6), Block("candle"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block("lantern"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("lantern"))

    place_roof(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_stairs"], MATERIALS["roof_beams"])

def build_scriptorium_E(x, y, z):
    """Builds the Mossy Stone Scriptorium (2F, North)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "stripped_spruce_log")
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')

    # Bookshelves
    for i in range(ROOM_LENGTH - 4):
        editor.placeBlock((x + 1, y + 1, z + 2 + i), Block("bookshelf"))
        editor.placeBlock((x + 1, y + 2, z + 2 + i), Block("bookshelf"))
        editor.placeBlock((x + 1, y + 3, z + 2 + i), Block("bookshelf"))
    for i in range(ROOM_WIDTH - 4):
        editor.placeBlock((x + 2 + i, y + 1, z + 1), Block("bookshelf"))
        editor.placeBlock((x + 2 + i, y + 2, z + 1), Block("bookshelf"))

    # Study Area
    editor.placeBlock((x + 5, y + 1, z + 5), Block("lectern", {"facing": "north"}))
    editor.placeBlock((x + 7, y + 1, z + 5), Block("cartography_table"))
    editor.placeBlock((x + 6, y + 1, z + 6), Block("mossy_stone_brick_stairs", {"facing": "south"}))
    for i in range(4):
        for j in range(4):
            editor.placeBlock((x + 5 + i, y + 1, z + 5 + j), Block("moss_carpet"))

    # Lighting
    editor.placeBlock((x + 1, y + 1, z + 1), Block("soul_lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 1), Block("soul_lantern"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("soul_lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("soul_lantern"))

    place_roof(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_stairs"], MATERIALS["roof_beams"])

def build_end_stair_room_at(x, y, z):
    """Builds the end_stair_room (2F, Center)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "stripped_spruce_log")
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')

    # Create opening for stairs from below
    make_stair_passage_on_floor(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'north')

    # Add stone railings to match materials list
    x_start = x + ROOM_WIDTH // 2
    z_start = z + (ROOM_LENGTH - ROOM_HEIGHT) // 2
    for i in range(ROOM_HEIGHT - 1):
        editor.placeBlock((x_start + 1, y + 1, z_start + i), Block("stone_brick_wall"))
        editor.placeBlock((x_start - 1, y + 1, z_start + i), Block("stone_brick_wall"))
    editor.placeBlock((x_start, y + 1, z_start - 1), Block("stone_brick_wall"))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block("lantern"))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("lantern"))

    place_roof(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_stairs"], MATERIALS["roof_beams"])

# === Master Build Function ===
def build_stone_house(x, y, z):
    """Constructs the entire house by calling the module functions based on the layout."""
    # Floor 1 Layout
    # ΦCΦ
    # A$B
    # ΦΦΦ
    build_kitchen_C(x + 1 * ROOM_WIDTH, y, z)
    build_greatroom_A(x, y, z + 1 * ROOM_LENGTH)
    build_stair_room_dollar(x + 1 * ROOM_WIDTH, y, z + 1 * ROOM_LENGTH)
    build_master_chamber_B(x + 2 * ROOM_WIDTH, y, z + 1 * ROOM_LENGTH)

    # Floor 2 Layout
    # ΦEΦ
    # D@Φ
    # ΦΦΦ
    build_scriptorium_E(x + 1 * ROOM_WIDTH, y + 1 * ROOM_HEIGHT, z)
    build_refectory_D(x, y + 1 * ROOM_HEIGHT, z + 1 * ROOM_LENGTH)
    build_end_stair_room_at(x + 1 * ROOM_WIDTH, y + 1 * ROOM_HEIGHT, z + 1 * ROOM_LENGTH)

    print(f"Stone house construction initiated at ({x}, {y}, {z}).")


# === Main Execution Block ===
if __name__ == '__main__':
    try:
        start_x, start_y, start_z = 18000, -60, -261

        # Call the master function to build the entire house.
        build_stone_house(start_x, start_y, start_z)

        # Flush the buffer to apply all the changes to the world.
        editor.flushBuffer()
        print("Build complete! Your stone house is ready.")

    except Exception as e:
        print(f"An error occurred during the build process: {e}")
        if "flushBuffer" in dir(editor):
            editor.flushBuffer()