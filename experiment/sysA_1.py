from gdpc import Editor, Block, Transform, geometry

editor = Editor(buffering=True)

def place_octagonal_ring(x, y, z, diameter, material):
    """
Places
a
single
layer
of
an
octagon.
"""
    radius = diameter // 2
    # This is a simplified block-based octagon algorithm
    for i in range(-radius, radius + 1):
        # Top and bottom edges
        width = radius * 2 + 1 - (abs(i) // 2 * 4)
        if width > radius * 2 +1:
             width = radius * 2 + 1
        if diameter % 4 == 0 and abs(i) > radius -2:
             width -=2
        elif diameter % 4 == 1 and abs(i) > radius -2:
             width -=2
        elif diameter % 4 == 2 and abs(i) > radius -1:
             width -=1
        elif diameter % 4 == 3 and abs(i) > radius -1:
             width -=1
        start_x = x - width // 2
        for j in range(width):
            editor.placeBlock((start_x + j, y, z + i), Block(material))

def place_octagonal_walls(x, y, z, d, h, wall_mat, accent_mat, window_mat, shutter_mat, door_mat):
    """
Builds
the
octagonal
walls
with windows and a door."""
    for yy in range(h):
        # Determine material for the current layer
        current_wall_material = accent_mat if yy == 0 or yy == h - 1 else wall_mat

        radius = d // 2
        # Top and bottom sides
        for i in range(-2, 3):
            editor.placeBlock((x + i, y + yy, z + radius), Block(current_wall_material))
            editor.placeBlock((x + i, y + yy, z - radius), Block(current_wall_material))
        # Left and right sides
        for i in range(-2, 3):
             editor.placeBlock((x + radius, y + yy, z + i), Block(current_wall_material))
             editor.placeBlock((x - radius, y + yy, z + i), Block(current_wall_material))
        # Diagonal sections
        for i in range(1, 5):
            editor.placeBlock((x + radius - i, y + yy, z + radius - (5-i)), Block(current_wall_material))
            editor.placeBlock((x - radius + i, y + yy, z + radius - (5-i)), Block(current_wall_material))
            editor.placeBlock((x + radius - i, y + yy, z - radius + (5-i)), Block(current_wall_material))
            editor.placeBlock((x - radius + i, y + yy, z - radius + (5-i)), Block(current_wall_material))

    # Place Door
    editor.placeBlock((x, y, z + d//2), Block("air"))
    editor.placeBlock((x, y + 1, z + d//2), Block("air"))
    editor.placeBlock((x, y, z + d//2), Block(door_mat, {"half": "lower", "facing": "south"}))
    editor.placeBlock((x, y + 1, z + d//2), Block(door_mat, {"half": "upper", "facing": "south"}))

    # Place Windows and Shutters
    window_y = y + 3
    # Back Window
    editor.placeBlock((x, window_y, z - d//2), Block(window_mat))
    editor.placeBlock((x, window_y+1, z - d//2), Block(window_mat))
    editor.placeBlock((x - 1, window_y, z - d//2), Block(shutter_mat, {"facing": "east", "open": "true"}))
    editor.placeBlock((x + 1, window_y, z - d//2), Block(shutter_mat, {"facing": "west", "open": "true"}))
    editor.placeBlock((x - 1, window_y+1, z - d//2), Block(shutter_mat, {"facing": "east", "open": "true"}))
    editor.placeBlock((x + 1, window_y+1, z - d//2), Block(shutter_mat, {"facing": "west", "open": "true"}))

    # Left Window
    editor.placeBlock((x - d//2, window_y, z), Block(window_mat))
    editor.placeBlock((x - d//2, window_y+1, z), Block(window_mat))
    editor.placeBlock((x - d//2, window_y, z - 1), Block(shutter_mat, {"facing": "south", "open": "true"}))
    editor.placeBlock((x - d//2, window_y, z + 1), Block(shutter_mat, {"facing": "north", "open": "true"}))
    editor.placeBlock((x - d//2, window_y+1, z - 1), Block(shutter_mat, {"facing": "south", "open": "true"}))
    editor.placeBlock((x - d//2, window_y+1, z + 1), Block(shutter_mat, {"facing": "north", "open": "true"}))

    # Right Window
    editor.placeBlock((x + d//2, window_y, z), Block(window_mat))
    editor.placeBlock((x + d//2, window_y+1, z), Block(window_mat))
    editor.placeBlock((x + d//2, window_y, z - 1), Block(shutter_mat, {"facing": "south", "open": "true"}))
    editor.placeBlock((x + d//2, window_y, z + 1), Block(shutter_mat, {"facing": "north", "open": "true"}))
    editor.placeBlock((x + d//2, window_y+1, z - 1), Block(shutter_mat, {"facing": "south", "open": "true"}))
    editor.placeBlock((x + d//2, window_y+1, z + 1), Block(shutter_mat, {"facing": "north", "open": "true"}))

def build_cone_roof(x, y, z, diameter, height, plank_mat, stair_mat):
    """Builds a cone-shaped roof."""
    base_radius = diameter // 2
    for yy in range(height):
        current_radius = base_radius - (yy // 2)
        if current_radius < 0:
            current_radius = 0

        # Create rings of stairs
        y_pos = y + yy

        # Simplified cone algorithm
        for i in range(-current_radius, current_radius + 1):
            for j in range(-current_radius, current_radius + 1):
                if int((i**2 + j**2)**0.5) == current_radius:
                    # Place blocks for the ring
                    # Determine stair facing direction
                    if abs(i) > abs(j):
                        if i > 0:
                            facing = "south"
                        else:
                            facing = "north"
                    else:
                        if j > 0:
                            facing = "east"
                        else:
                            facing = "west"
                    editor.placeBlock((x + j, y_pos, z + i), Block(stair_mat, {"facing": facing}))

    # Place the capstone
    editor.placeBlock((x, y + height, z), Block(plank_mat))

def add_furnishings(x, y, z, bed_mat, chest_mat, craft_mat, furnace_mat, shelf_mat, light_mat):
    """Adds furniture and decorations to the interior."""
    # Place Bed
    editor.placeBlock((x + 5, y, z + 5), Block(bed_mat, {"part": "foot", "facing": "north"}))
    editor.placeBlock((x + 5, y, z + 4), Block(bed_mat, {"part": "head", "facing": "north"}))

    # Place Storage and Crafting Area
    editor.placeBlock((x - 5, y, z + 5), Block(craft_mat))
    editor.placeBlock((x - 6, y, z + 5), Block(furnace_mat))
    editor.placeBlock((x - 5, y, z + 4), Block(chest_mat))
    editor.placeBlock((x - 6, y, z + 4), Block(chest_mat))

    # Place Bookshelves
    for i in range(4):
        editor.placeBlock((x - 6 + i, y, z - 6), Block(shelf_mat))
        editor.placeBlock((x - 6 + i, y + 1, z - 6), Block(shelf_mat))

    # Place central lantern
    editor.placeBlock((x, y + 7, z), Block("chain"))
    editor.placeBlock((x, y + 6, z), Block(light_mat))

def build_woolen_retreat(x, y, z):
    """Main function to build the entire woolen house."""
    DIAMETER = 17
    WALL_HEIGHT = 8
    ROOF_HEIGHT = 10

    # Materials
    floor_material = "birch_planks"
    wall_material = "white_wool"
    accent_material = "light_gray_wool"
    window_material = "glass_pane"
    shutter_material = "spruce_trapdoor"
    door_material = "spruce_door"
    roof_plank_material = "spruce_planks"
    roof_stair_material = "spruce_stairs"
    pillar_material = "dark_oak_log"

    # Furniture Materials
    bed_material = "red_bed"
    chest_material = "chest"
    crafting_material = "crafting_table"
    furnace_material = "furnace"
    bookshelf_material = "bookshelf"
    lantern_material = "lantern"

    # Build Foundation and Floor
    print("Building floor...")
    radius = DIAMETER // 2
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if (i**2 + j**2)**0.5 <= radius:
                editor.placeBlock((x + i, y -1, z + j), Block(floor_material))

    # Build Walls
    print("Building walls...")
    place_octagonal_walls(x, y, z, DIAMETER, WALL_HEIGHT, wall_material, accent_material, window_material, shutter_material, door_material)

    # Build Roof
    print("Building roof...")
    build_cone_roof(x, y + WALL_HEIGHT, z, DIAMETER, ROOF_HEIGHT, roof_plank_material, roof_stair_material)

    # Add central pillar
    print("Adding support pillar...")
    for i in range(WALL_HEIGHT + ROOF_HEIGHT - 1):
        editor.placeBlock((x, y + i, z), Block(pillar_material))

    # Add Furnishings
    print("Adding furniture...")
    add_furnishings(x, y, z, bed_material, chest_material, crafting_material, furnace_material, bookshelf_material, lantern_material)

    print("Woolen Retreat build complete!")

# Example usage:
if __name__ == '__main__':
    try:
        x, y, z = 3516, -60, -233

        # Call the main build function
        build_woolen_retreat(x, y, z)

        # Manually send all buffered commands to Minecraft
        editor.flushBuffer()

    except Exception as e:
        print(f"An error occurred: {e}")