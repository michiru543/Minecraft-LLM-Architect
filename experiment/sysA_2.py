from gdpc import Editor, Block, Transform, geometry

editor = Editor(buffering=True)

def build_modern_glass_house(x, y, z):
    """
Main
function
to
construct
the
entire
modern
house.
"""

    # --- House Dimensions and Materials ---
    LENGTH = 25
    WIDTH = 15
    HEIGHT = 10

    # Materials
    WALL_MATERIAL = "smooth_quartz"
    PILLAR_MATERIAL = "gray_concrete"
    GROUND_FLOOR_MATERIAL = "stone_bricks"
    SECOND_FLOOR_MATERIAL = "birch_planks"
    ROOF_MATERIAL = "glass"
    ROOF_FRAME_MATERIAL = "quartz_slab"
    WINDOW_MATERIAL = "black_stained_glass_pane"
    DOOR_MATERIAL = "dark_oak_door"
    STAIR_MATERIAL = "quartz_stairs"

    # Furniture
    BED_MATERIAL = "black_bed"
    LIGHTING_MATERIAL = "sea_lantern"
    SOFA_MATERIAL = "white_wool"
    SHELF_MATERIAL = "bookshelf"

    # --- Build Foundation and Floors ---
    print("Laying foundation and floors...")
    # Ground floor
    for dx in range(LENGTH):
        for dz in range(WIDTH):
            editor.placeBlock((x + dx, y, z + dz), Block(GROUND_FLOOR_MATERIAL))

    # Second floor (leaving a stairwell opening)
    stairwell_x_start = LENGTH - 5
    stairwell_z_start = 1
    for dx in range(LENGTH):
        for dz in range(WIDTH):
            is_stairwell = (stairwell_x_start <= dx < stairwell_x_start + 4) and (stairwell_z_start <= dz < stairwell_z_start + 8)
            if not is_stairwell:
                editor.placeBlock((x + dx, y + 5, z + dz), Block(SECOND_FLOOR_MATERIAL))

    # --- Build Walls and Pillars ---
    print("Erecting walls...")
    for dy in range(HEIGHT):
        for dx in range(LENGTH):
            # North and South Walls
            editor.placeBlock((x + dx, y + 1 + dy, z), Block(WALL_MATERIAL))
            editor.placeBlock((x + dx, y + 1 + dy, z + WIDTH - 1), Block(WALL_MATERIAL))
        for dz in range(WIDTH):
            # East and West Walls
            editor.placeBlock((x, y + 1 + dy, z + dz), Block(WALL_MATERIAL))
            editor.placeBlock((x + LENGTH - 1, y + 1 + dy, z + dz), Block(WALL_MATERIAL))

    # Add corner pillars
    for dy in range(HEIGHT):
        editor.placeBlock((x, y + 1 + dy, z), Block(PILLAR_MATERIAL))
        editor.placeBlock((x + LENGTH - 1, y + 1 + dy, z), Block(PILLAR_MATERIAL))
        editor.placeBlock((x, y + 1 + dy, z + WIDTH - 1), Block(PILLAR_MATERIAL))
        editor.placeBlock((x + LENGTH - 1, y + 1 + dy, z + WIDTH - 1), Block(PILLAR_MATERIAL))

    # --- Add Windows and Door ---
    print("Installing windows and door...")
    # Clear space for windows on the long (south) wall
    for dx in range(3, LENGTH - 3, 4):
        editor.placeBlock((x + dx, y + 2, z + WIDTH - 1), Block("air"))
        editor.placeBlock((x + dx + 1, y + 2, z + WIDTH - 1), Block("air"))
        editor.placeBlock((x + dx, y + 3, z + WIDTH - 1), Block("air"))
        editor.placeBlock((x + dx + 1, y + 3, z + WIDTH - 1), Block("air"))
        # Place panes
        editor.placeBlock((x + dx, y + 2, z + WIDTH - 1), Block(WINDOW_MATERIAL))
        editor.placeBlock((x + dx + 1, y + 2, z + WIDTH - 1), Block(WINDOW_MATERIAL))
        editor.placeBlock((x + dx, y + 3, z + WIDTH - 1), Block(WINDOW_MATERIAL))
        editor.placeBlock((x + dx + 1, y + 3, z + WIDTH - 1), Block(WINDOW_MATERIAL))

    # Place Door (centered on a short wall)
    door_x = x + LENGTH // 2
    editor.placeBlock((door_x, y + 1, z), Block("air"))
    editor.placeBlock((door_x, y + 2, z), Block("air"))
    editor.placeBlock((door_x, y + 1, z), Block(DOOR_MATERIAL, {"half": "lower", "facing": "south", "hinge": "left"}))
    editor.placeBlock((door_x, y + 2, z), Block(DOOR_MATERIAL, {"half": "upper", "facing": "south", "hinge": "left"}))

    # --- Build the Glass Roof ---
    print("Constructing the glass roof...")
    roof_y = y + HEIGHT + 1
    for dx in range(LENGTH):
        for dz in range(WIDTH):
            is_edge = dx == 0 or dx == LENGTH - 1 or dz == 0 or dz == WIDTH - 1
            material = ROOF_FRAME_MATERIAL if is_edge else ROOF_MATERIAL
            editor.placeBlock((x + dx, roof_y, z + dz), Block(material))

    # --- Add Interior Furnishings ---
    print("Adding interior furnishings...")
    # Staircase
    for i in range(5):
        editor.placeBlock((x + stairwell_x_start + 3, y + 1 + i, z + stairwell_z_start + i), Block(STAIR_MATERIAL, {"facing": "west"}))
        editor.placeBlock((x + stairwell_x_start + 2, y + 1 + i, z + stairwell_z_start + i), Block(STAIR_MATERIAL, {"facing": "west"}))

    # Second Floor furnishings
    bed_y = y + 6
    # Bed
    editor.placeBlock((x + 2, bed_y, z + 2), Block(BED_MATERIAL, {"part": "foot", "facing": "south"}))
    editor.placeBlock((x + 2, bed_y, z + 1), Block(BED_MATERIAL, {"part": "head", "facing": "south"}))
    # Bookshelves
    for i in range(4):
        editor.placeBlock((x + 1, bed_y + i, z + 5), Block(SHELF_MATERIAL))

    # Sofas
    for i in range(4):
        editor.placeBlock((x + LENGTH - 3, bed_y, z + 2 + i), Block(SOFA_MATERIAL))
    editor.placeBlock((x + LENGTH - 4, bed_y, z + 2), Block(STAIR_MATERIAL, {"facing": "east"}))
    editor.placeBlock((x + LENGTH - 4, bed_y, z + 5), Block(STAIR_MATERIAL, {"facing": "east"}))

    # Lighting (embedded in the second floor)
    editor.placeBlock((x + 3, y + 5, z + 3), Block(LIGHTING_MATERIAL))
    editor.placeBlock((x + LENGTH - 4, y + 5, z + 3), Block(LIGHTING_MATERIAL))
    editor.placeBlock((x + 3, y + 5, z + WIDTH - 4), Block(LIGHTING_MATERIAL))
    editor.placeBlock((x + LENGTH - 4, y + 5, z + WIDTH - 4), Block(LIGHTING_MATERIAL))

    print("Quartz Atrium House build complete!")

# --- Main Execution ---
if __name__ == '__main__':
    try:
        start_x, start_y, start_z = 17784, -60, -979

        # Call the main function to build the house at the start of the build area
        build_modern_glass_house(start_x, start_y, start_z)

        # IMPORTANT: Flush the buffer to send all commands to the game
        print("Sending all commands to Minecraft...")
        editor.flushBuffer()
        print("Done!")

    except Exception as e:
        print(f"An error occurred during the build process: {e}")