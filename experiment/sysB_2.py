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
    "foundation": "polished_diorite",
    "frame": "quartz_pillar",
    "walls": "white_concrete",
    "roof": "light_gray_stained_glass",
    "flooring": "smooth_quartz",
    "doors": "birch_door",
    "staircase_block": "birch_planks",
    "staircase_stairs": "birch_stairs",
    "lighting": "sea_lantern"
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

def place_framing(x, y, z, width, length, height, material):
    """Places framing pillars at the corners of a room."""
    for i in range(height):
        editor.placeBlock((x, y + i, z), Block(material))
        editor.placeBlock((x + width - 1, y + i, z), Block(material))
        editor.placeBlock((x, y + i, z + length - 1), Block(material))
        editor.placeBlock((x + width - 1, y + i, z + length - 1), Block(material))

def place_lighting(x, y, z, width, length, height, material):
    """Places lighting fixtures in the corners of a room."""
    # Floor lighting
    editor.placeBlock((x + 1, y + 1, z + 1), Block(material))
    editor.placeBlock((x + width - 2, y + 1, z + 1), Block(material))
    editor.placeBlock((x + 1, y + 1, z + length - 2), Block(material))
    editor.placeBlock((x + width - 2, y + 1, z + length - 2), Block(material))
    # Ceiling lighting
    editor.placeBlock((x + width // 2, y + height - 2, z + length // 2), Block(material))

def place_roof(x, y, z, width, length, material):
    """Places a flat roof on top of a module."""
    for i in range(width):
        for j in range(length):
            editor.placeBlock((x + i, y, z + j), Block(material))

# === Module Functions ===

def build_radiant_quartz_atrium(x, y, z):  # Module A
    """Builds the Radiant Quartz Atrium (1F, North)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["foundation"], MATERIALS["flooring"])
    place_framing(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')
    place_door(x + ROOM_WIDTH // 2, y + 1, z, 'north', MATERIALS["doors"])

    # Furniture: Central seating area
    for i in range(4):
        for j in range(4):
            editor.placeBlock((x + 4 + i, y + 1, z + 4 + j), Block("white_carpet"))
    editor.placeBlock((x + 5, y + 1, z + 5), Block("smooth_quartz_slab", {"type": "bottom"}))
    editor.placeBlock((x + 6, y + 1, z + 5), Block("smooth_quartz_slab", {"type": "bottom"}))
    editor.placeBlock((x + 5, y + 1, z + 6), Block("smooth_quartz_slab", {"type": "bottom"}))
    editor.placeBlock((x + 6, y + 1, z + 6), Block("smooth_quartz_slab", {"type": "bottom"}))
    editor.placeBlock((x + 5, y + 2, z + 5), Block("flower_pot"))
    editor.placeBlock((x + 5, y + 3, z + 5), Block("azalea"))

    # Side tables with trapdoors
    editor.placeBlock((x + 2, y + 1, z + 2), Block("smooth_quartz_stairs", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("birch_trapdoor", {"facing": "north", "half": "top"}))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 2), Block("smooth_quartz_stairs", {"facing": "west"}))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 3), Block("birch_trapdoor", {"facing": "north", "half": "top"}))

    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["lighting"])

def build_sun_drenched_great_room(x, y, z):  # Module B
    """Builds the Sun-Drenched Great Room (1F, West)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["foundation"], MATERIALS["roof"])
    place_framing(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_roof(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof"])

    # Furniture: Bookshelf wall
    for i in range(ROOM_LENGTH - 2):
        for j in range(ROOM_HEIGHT - 2):
            editor.placeBlock((x + 1, y + 1 + j, z + 1 + i), Block("bookshelf"))
    
    # Furniture: Sofa and table
    for i in range(4):
        editor.placeBlock((x + 5, y + 1, z + 4 + i), Block("smooth_quartz_stairs", {"facing": "west"}))
    editor.placeBlock((x + 6, y + 1, z + 3), Block("smooth_quartz_stairs", {"facing": "south"}))
    editor.placeBlock((x + 6, y + 1, z + 8), Block("smooth_quartz_stairs", {"facing": "north"}))
    editor.placeBlock((x + 7, y + 1, z + 5), Block("birch_slab", {"type": "bottom"}))
    editor.placeBlock((x + 7, y + 1, z + 6), Block("birch_slab", {"type": "bottom"}))

    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["lighting"])

def build_minimalist_birch_kitchen(x, y, z):  # Module C
    """Builds the Minimalist Birch Kitchen (1F, East)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["foundation"], MATERIALS["roof"])
    place_framing(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')
    place_roof(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof"])

    # Kitchen counters
    for i in range(5):
        editor.placeBlock((x + 2, y + 1, z + 2 + i), Block("quartz_block"))
        editor.placeBlock((x + 2, y + 2, z + 2 + i), Block("polished_blackstone_pressure_plate"))
    editor.placeBlock((x + 2, y + 1, z + 2), Block("smoker", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("barrel"))
    editor.placeBlock((x + 2, y + 1, z + 6), Block("cauldron"))
    
    # Fridge
    editor.placeBlock((x + 2, y + 1, z + 8), Block("white_concrete"))
    editor.placeBlock((x + 2, y + 2, z + 8), Block("white_concrete"))
    editor.placeBlock((x + 2, y + 3, z + 8), Block("white_concrete"))
    editor.placeBlock((x + 1, y + 2, z + 8), Block("birch_button", {"face": "wall", "facing": "east"}))

    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["lighting"])

def build_luminous_quartz_office(x, y, z):  # Module E
    """Builds the Luminous Quartz Office (2F, North)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["flooring"])
    place_framing(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')

    # Desk
    for i in range(4):
        editor.placeBlock((x + 4 + i, y + 1, z + 2), Block("smooth_quartz_slab", {"type": "top"}))
    editor.placeBlock((x + 3, y + 1, z + 2), Block("quartz_pillar"))
    editor.placeBlock((x + 8, y + 1, z + 2), Block("quartz_pillar"))
    editor.placeBlock((x + 6, y + 1, z + 3), Block("birch_stairs", {"facing": "north"}))

    # Shelves and decor
    editor.placeBlock((x + 2, y + 1, z + 8), Block("bookshelf"))
    editor.placeBlock((x + 2, y + 2, z + 8), Block("bookshelf"))
    editor.placeBlock((x + 3, y + 1, z + 8), Block("chiseled_quartz_block"))
    editor.placeBlock((x + 3, y + 2, z + 8), Block("flower_pot"))
    editor.placeBlock((x + 3, y + 3, z + 8), Block("fern"))

    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["lighting"])

def build_serene_skyview_suite(x, y, z):  # Module D
    """Builds the Serene Skyview Suite (3F, North)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["roof"])
    place_framing(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')
    place_roof(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof"])

    # Bed
    editor.placeBlock((x + 4, y + 1, z + 2), Block("white_bed", {"part": "head", "facing": "south"}))
    editor.placeBlock((x + 4, y + 1, z + 3), Block("white_bed", {"part": "foot", "facing": "south"}))
    editor.placeBlock((x + 5, y + 1, z + 2), Block("white_bed", {"part": "head", "facing": "south"}))
    editor.placeBlock((x + 5, y + 1, z + 3), Block("white_bed", {"part": "foot", "facing": "south"}))
    
    # Carpet and side tables
    for i in range(4):
        for j in range(5):
            editor.placeBlock((x + 3 + i, y + 1, z + 5 + j), Block("white_carpet"))
    editor.placeBlock((x + 3, y + 1, z + 2), Block("birch_slab", {"type": "bottom"}))
    editor.placeBlock((x + 6, y + 1, z + 2), Block("birch_slab", {"type": "bottom"}))
    editor.placeBlock((x + 3, y + 2, z + 2), Block("end_rod"))
    editor.placeBlock((x + 6, y + 2, z + 2), Block("end_rod"))

    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["lighting"])

def build_stair_room(x, y, z):  # Module $
    """Builds the central staircase for floors 1 and 2."""
    # First floor stair room
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["foundation"], MATERIALS["flooring"])
    place_framing(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')
    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["lighting"])

    # Second floor stair room
    place_filled_room(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["flooring"])
    place_framing(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_lighting(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["lighting"])

    # Place stairs from 1F to 2F
    place_stairs(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'south', MATERIALS["staircase_stairs"])
    # Place stairs from 2F to 3F
    place_stairs(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'south', MATERIALS["staircase_stairs"])

def build_end_stair_room(x, y, z):  # Module @
    """Builds the top floor landing."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["walls"], MATERIALS["flooring"], MATERIALS["roof"])
    place_framing(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["frame"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')
    place_roof(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, MATERIALS["roof"])

    # Create opening for stairs from below
    make_stair_passage_on_floor(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'south')

    # Decor
    for i in range(4):
        for j in range(4):
            editor.placeBlock((x + 4 + i, y + 1, z + 1 + j), Block("light_gray_carpet"))
    editor.placeBlock((x + 2, y + 1, z + 2), Block("birch_slab", {"type": "bottom"}))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("birch_slab", {"type": "bottom"}))

    place_lighting(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["lighting"])

# === Master Build Function ===
def build_villa(x, y, z):
    """Constructs the entire villa by calling the module functions based on the layout."""
    # --- Floor 1 ---
    # Layout:
    # ΦAΦ
    # B$C
    # ΦΦΦ
    build_radiant_quartz_atrium(x + 1 * ROOM_WIDTH, y, z + 0 * ROOM_LENGTH)
    build_sun_drenched_great_room(x + 0 * ROOM_WIDTH, y, z + 1 * ROOM_LENGTH)
    build_minimalist_birch_kitchen(x + 2 * ROOM_WIDTH, y, z + 1 * ROOM_LENGTH)
    
    # --- Floor 2 ---
    # Layout:
    # ΦEΦ
    # Φ$Φ
    # ΦΦΦ
    build_luminous_quartz_office(x + 1 * ROOM_WIDTH, y + 1 * ROOM_HEIGHT, z + 0 * ROOM_LENGTH)

    # --- Floor 3 ---
    # Layout:
    # ΦDΦ
    # Φ@Φ
    # ΦΦΦ
    build_serene_skyview_suite(x + 1 * ROOM_WIDTH, y + 2 * ROOM_HEIGHT, z + 0 * ROOM_LENGTH)
    build_end_stair_room(x + 1 * ROOM_WIDTH, y + 2 * ROOM_HEIGHT, z + 1 * ROOM_LENGTH)

    # --- Multi-floor Structures ---
    # Staircase must be built after the rooms it connects to avoid being overwritten
    build_stair_room(x + 1 * ROOM_WIDTH, y, z + 1 * ROOM_LENGTH)

    print("Contemporary villa construction initiated.")

# === Main Execution Block ===
if __name__ == '__main__':
    try:
        start_x, start_y, start_z = 17589, -60, -1127

        # Call the master function to build the entire house.
        build_villa(start_x, start_y, start_z)

        # Flush the buffer to apply all the changes to the world.
        editor.flushBuffer()
        print("Build complete! Your contemporary villa is ready.")

    except Exception as e:
        print("An error occurred during the build process:")
        print(e)