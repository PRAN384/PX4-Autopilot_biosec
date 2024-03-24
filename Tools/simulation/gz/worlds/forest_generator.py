import random
n = 1
m = 1
def generate_forest():
    # Define the trees and their properties
    trees = [
        {"type": 2, "height": 11.3, "diameter": 7.23, "quantity": 5*n},
        {"type": 3, "height": 5.7, "diameter": 6.0, "quantity": 7*n},
        {"type": 1, "height": 6, "diameter": 3.7, "quantity": 7*n},
        {"type": 5, "height": 5.3, "diameter": 3.2, "quantity": 7*n},
        {"type": 4, "height": 22, "diameter": 2.7, "quantity": 4*n},
        {"type": 8, "height": 22, "diameter": 2.7, "quantity": 4*n},
        {"type": 7, "height": 7, "diameter": 2, "quantity": 10*n},
        {"type": 9, "height": 16.8, "diameter": 1.2, "quantity": 15*n},
        {"type": 6, "height": 1, "diameter": 0.3, "quantity": 15*n}
    ]


    bushes = [
        {"type": 0, "height": 3, "diameter": 1, "quantity": 5*m},
        {"type": 1, "height": 4, "diameter": 1, "quantity": 5*m},
        {"type": 2, "height": 1, "diameter": 1, "quantity": 5*m},
        {"type": 3, "height": 2, "diameter": 1, "quantity": 5*m},
        {"type": 4, "height": 3, "diameter": 1, "quantity": 5*m},
        {"type": 5, "height": 3.5, "diameter": 1, "quantity": 5*m}
    ]


    # Forest size
    forest_size = 10  # 25x25 meters
    half_forest_size = forest_size / 2

    sdf_elements = []

    # Function to check if a new position is valid (no overlap)
    def is_valid_position(x, y, diameter):
        # Check for exclusion zone around (0, 0)
        exclusion_zone_radius = 2.5
        if ((x - 0) ** 2 + (y - 0) ** 2) ** 0.5 < exclusion_zone_radius:
            return False

        # Check for overlaps with other elements
        for element in sdf_elements:
            dist = ((element["x"] - x) ** 2 + (element["y"] - y) ** 2) ** 0.5
            min_dist = (element["diameter"] + diameter) / 2
            if dist < min_dist:
                return False

        return True


    # Place trees
    for tree in trees:
        placed_count = 0
        attempts = 0
        while placed_count < tree["quantity"] and attempts < 1000:
            x = random.uniform(-half_forest_size, half_forest_size) 
            y = random.uniform(-half_forest_size, half_forest_size) 
            if is_valid_position(x, y, tree["diameter"]):
                sdf_elements.append({
                    "type": "tree",
                    "tree_type": tree["type"],
                    "x": x,
                    "y": y,
                    "diameter": tree["diameter"]
                })
                placed_count += 1
            attempts += 1

    # Place bushes
    for bush in bushes:
        placed_count = 0
        attempts = 0
        while placed_count < bush["quantity"] and attempts < 100000:
            x = random.uniform(-half_forest_size, half_forest_size)
            y = random.uniform(-half_forest_size, half_forest_size)
            if is_valid_position(x, y, bush["diameter"]):
                sdf_elements.append({
                    "type": "bush",
                    "bush_type": bush["type"],
                    "x": x,
                    "y": y,
                    "diameter": bush["diameter"]
                })
                placed_count += 1
                print(f"Bush {bush['type']} added at ({x}, {y})")  # Diagnostic print
            attempts += 1

    return sdf_elements

def create_sdf_content(elements):
    
    sdf_content = ""
    with open('static_content.sdf', 'r') as file:
        sdf_content = file.read()
    tree_count = {}
    bush_count = {}

    for element in elements:
        if element["type"] == "tree":
            tree_type = element["tree_type"]
            tree_count[tree_type] = tree_count.get(tree_type, 0) + 1
            identifier = tree_count[tree_type]
            sdf_content += (
                f"    <include>\n"
                f"      <uri>file:///home/ubuntu22/PX4-Autopilot_biosec/Tools/simulation/gz/worlds/tree_{tree_type}</uri>\n"
                f"      <name>tree {tree_type}{identifier}</name>\n"
                f"      <pose>{element['x']} {element['y']} 0 1.5708000000000006 0 0</pose>\n"
                f"    </include>\n\n"
            )
        elif element["type"] == "bush":
            bush_type = element["bush_type"]
            bush_count[bush_type] = bush_count.get(bush_type, 0) + 1
            identifier = bush_count[bush_type]
            sdf_content += (
                f"    <include>\n"
                f"      <uri>file:///home/ubuntu22/PX4-Autopilot_biosec/Tools/simulation/gz/worlds/bush_{bush_type}</uri>\n"
                f"      <name>bush {bush_type}{identifier}</name>\n"
                f"      <pose>{element['x']} {element['y']} 0 1.5708000000000006 0 0</pose>\n"
                f"    </include>\n\n"
            )
    sdf_content += "  </world>\n</sdf>\n"
    return sdf_content




# Generate the forest elements
forest_elements = generate_forest()

# Create SDF content
sdf_content = create_sdf_content(forest_elements)


with open('grass_world.sdf', 'w') as file:
    file.write(sdf_content)

print("Complete SDF file has been created and saved.")
# Print the first few lines of the SDF content for preview
# print(sdf_content)  # Print first 500 characters for brevity