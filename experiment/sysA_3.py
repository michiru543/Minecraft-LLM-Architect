from gdpc import Editor, Block, Transform, geometry

editor = Editor(buffering=True)

def build_foresters_stronghold(x, y, z):
    """
Main
function
to
construct
the
entire
wooden and stone
house.
"""

    # --- House Dimensions and Materials ---
    LENGTH = 20  # along x-axis
    WIDTH = 12   # along z-axis
    WALL_HEIGHT = 6

    # Materials
    FOUNDATION_MATERIAL = "cobblestone"
    FRAME_MATERIAL = "oak_log"
    WALL_MATERIAL = "oak_planks"
    SECOND_FLOOR_MATERIAL = "oak_planks"
    ROOF_STAIR_MATERIAL = "cobblestone_stairs"
    ROOF_SLAB_MATERIAL = "cobblestone_slab"
    WINDOW_MATERIAL = "glass_pane"
    DOOR_MATERIAL = "dark_oak_door"
    STAIRCASE_MATERIAL = "oak_stairs"

    # Furniture & Decorations
    FURNACE_MATERIAL = "furnace"
    CRAFTING_MATERIAL = "crafting_table"
    CHEST_MATERIAL = "chest"
    BED_MATERIAL = "white_bed"
    BARREL_MATERIAL = "barrel"
    LIGHTING_MATERIAL = "lantern"

    # --- Build Foundation and First Floor ---
    print("Laying the foundation...")
    for dx in range(LENGTH):
        for dz in range(WIDTH):
            editor.placeBlock((x + dx, y, z + dz), Block(FOUNDATION_MATERIAL))

    # --- Build Structural Frame and Walls ---
    print("Building the timber frame and walls...")
    for dy in range(WALL_HEIGHT):
        # Place logs at corners and midpoints
        for dx in [0, LENGTH // 2 -1, LENGTH - 1]:
            editor.placeBlock((x + dx, y + 1 + dy, z), Block(FRAME_MATERIAL))
            editor.placeBlock((x + dx, y + 1 + dy, z + WIDTH - 1), Block(FRAME_MATERIAL))
        for dz in [0, WIDTH - 1]:
             editor.placeBlock((x, y + 1 + dy, z + dz), Block(FRAME_MATERIAL))
             editor.placeBlock((x + LENGTH - 1, y + 1 + dy, z + dz), Block(FRAME_MATERIAL))

    # Fill in walls with planks
    for dy in range(WALL_HEIGHT):
        for dx in range(1, LENGTH - 1):
            editor.placeBlock((x + dx, y + 1 + dy, z), Block(WALL_MATERIAL))
            editor.placeBlock((x + dx, y + 1 + dy, z + WIDTH - 1), Block(WALL_MATERIAL))
        for dz in range(1, WIDTH - 1):
            editor.placeBlock((x, y + 1 + dy, z + dz), Block(WALL_MATERIAL))
            editor.placeBlock((x + LENGTH - 1, y + 1 + dy, z + dz), Block(WALL_MATERIAL))

    # --- Place Second Floor ---
    print("Adding the second floor...")
    for dx in range(LENGTH):
        for dz in range(WIDTH):
            editor.placeBlock((x + dx, y + WALL_HEIGHT + 1, z + dz), Block(SECOND_FLOOR_MATERIAL))

    # Add ceiling beams
    for dx in range(LENGTH):
        editor.placeBlock((x + dx, y + WALL_HEIGHT + 1, z), Block(FRAME_MATERIAL))
        editor.placeBlock((x + dx, y + WALL_HEIGHT + 1, z + WIDTH - 1), Block(FRAME_MATERIAL))
        editor.placeBlock((x + dx, y + WALL_HEIGHT + 1, z + WIDTH // 2), Block(FRAME_MATERIAL))

    # --- Carve out Windows and Door ---
    print("Adding windows and door...")
    # Door
    door_x = x + LENGTH // 2
    editor.placeBlock((door_x, y + 1, z), Block("air"))
    editor.placeBlock((door_x, y + 2, z), Block("air"))
    editor.placeBlock((door_x, y + 1, z), Block(DOOR_MATERIAL, {"half": "lower", "facing": "south"}))
    editor.placeBlock((door_x, y + 2, z), Block(DOOR_MATERIAL, {"half": "upper", "facing": "south"}))

    # Windows
    for dx in [4, LENGTH - 5]:
        editor.placeBlock((x + dx, y + 3, z), Block(WINDOW_MATERIAL))
        editor.placeBlock((x + dx, y + 3, z + WIDTH - 1), Block(WINDOW_MATERIAL))
    for dz in [3, WIDTH - 4]:
        editor.placeBlock((x, y + 3, z + dz), Block(WINDOW_MATERIAL))
        editor.placeBlock((x + LENGTH - 1, y + 3, z + dz), Block(WINDOW_MATERIAL))

    # --- Build the Roof ---
    print("Constructing the stone roof...")
    roof_height = (WIDTH // 2) + 2
    roof_y_start = y + WALL_HEIGHT + 2
    for i in range(roof_height):
        # Place stairs for the slope
        for dx in range(-1, LENGTH + 1):
            # South-facing stairs
            editor.placeBlock((x + dx, roof_y_start + i, z - 1 + i), Block(ROOF_STAIR_MATERIAL, {"facing": "south"}))
            # North-facing stairs
            editor.placeBlock((x + dx, roof_y_start + i, z + WIDTH - i), Block(ROOF_STAIR_MATERIAL, {"facing": "north"}))

        # Fill in the gables
        if i < roof_height - 1:
            for dy in range(i + 1):
                editor.placeBlock((x - 1, roof_y_start + dy, z + i), Block(WALL_MATERIAL))
                editor.placeBlock((x + LENGTH, roof_y_start + dy, z + i), Block(WALL_MATERIAL))
                editor.placeBlock((x - 1, roof_y_start + dy, z + WIDTH - 1 - i), Block(WALL_MATERIAL))
                editor.placeBlock((x + LENGTH, roof_y_start + dy, z + WIDTH - 1 - i), Block(WALL_MATERIAL))


    # Add the roof cap
    for dx in range(-1, LENGTH + 1):
        editor.placeBlock((x + dx, roof_y_start + roof_height -1, z - 1 + roof_height -1), Block(ROOF_SLAB_MATERIAL))


    # --- Add Interior ---
    print("Furnishing the interior...")
    # Staircase
    for i in range(WALL_HEIGHT + 1):
        editor.placeBlock((x + LENGTH - 2, y + 1 + i, z + WIDTH - 2 - i), Block(STAIRCASE_MATERIAL, {"facing": "north"}))
        # Clear space for stairs
        editor.placeBlock((x + LENGTH - 2, y + WALL_HEIGHT + 1, z + WIDTH - 2 - i), Block("air"))

    # Ground Floor furnishings
    editor.placeBlock((x + 1, y + 1, z + 1), Block(CRAFTING_MATERIAL))
    editor.placeBlock((x + 2, y + 1, z + 1), Block(FURNACE_MATERIAL))
    editor.placeBlock((x + 1, y + 1, z + WIDTH - 2), Block(CHEST_MATERIAL))
    editor.placeBlock((x + 2, y + 1, z + WIDTH - 2), Block(CHEST_MATERIAL, {"facing": "west"}))

    # Second Floor furnishings (relative to the new floor height)
    bed_y = y + WALL_HEIGHT + 2
    editor.placeBlock((x + 1, bed_y, z + 1), Block(BED_MATERIAL, {"part": "foot", "facing": "south"}))
    editor.placeBlock((x + 1, bed_y, z), Block(BED_MATERIAL, {"part": "head", "facing": "south"}))
    editor.placeBlock((x + 1, bed_y, z + 2), Block(BARREL_MATERIAL))
    editor.placeBlock((x + 2, bed_y, z + 2), Block(BARREL_MATERIAL))

    # Lighting
    editor.placeBlock((x + 3, y + WALL_HEIGHT, z + 3), Block(LIGHTING_MATERIAL))
    editor.placeBlock((x + LENGTH - 4, y + WALL_HEIGHT, z + WIDTH - 4), Block(LIGHTING_MATERIAL))
    editor.placeBlock((x + LENGTH // 2, y + WALL_HEIGHT + roof_height + 1, z + WIDTH // 2), Block(LIGHTING_MATERIAL))


    print("Forester's Stronghold build complete!")

# --- Main Execution ---
if __name__ == '__main__':
    try:
        start_x, start_y, start_z = 5516, -60, -233

        build_foresters_stronghold(start_x, start_y, start_z)

        print("Sending all commands to Minecraft...")
        editor.flushBuffer()
        print("Done!")

    except Exception as e:
        print(f"An error occurred: {e}")