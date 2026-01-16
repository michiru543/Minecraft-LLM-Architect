
from gdpc import Editor, Block, Transform, geometry

editor = Editor(buffering=True)

def build_miners_cottage(x, y, z):
    """
Main
function
to
construct
the
stone and wood
cottage.
"""

    # --- House Dimensions and Materials ---
    LENGTH = 11  # along x-axis
    WIDTH = 9    # along z-axis
    WALL_HEIGHT = 5

    # Materials
    WALL_MATERIAL = "stone_bricks"
    CORNER_MATERIAL = "cobblestone"
    FLOOR_MATERIAL = "spruce_planks"
    ROOF_STAIR_MATERIAL = "dark_oak_stairs"
    ROOF_SLAB_MATERIAL = "dark_oak_slab"
    ROOF_PLANK_MATERIAL = "dark_oak_planks"
    WINDOW_MATERIAL = "glass"
    DOOR_MATERIAL = "oak_door"

    # Furniture & Decorations
    BED_MATERIAL = "blue_bed"
    CHEST_MATERIAL = "chest"
    FURNACE_MATERIAL = "furnace"
    CRAFTING_MATERIAL = "crafting_table"
    LIGHTING_MATERIAL = "torch"

    # --- Build Floor ---
    print("Laying the floor...")
    for dx in range(LENGTH):
        for dz in range(WIDTH):
            editor.placeBlock((x + dx, y, z + dz), Block(FLOOR_MATERIAL))

    # --- Build Walls ---
    print("Building the stone walls...")
    for dy in range(WALL_HEIGHT):
        for dx in range(LENGTH):
            for dz in range(WIDTH):
                is_wall = dx == 0 or dx == LENGTH - 1 or dz == 0 or dz == WIDTH - 1
                is_corner = (dx == 0 or dx == LENGTH - 1) and (dz == 0 or dz == WIDTH - 1)

                if is_corner:
                    editor.placeBlock((x + dx, y + 1 + dy, z + dz), Block(CORNER_MATERIAL))
                elif is_wall:
                    editor.placeBlock((x + dx, y + 1 + dy, z + dz), Block(WALL_MATERIAL))

    # --- Place Door and Windows ---
    print("Adding door and windows...")
    # Door (centered on the front wall)
    door_x = x + LENGTH // 2
    editor.placeBlock((door_x, y + 1, z), Block("air"))
    editor.placeBlock((door_x, y + 2, z), Block("air"))
    editor.placeBlock((door_x, y + 1, z), Block(DOOR_MATERIAL, {"half": "lower", "facing": "south"}))
    editor.placeBlock((door_x, y + 2, z), Block(DOOR_MATERIAL, {"half": "upper", "facing": "south"}))

    # Windows
    window_y = y + 3
    # Front windows
    editor.placeBlock((x + 2, window_y, z), Block(WINDOW_MATERIAL))
    editor.placeBlock((x + LENGTH - 3, window_y, z), Block(WINDOW_MATERIAL))
    # Back window
    editor.placeBlock((x + LENGTH // 2, window_y, z + WIDTH - 1), Block(WINDOW_MATERIAL))
    # Side windows
    editor.placeBlock((x, window_y, z + WIDTH // 2), Block(WINDOW_MATERIAL))
    editor.placeBlock((x + LENGTH - 1, window_y, z + WIDTH // 2), Block(WINDOW_MATERIAL))

    # --- Build the Roof ---
    print("Constructing the wooden roof...")
    roof_y_start = y + WALL_HEIGHT + 1
    roof_height = (WIDTH // 2) + 1
    for i in range(roof_height):
        # Place stairs for the slope
        for dx in range(-1, LENGTH + 1):
            # South-facing stairs (front)
            editor.placeBlock((x + dx, roof_y_start + i, z - 1 + i), Block(ROOF_STAIR_MATERIAL, {"facing": "south"}))
            # North-facing stairs (back)
            editor.placeBlock((x + dx, roof_y_start + i, z + WIDTH - i), Block(ROOF_STAIR_MATERIAL, {"facing": "north"}))

    # Fill in the roof gables (sides)
    for i in range(roof_height):
        for j in range(i, roof_height -1):
             editor.placeBlock((x-1, roof_y_start + i, z + j), Block(ROOF_PLANK_MATERIAL))
             editor.placeBlock((x+LENGTH, roof_y_start + i, z + j), Block(ROOF_PLANK_MATERIAL))
             editor.placeBlock((x-1, roof_y_start + i, z + WIDTH -1 -j), Block(ROOF_PLANK_MATERIAL))
             editor.placeBlock((x+LENGTH, roof_y_start + i, z + WIDTH -1 - j), Block(ROOF_PLANK_MATERIAL))


    # Add the roof ridge
    ridge_y = roof_y_start + roof_height - 1
    ridge_z = z + WIDTH // 2
    for dx in range(-1, LENGTH + 1):
        editor.placeBlock((x + dx, ridge_y, ridge_z), Block(ROOF_SLAB_MATERIAL))

    # --- Add Interior Furnishings ---
    print("Furnishing the cottage...")
    # Bed
    editor.placeBlock((x + 1, y + 1, z + WIDTH - 2), Block(BED_MATERIAL, {"part": "foot", "facing": "east"}))
    editor.placeBlock((x + 2, y + 1, z + WIDTH - 2), Block(BED_MATERIAL, {"part": "head", "facing": "east"}))
    # Chest
    editor.placeBlock((x + 1, y + 1, z + WIDTH - 3), Block(CHEST_MATERIAL))
    # Crafting and Furnace
    editor.placeBlock((x + LENGTH - 2, y + 1, z + 1), Block(CRAFTING_MATERIAL))
    editor.placeBlock((x + LENGTH - 2, y + 1, z + 2), Block(FURNACE_MATERIAL))
    # Torch
    editor.placeBlock((x + LENGTH // 2, y + 4, z + 1), Block(LIGHTING_MATERIAL))


    print("Miner's Cottage build complete!")

# --- Main Execution ---
if __name__ == '__main__':
    try:
        start_x, start_y, start_z = 6616, -60, -233

        build_miners_cottage(start_x, start_y, start_z)

        print("Sending all commands to Minecraft...")
        editor.flushBuffer()
        print("Done!")

    except Exception as e:
        print(f"An error occurred: {e}")