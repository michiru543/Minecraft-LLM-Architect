from gdpc import Editor, Block
import random

# It is recommended to use buffering, especially for larger structures.
editor = Editor(buffering=True)

# === Constants ===
# Define the dimensions for each modular room of the house.
ROOM_WIDTH = 12
ROOM_LENGTH = 12
ROOM_HEIGHT = 6

# Define building materials based on the provided JSON for easy access and modification.
MATERIALS = {
    "foundation_primary": "stone_bricks",
    "foundation_secondary": "mossy_stone_bricks",
    "frame": "dark_oak_log",
    "walls": "spruce_planks",
    "roof_block": "deepslate_tiles",
    "roof_stairs": "deepslate_tile_stairs",
    "flooring": "oak_planks",
    "ceiling": "oak_planks",
    "door": "dark_oak_door",
    "fence": "spruce_fence",
    "lantern": "lantern",
    "chain": "chain",
    "stair_material": "dark_oak_stairs"
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
            editor.placeBlock((x_start + 1, y_start + i, z_start - i), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - 1, y_start + i, z_start - i), Block("light_gray_stained_glass_pane"))
    elif facing == 'south':
        x_start = x + width // 2
        y_start = y + 1
        z_start = z + base_point_z
        for i in range(height - 1):
            for j in range(height - 1):
                editor.placeBlock((x_start, y_start + 1 + j, z_start + i), Block("air"))
            editor.placeBlock((x_start, y_start + i, z_start + i), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start + 1, y_start + i, z_start + i), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - 1, y_start + i, z_start + i), Block("light_gray_stained_glass_pane"))
    elif facing == 'west':
        x_start = x + base_point_x + height - 2
        y_start = y + 1
        z_start = z + length // 2
        for i in range(height - 1):
            for j in range(height - 1):
                editor.placeBlock((x_start - i, y_start + 1 + j, z_start), Block("air"))
            editor.placeBlock((x_start - i, y_start + i, z_start), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start - i, y_start + i, z_start + 1), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - i, y_start + i, z_start - 1), Block("light_gray_stained_glass_pane"))
    elif facing == 'east':
        x_start = x + base_point_x
        y_start = y + 1
        z_start = z + length // 2
        for i in range(height - 1):
            for j in range(height - 1):
                editor.placeBlock((x_start + i, y_start + 1 + j, z_start), Block("air"))
            editor.placeBlock((x_start + i, y_start + i, z_start), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start + i, y_start + i, z_start + 1), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start + i, y_start + i, z_start - 1), Block("light_gray_stained_glass_pane"))

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

# === New Utility Functions ===

def place_foundation(x, y, z, width, length, material1, material2):
    """Places a 1-block high foundation with mixed materials."""
    for ix in range(width):
        for iz in range(length):
            material = material1 if random.random() > 0.2 else material2
            editor.placeBlock((x + ix, y - 1, z + iz), Block(material))

def place_log_frame(x, y, z, width, length, height, material):
    """Constructs a log frame around a room module."""
    # Vertical pillars
    for iy in range(height):
        editor.placeBlock((x, y + iy, z), Block(material))
        editor.placeBlock((x + width - 1, y + iy, z), Block(material))
        editor.placeBlock((x, y + iy, z + length - 1), Block(material))
        editor.placeBlock((x + width - 1, y + iy, z + length - 1), Block(material))
    # Horizontal beams
    for ix in range(width):
        editor.placeBlock((x + ix, y + height - 1, z), Block(material))
        editor.placeBlock((x + ix, y + height - 1, z + length - 1), Block(material))
    for iz in range(length):
        editor.placeBlock((x, y + height - 1, z + iz), Block(material))
        editor.placeBlock((x + width - 1, y + height - 1, z + iz), Block(material))

def place_sloped_roof(x, y, z, width, length, block_material, stairs_material):
    """Builds a solid, A-frame roof on top of a module."""
    roof_height = width // 2
    # Build the solid triangular prism structure
    for i in range(roof_height):
        start_x = x + i
        end_x = x + width - i
        for ix in range(start_x, end_x):
            for iz in range(z, z + length):
                editor.placeBlock((ix, y + i, iz), Block(block_material))

    # Cover the slopes with stairs
    for i in range(roof_height):
        for k in range(-1, length + 1): # Overhang
            editor.placeBlock((x + width - i, y + i, z + k), Block(stairs_material, {"facing": "west"}))
            editor.placeBlock((x - 1 + i, y + i, z + k), Block(stairs_material, {"facing": "east"}))

def replace_stair_railing(x, y, z, width, length, height, facing, new_material):
    """Replaces the default stair railing with a specified material."""
    base_point_z = (length - height) // 2
    if facing == 'north':
        x_start = x + width // 2
        y_start = y + 1
        z_start = z + base_point_z + height - 2
        for i in range(height - 1):
            editor.placeBlock((x_start + 1, y_start + i, z_start - i), Block(new_material))
            editor.placeBlock((x_start - 1, y_start + i, z_start - i), Block(new_material))

# === Module Functions ===

def build_dark_oak_hearth_hall(x, y, z):  # Module A
    """Builds the Dark Oak Hearth Hall (1F, Southeast)."""
    place_foundation(x, y, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["foundation_primary"], MATERIALS["foundation_secondary"])
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_log_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    
    # Entrances
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')  # To stair_room
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north') # To Oak Plank Dining Room
    place_door(x + ROOM_WIDTH // 2, y + 1, z + ROOM_LENGTH - 1, 'south', MATERIALS["door"]) # Main entrance

    # Hearth
    for i in range(4):
        editor.placeBlock((x + 2 + i, y + 1, z + 2), Block("stone_bricks"))
    editor.placeBlock((x + 3, y + 1, z + 2), Block("campfire"))
    for i in range(4):
        editor.placeBlock((x + 2 + i, y + 2, z + 2), Block("iron_bars"))

    # Furniture
    editor.placeBlock((x + 7, y + 1, z + 4), Block("dark_oak_stairs", {"facing": "west"}))
    editor.placeBlock((x + 7, y + 1, z + 5), Block("dark_oak_stairs", {"facing": "west"}))
    editor.placeBlock((x + 7, y + 1, z + 6), Block("dark_oak_stairs", {"facing": "west"}))
    editor.placeBlock((x + 2, y + 1, z + ROOM_LENGTH - 3), Block("bookshelf"))
    editor.placeBlock((x + 2, y + 2, z + ROOM_LENGTH - 3), Block("bookshelf"))
    
    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))

    # Roof
    place_sloped_roof(x, y + ROOM_HEIGHT - 1, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_block"], MATERIALS["roof_stairs"])

def build_deepslate_tile_kitchen(x, y, z):  # Module B
    """Builds the Deepslate Tile Kitchen (1F, North)."""
    place_foundation(x, y, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["foundation_primary"], MATERIALS["foundation_secondary"])
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_log_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])

    # Entrances
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')  # To Oak Plank Dining Room
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')  # To Mossy Stone Study
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south') # To stair_room

    # Counters and Appliances
    for i in range(5):
        editor.placeBlock((x + 2, y + 1, z + 2 + i), Block("polished_deepslate"))
    editor.placeBlock((x + 2, y + 1, z + 2), Block("blast_furnace", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("smoker", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 6), Block("cauldron"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 2), Block("crafting_table"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 3), Block("barrel", {"facing": "up"}))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))

def build_spruce_and_slate_master_suite(x, y, z):  # Module C
    """Builds the Spruce and Slate Master Suite (2F, North)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "spruce_planks")
    place_log_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])

    # Entrances
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')  # To Lantern-Lit Loft
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south') # To end_stair_room

    # Bed
    editor.placeBlock((x + 2, y + 1, z + 3), Block("brown_bed", {"part": "foot", "facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 2), Block("brown_bed", {"part": "head", "facing": "east"}))
    
    # Furniture
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 2), Block("chest"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 3), Block("chest"))
    editor.placeBlock((x + 2, y + 1, z + ROOM_LENGTH - 3), Block("barrel"))
    for i in range(3):
        for j in range(3):
            editor.placeBlock((x + 5 + i, y + 1, z + 5 + j), Block("gray_carpet"))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))

    # Roof
    place_sloped_roof(x, y + ROOM_HEIGHT - 1, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_block"], MATERIALS["roof_stairs"])

def build_mossy_stone_study(x, y, z):  # Module D
    """Builds the Mossy Stone Study (1F, Northwest)."""
    place_foundation(x, y, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["foundation_primary"], MATERIALS["foundation_secondary"])
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_log_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])

    # Entrance
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')  # To Deepslate Tile Kitchen

    # Furniture
    for i in range(4):
        editor.placeBlock((x + 2, y + 1 + i, z + 2), Block("bookshelf"))
        editor.placeBlock((x + 2, y + 1 + i, z + 3), Block("bookshelf"))
    editor.placeBlock((x + 4, y + 1, z + 2), Block("lectern", {"facing": "east"}))
    editor.placeBlock((x + 5, y + 1, z + 2), Block("dark_oak_stairs", {"facing": "west"}))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + ROOM_LENGTH - 3), Block("cartography_table"))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))

    # Roof
    place_sloped_roof(x, y + ROOM_HEIGHT - 1, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_block"], MATERIALS["roof_stairs"])

def build_oak_plank_dining_room(x, y, z):  # Module E
    """Builds the Oak Plank Dining Room (1F, Northeast)."""
    place_foundation(x, y, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["foundation_primary"], MATERIALS["foundation_secondary"])
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_log_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])

    # Entrances
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')  # To Deepslate Tile Kitchen
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south') # To Dark Oak Hearth Hall

    # Dining Table
    for i in range(4):
        editor.placeBlock((x + 4 + i, y + 1, z + 5), Block("oak_trapdoor", {"facing": "north", "half": "top"}))
    editor.placeBlock((x + 4, y + 1, z + 4), Block(MATERIALS["fence"]))
    editor.placeBlock((x + 7, y + 1, z + 4), Block(MATERIALS["fence"]))
    
    # Chairs
    editor.placeBlock((x + 4, y + 1, z + 6), Block("oak_stairs", {"facing": "north"}))
    editor.placeBlock((x + 5, y + 1, z + 6), Block("oak_stairs", {"facing": "north"}))
    editor.placeBlock((x + 6, y + 1, z + 6), Block("oak_stairs", {"facing": "north"}))
    editor.placeBlock((x + 7, y + 1, z + 6), Block("oak_stairs", {"facing": "north"}))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))

def build_lantern_lit_loft(x, y, z):  # Module F
    """Builds the Lantern-Lit Loft (2F, Northeast)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "spruce_planks")
    place_log_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])

    # Entrance
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')  # To Spruce and Slate Master Suite

    # Furniture
    editor.placeBlock((x + 2, y + 1, z + 2), Block("hay_block"))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("hay_block"))
    editor.placeBlock((x + 3, y + 1, z + 2), Block("hay_block"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 2), Block("loom"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + ROOM_LENGTH - 3), Block("chest"))
    editor.placeBlock((x + 2, y + 1, z + ROOM_LENGTH - 3), Block("spruce_stairs", {"facing": "east"}))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))

    # Roof
    place_sloped_roof(x, y + ROOM_HEIGHT - 1, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_block"], MATERIALS["roof_stairs"])

def build_stair_room(x, y, z):  # Module $
    """Builds the stair room connecting floors 1 and 2."""
    place_foundation(x, y, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["foundation_primary"], MATERIALS["foundation_secondary"])
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["ceiling"])
    place_log_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])

    # Entrances
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')  # To Dark Oak Hearth Hall
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north') # To Deepslate Tile Kitchen

    # Build stairs from Floor 1 to Floor 2, facing North
    place_stairs(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'north', MATERIALS["stair_material"])
    replace_stair_railing(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'north', MATERIALS["fence"])

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block("wall_torch", {"facing": "south"}))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block("wall_torch", {"facing": "south"}))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("wall_torch", {"facing": "north"}))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block("wall_torch", {"facing": "north"}))

def build_end_stair_room(x, y, z):  # Module @
    """Builds the landing for the top floor."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], "spruce_planks")
    place_log_frame(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])

    # Entrance
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')  # To Spruce and Slate Master Suite

    # Create hole for the stairs from below
    make_stair_passage_on_floor(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'north')
    # Replace default railing with fences
    base_point_z = (ROOM_LENGTH - ROOM_HEIGHT) // 2
    x_start = x + ROOM_WIDTH // 2
    z_start = z + base_point_z
    for i in range(ROOM_HEIGHT - 1):
        editor.placeBlock((x_start + 1, y + 1, z_start + i), Block(MATERIALS["fence"]))
        editor.placeBlock((x_start - 1, y + 1, z_start + i), Block(MATERIALS["fence"]))

    # Lighting
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + 1), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + 1, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 2), Block(MATERIALS["lantern"]))

    # Roof
    place_sloped_roof(x, y + ROOM_HEIGHT - 1, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof_block"], MATERIALS["roof_stairs"])

# === Master Build Function ===
def build_woodland_lodge(x, y, z):
    """Constructs the entire house by calling the module functions based on the layout."""
    # Floor 1 Layout
    # DBE
    # Φ$A
    build_mossy_stone_study(x, y, z)
    build_deepslate_tile_kitchen(x + ROOM_WIDTH, y, z)
    build_oak_plank_dining_room(x + 2 * ROOM_WIDTH, y, z)
    build_stair_room(x + ROOM_WIDTH, y, z + ROOM_LENGTH)
    build_dark_oak_hearth_hall(x + 2 * ROOM_WIDTH, y, z + ROOM_LENGTH)

    # Floor 2 Layout
    # ΦCF
    # Φ@Φ
    build_spruce_and_slate_master_suite(x + ROOM_WIDTH, y + ROOM_HEIGHT, z)
    build_lantern_lit_loft(x + 2 * ROOM_WIDTH, y + ROOM_HEIGHT, z)
    build_end_stair_room(x + ROOM_WIDTH, y + ROOM_HEIGHT, z + ROOM_LENGTH)

    print(f"Rustic woodland lodge construction initiated at ({x}, {y}, {z}).")


# === Main Execution Block ===
if __name__ == '__main__':
    try:
        start_x, start_y, start_z = 16000, -60, -261

        # Call the master function to build the entire house.
        build_woodland_lodge(start_x, start_y, start_z)

        # Flush the buffer to apply all the changes to the world.
        editor.flushBuffer()
        print("Build complete! Your rustic woodland lodge is ready.")

    except Exception as e:
        print(f"An error occurred during the build process: {e}")
        # It's good practice to still flush the buffer to see partial results
        if "flushBuffer" in dir(editor):
            editor.flushBuffer()