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
    "primary_facade": "white_concrete",
    "accent_facade": "calcite",
    "frame_and_roof": "smooth_quartz",
    "internal_flooring": "birch_planks",
    "windows": "light_gray_stained_glass",
    "door": "dark_oak_door",
    "door_accents": "dark_oak_planks",
    "pool_basin": "prismarine_bricks",
    "pool_water": "water",
    "pool_deck": "polished_andesite",
    "stair_material": "smooth_quartz_stairs"
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
            # Clear space for headroom
            for j in range(height - 1):
                editor.placeBlock((x_start, y_start + 1 + j, z_start - i), Block("air"))
                editor.placeBlock((x_start + 1, y_start + 1 + j, z_start - i), Block("air"))
                editor.placeBlock((x_start - 1, y_start + 1 + j, z_start - i), Block("air"))

            # Place stair block
            editor.placeBlock((x_start, y_start + i, z_start - i), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start + 1, y_start + i, z_start - i), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start - 1, y_start + i, z_start - i), Block(material, {"half": "bottom", "facing": facing}))

            # Railing
            editor.placeBlock((x_start + 2, y_start, z_start - i), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - 2, y_start, z_start - i), Block("light_gray_stained_glass_pane"))
    elif facing == 'south':
        x_start = x + width // 2
        y_start = y + 1
        z_start = z + base_point_z
        for i in range(height - 1):
            # Clear space for headroom
            for j in range(height - 1):
                editor.placeBlock((x_start, y_start + 1 + j, z_start + i), Block("air"))
                editor.placeBlock((x_start + 1, y_start + 1 + j, z_start + i), Block("air"))
                editor.placeBlock((x_start - 1, y_start + 1 + j, z_start + i), Block("air"))

            # Place stair block
            editor.placeBlock((x_start, y_start + i, z_start + i), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start + 1, y_start + i, z_start + i), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start - 1, y_start + i, z_start + i), Block(material, {"half": "bottom", "facing": facing}))

            # Railing
            editor.placeBlock((x_start + 2, y_start, z_start + i), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - 2, y_start, z_start + i), Block("light_gray_stained_glass_pane"))
    elif facing == 'west':
        x_start = x + base_point_x + height - 2
        y_start = y + 1
        z_start = z + length // 2
        for i in range(height - 1):
            # Clear space for headroom
            for j in range(height - 1):
                editor.placeBlock((x_start - i, y_start + 1 + j, z_start), Block("air"))
                editor.placeBlock((x_start - i, y_start + 1 + j, z_start - 1), Block("air"))
                editor.placeBlock((x_start - i, y_start + 1 + j, z_start + 1), Block("air"))

            # Place stair block
            editor.placeBlock((x_start - i, y_start + i, z_start), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start - i, y_start + i, z_start + 1), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start - i, y_start + i, z_start - 1), Block(material, {"half": "bottom", "facing": facing}))

            # Railing
            editor.placeBlock((x_start - i, y_start, z_start + 2), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - i, y_start, z_start - 2), Block("light_gray_stained_glass_pane"))
    elif facing == 'east':
        x_start = x + base_point_x
        y_start = y + 1
        z_start = z + length // 2
        for i in range(height - 1):
            # Clear space for headroom
            for j in range(height - 1):
                editor.placeBlock((x_start + i, y_start + 1 + j, z_start), Block("air"))
                editor.placeBlock((x_start + i, y_start + 1 + j, z_start - 1), Block("air"))
                editor.placeBlock((x_start + i, y_start + 1 + j, z_start + 1), Block("air"))

            # Place stair block
            editor.placeBlock((x_start + i, y_start + i, z_start), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start + i, y_start + i, z_start + 1), Block(material, {"half": "bottom", "facing": facing}))
            editor.placeBlock((x_start + i, y_start + i, z_start - 1), Block(material, {"half": "bottom", "facing": facing}))

            # Railing
            editor.placeBlock((x_start + i, y_start, z_start + 2), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start + i, y_start, z_start - 2), Block("light_gray_stained_glass_pane"))

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
            editor.placeBlock((x_start + 1, y, z_start + i), Block("air"))
            editor.placeBlock((x_start - 1, y, z_start + i), Block("air"))
            editor.placeBlock((x_start + 2, y + 1, z_start + i), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start - 2, y + 1, z_start + i), Block("light_gray_stained_glass_pane"))
    elif direction == 'east' or direction == 'west':
        x_start = x + base_point_x
        z_start = z + length // 2
        for i in range(height - 1):
            editor.placeBlock((x_start + i, y, z_start), Block("air"))
            editor.placeBlock((x_start + i, y, z_start + 1), Block("air"))
            editor.placeBlock((x_start + i, y, z_start - 1), Block("air"))
            editor.placeBlock((x_start + i, y + 1, z_start + 2), Block("light_gray_stained_glass_pane"))
            editor.placeBlock((x_start + i, y + 1, z_start - 2), Block("light_gray_stained_glass_pane"))

# === Module Functions ===
# Each function builds a specific module (room or area) from the JSON layout.

def build_grand_foyer(x, y, z):  # Module A
    """Builds the Grand Foyer (1F, south-center)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["primary_facade"],MATERIALS["internal_flooring"], MATERIALS["frame_and_roof"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')  # To Main Staircase
    place_door(x + ROOM_WIDTH // 2, y + 1, z + ROOM_LENGTH - 1, 'south', MATERIALS["door"])

    # Furniture
    editor.placeBlock((x + 2, y + 1, z + 2), Block("flower_pot"))
    editor.placeBlock((x + 2, y + 2, z + 2), Block("birch_sapling"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 2), Block("sea_lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 2, z + 2), Block("light_gray_carpet"))
    # Console Table
    for i in range(3):
        editor.placeBlock((x + 4 + i, y + 1, z + 2), Block("smooth_quartz_slab", {"type": "bottom"}))
    editor.placeBlock((x + 3, y + 1, z + 2), Block("dark_oak_fence"))
    editor.placeBlock((x + 7, y + 1, z + 2), Block("dark_oak_fence"))

    # Lightning
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))


def build_open_plan_living(x, y, z):  # Module B
    """Builds the Open-Plan Living Area (1F, east-center)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["primary_facade"],MATERIALS["internal_flooring"], MATERIALS["frame_and_roof"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')  # To Modern Kitchen
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')  # To Main Staircase

    # Furniture: Sofa
    for i in range(4):
        editor.placeBlock((x + 3, y + 1, z + 4 + i), Block("smooth_quartz_stairs", {"facing": "east"}))
    editor.placeBlock((x + 4, y + 1, z + 3), Block("smooth_quartz_stairs", {"facing": "south"}))
    editor.placeBlock((x + 4, y + 1, z + 8), Block("smooth_quartz_stairs", {"facing": "north"}))
    for i in range(2):
        for j in range(4):
            editor.placeBlock((x + 4 + i, y + 1, z + 4 + j), Block("white_wool"))

    # Furniture: TV and Entertainment Center
    place_wall_section(x + ROOM_WIDTH - 2, y + 1, z + 4, 3, 2, "black_concrete", 'west')
    for i in range(5):
        editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 3 + i), Block("birch_slab", {"type": "bottom"}))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 3, z + 5), Block("chain"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 2, z + 5), Block("end_rod"))

    # Lightning
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))


def build_modern_kitchen(x, y, z):  # Module C
    """Builds the Modern Kitchen (1F, east-north)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["accent_facade"],MATERIALS["internal_flooring"], MATERIALS["frame_and_roof"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')  # To Living Area
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')  # To Poolside Lounge

    # Counters and Appliances
    for i in range(5):
        editor.placeBlock((x + 2, y + 1, z + 2 + i), Block("smooth_quartz"))
        editor.placeBlock((x + 2, y + 2, z + 2 + i), Block("heavy_weighted_pressure_plate"))
    editor.placeBlock((x + 2, y + 1, z + 2), Block("blast_furnace", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("smoker", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 6), Block("cauldron"))
    editor.placeBlock((x + 1, y + 2, z + 6), Block("tripwire_hook", {"facing": "east"}))
    # Fridge
    editor.placeBlock((x + 2, y + 1, z + 8), Block("iron_block"))
    editor.placeBlock((x + 2, y + 2, z + 8), Block("iron_block"))
    # Cabinets
    for i in range(5):
        editor.placeBlock((x + 2, y + 3, z + 2 + i), Block("white_shulker_box", {"facing": "east"}))

    # Lightning
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))


def build_master_suite(x, y, z):  # Module D
    """Builds the Master Suite (2F, east-center)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["primary_facade"],MATERIALS["internal_flooring"], MATERIALS["frame_and_roof"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')  # To Main Staircase

    # Bed
    editor.placeBlock((x + 4, y + 1, z + 3), Block("white_bed", {"part": "foot", "facing": "north"}))
    editor.placeBlock((x + 4, y + 1, z + 2), Block("white_bed", {"part": "head", "facing": "north"}))
    editor.placeBlock((x + 5, y + 1, z + 3), Block("white_bed", {"part": "foot", "facing": "north"}))
    editor.placeBlock((x + 5, y + 1, z + 2), Block("white_bed", {"part": "head", "facing": "north"}))

    # Wardrobe
    for i in range(4):
        editor.placeBlock((x + ROOM_WIDTH - 2, y + 1 + i, z + 8), Block(MATERIALS["door_accents"]))
        editor.placeBlock((x + ROOM_WIDTH - 2, y + 1 + i, z + 9), Block(MATERIALS["door_accents"]))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 8), Block("birch_door", {"facing": "east"}))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + 1, z + 9), Block("birch_door", {"facing": "east"}))

    # Lighting and Carpet
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("end_rod", {"facing": "down"}))
    for i in range(5):
        for j in range(5):
            editor.placeBlock((x + 3 + i, y + 1, z + 2 + j), Block("white_carpet"))

    # Lightning
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))


def build_cantilevered_balcony(x, y, z):  # Module E
    """Builds the Cantilevered Balcony (2F, north-center)."""
    # Balcony is open-air, so no room, just a floor and railing.
    for i in range(ROOM_WIDTH):
        for j in range(ROOM_LENGTH):
            editor.placeBlock((x + i, y, z + j), Block(MATERIALS["frame_and_roof"]))

    # Railing
    for i in range(ROOM_WIDTH):
        editor.placeBlock((x + i, y + 1, z), Block("light_gray_stained_glass_pane"))
    for j in range(ROOM_LENGTH):
        editor.placeBlock((x, y + 1, z + j), Block("light_gray_stained_glass_pane"))
        editor.placeBlock((x + ROOM_WIDTH - 1, y + 1, z + j), Block("light_gray_stained_glass_pane"))

    # Passage to staircase (south wall is open)
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')

    # Furniture
    editor.placeBlock((x + 2, y + 1, z + 2), Block("dark_oak_stairs", {"facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + 3), Block("dark_oak_slab"))
    editor.placeBlock((x + 2, y + 1, z + 4), Block("dark_oak_stairs", {"facing": "east"}))
    editor.placeBlock((x + 4, y + 1, z + 2), Block("dirt"))
    editor.placeBlock((x + 4, y + 2, z + 2), Block("white_tulip"))
    editor.placeBlock((x + ROOM_WIDTH - 2, y + 1, z + 2), Block("lantern"))

    # Lightning
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))


def build_poolside_lounge(x, y, z):  # Module F
    """Builds the Poolside Lounge (1F, north-center)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["primary_facade"],MATERIALS["pool_deck"], MATERIALS["frame_and_roof"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')  # To Main Staircase
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')  # To Modern Kitchen

    # Glass wall facing the pool
    place_wall_section(x + 1, y + 1, z, ROOM_WIDTH - 2, ROOM_HEIGHT - 2, MATERIALS["windows"], 'north')

    # Furniture
    editor.placeBlock((x + 2, y + 1, z + 2), Block("flower_pot"))
    editor.placeBlock((x + 2, y + 2, z + 2), Block("azalea"))
    # Lounge chairs
    editor.placeBlock((x + 4, y + 1, z + 2), Block("birch_stairs", {"facing": "south"}))
    editor.placeBlock((x + 5, y + 1, z + 2), Block("birch_slab"))
    editor.placeBlock((x + 7, y + 1, z + 2), Block("birch_stairs", {"facing": "south"}))
    editor.placeBlock((x + 8, y + 1, z + 2), Block("birch_slab"))

    # Lightning
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))


def build_sky_lounge(x, y, z):  # Module G
    """Builds the Sky Lounge (3F, east-center)."""
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["primary_facade"],MATERIALS["internal_flooring"], MATERIALS["frame_and_roof"])
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'west')  # To Top Floor Landing

    # Large glass windows for sky view
    place_wall_section(x + 1, y + 1, z, ROOM_WIDTH - 2, ROOM_HEIGHT - 2, MATERIALS["windows"], 'north')
    place_wall_section(x + ROOM_WIDTH - 1, y + 1, z + 1, ROOM_LENGTH - 2, ROOM_HEIGHT - 2, MATERIALS["windows"], 'east')

    # Furniture
    for i in range(4):
        editor.placeBlock((x + 3 + i, y + 1, z + 3), Block("gray_wool"))
    editor.placeBlock((x + 3, y + 1, z + 4), Block("gray_wool"))
    editor.placeBlock((x + 6, y + 1, z + 4), Block("gray_wool"))
    editor.placeBlock((x + 4, y + 1, z + 5), Block("smooth_quartz_slab"))
    editor.placeBlock((x + 5, y + 1, z + 5), Block("smooth_quartz_slab"))
    editor.placeBlock((x + 2, y + 1, z + ROOM_LENGTH - 2), Block("amethyst_block"))
    editor.placeBlock((x + 2, y + 2, z + ROOM_LENGTH - 2), Block("end_rod"))

def build_main_staircase(x, y, z):  # Module $
    """Builds the Main Staircase connecting floors 1 and 2."""
    # Build room structure for the first floor
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["primary_facade"],MATERIALS["internal_flooring"], MATERIALS["internal_flooring"]) # Floor is also roof of below
    # Build room structure for the second floor
    place_filled_room(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["primary_facade"],MATERIALS["internal_flooring"], MATERIALS["frame_and_roof"])

    # Passages on 1F
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'north')  # To Poolside Lounge (F)
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'south')  # To Grand Foyer (A)
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')  # To Open-Plan Living (B)

    # Lightning on 1F
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))

    # Passages on 2F
    place_3x3_arch(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, 'north')  # To Balcony (E)
    place_3x3_arch(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, 'east')  # To Master Suite (D)

    # Build stairs from Floor 1 to Floor 2, facing North
    place_stairs(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'north', MATERIALS["stair_material"])
    # Build stairs from Floor 2 to Floor 3, facing North
    place_stairs(x, y + ROOM_HEIGHT, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'north', MATERIALS["stair_material"])

    # Lightning on 2F
    editor.placeBlock((x + 2, y + ROOM_HEIGHT * 2 - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT * 2 - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT * 2 - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT * 2 - 2, z + ROOM_LENGTH - 3), Block("lantern"))


def build_end_stair_room(x, y, z):  # Module @
    """Builds the landing for the top floor and the stairs from 2F to 3F."""
    # Build room structure for the third floor landing
    place_filled_room(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, MATERIALS["primary_facade"],MATERIALS["internal_flooring"], MATERIALS["frame_and_roof"])

    # Passage on 3F
    place_3x3_arch(x, y, z, ROOM_WIDTH, ROOM_LENGTH, 'east')  # To Sky Lounge (G)

    # Create hole for the stairs from below (Do not omit this step)
    make_stair_passage_on_floor(x, y, z, ROOM_WIDTH, ROOM_LENGTH, ROOM_HEIGHT, 'north')

    # Decor
    editor.placeBlock((x + 2, y + 1, z + 2), Block("quartz_pillar"))
    editor.placeBlock((x + 2, y + 2, z + 2), Block("chiseled_quartz_block"))
    editor.placeBlock((x + 2, y + 3, z + 2), Block("sea_lantern"))

    # Lightning
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + 2), Block("lantern"))
    editor.placeBlock((x + 2, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))
    editor.placeBlock((x + ROOM_WIDTH - 3, y + ROOM_HEIGHT - 2, z + ROOM_LENGTH - 3), Block("lantern"))



def build_pool(x, y, z):
    """Builds the outdoor pool."""
    pool_w, pool_l = ROOM_WIDTH, ROOM_LENGTH + 5
    pool_x, pool_z = x, z - pool_l
    # Pool basin
    for i in range(pool_w):
        for j in range(pool_l):
            for d in range(4):  # 4 blocks deep
                editor.placeBlock((pool_x + i, y - d, pool_z + j), Block("air"))  # Dig
            editor.placeBlock((pool_x + i, y - 4, pool_z + j), Block(MATERIALS["pool_basin"]))  # Basin floor
    # Fill with water
    for i in range(1, pool_w - 1):
        for j in range(1, pool_l - 1):
            for d in range(1, 4):
                editor.placeBlock((pool_x + i, y - d, pool_z + j), Block(MATERIALS["pool_water"]))
    # Pool deck border
    for i in range(pool_w):
        editor.placeBlock((pool_x + i, y, pool_z), Block(MATERIALS["pool_deck"]))
        editor.placeBlock((pool_x + i, y, pool_z + pool_l - 1), Block(MATERIALS["pool_deck"]))
    for j in range(pool_l):
        editor.placeBlock((pool_x, y, pool_z + j), Block(MATERIALS["pool_deck"]))
        editor.placeBlock((pool_x + pool_w - 1, y, pool_z + j), Block(MATERIALS["pool_deck"]))


# === Master Build Function ===
def build_luxury_home(x, y, z):
    """Constructs the entire house by calling the module functions based on the layout."""
    # Floor 1 Layout
    # ΦFC
    # Φ$B
    # ΦAΦ
    build_poolside_lounge(x + 1 * ROOM_WIDTH, y, z + 0 * ROOM_LENGTH)
    build_modern_kitchen(x + 2 * ROOM_WIDTH, y, z + 0 * ROOM_LENGTH)
    build_main_staircase(x + 1 * ROOM_WIDTH, y, z + 1 * ROOM_LENGTH) # Must execute build_main_staircase before executing build_end_stair_room.
    build_open_plan_living(x + 2 * ROOM_WIDTH, y, z + 1 * ROOM_LENGTH)
    build_grand_foyer(x + 1 * ROOM_WIDTH, y, z + 2 * ROOM_LENGTH)
    build_pool(x + 1 * ROOM_WIDTH, y, z + 0 * ROOM_LENGTH)

    # Build roof at A and C

    # Floor 2 Layout
    # ΦEΦ
    # Φ$D
    # ΦΦΦ
    build_cantilevered_balcony(x + 1 * ROOM_WIDTH, y + 1 * ROOM_HEIGHT, z + 0 * ROOM_LENGTH)
    build_master_suite(x + 2 * ROOM_WIDTH, y + 1 * ROOM_HEIGHT, z + 1 * ROOM_LENGTH)

    # Build roof at E

    # Floor 3 Layout
    # ΦΦΦ
    # Φ@G
    # ΦΦΦ
    build_end_stair_room(x + 1 * ROOM_WIDTH, y + 2 * ROOM_HEIGHT, z + 1 * ROOM_LENGTH)
    build_sky_lounge(x + 2 * ROOM_WIDTH, y + 2 * ROOM_HEIGHT, z + 1 * ROOM_LENGTH)

    # Build roof at @ and G

    print(f"Modern minimalist luxury home construction initiated at ({x}, {y}, {z}).")


# === Main Execution Block ===
if __name__ == '__main__':
    try:
        # Decided by the user
        start_x, start_y, start_z = 10600, -60, -261

        # Call the master function to build the entire house.
        build_luxury_home(start_x, start_y, start_z)

        # Flush the buffer to apply all the changes to the world.
        editor.flushBuffer()
        print("Build complete! Your modern luxury home is ready.")

    except Exception as e:
        print(f"An error occurred during the build process: {e}")
        # It's good practice to still flush the buffer to see partial results
        # in case of an error during a long build.
        if "flushBuffer" in dir(editor):
            editor.flushBuffer()