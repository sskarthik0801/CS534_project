import numpy as np

# This script generates the mock input files that Module 1 (Karthi)
# will provide. It simulates a world with Mapbox-like features.

SHAPE = (200, 200)

def generate_mock_world_files():
    print(f"Generating mock world files with shape {SHAPE}...")

    # 1. Create the Heightmap (Elevation Data)
    # ---------------------------------------------
    # Start with a base elevation
    heightmap = np.ones(SHAPE) * 10.0  # Base "ground" is 10 units high

    # Add a steep ridge on the right side
    # It will ramp from 10 units to 60 units high
    ramp = np.linspace(10, 60, SHAPE[1] // 2)
    heightmap[:, SHAPE[1] // 2:] = ramp

    # Add a road (10 pixels wide) with its own gentle slope
    # This "carves" through the ridge
    road_slope = np.linspace(10, 20, SHAPE[1]) # Road gently rises 10 units
    heightmap[95:105, :] = road_slope

    # 2. Create the Class Map (Terrain Type)
    # ---------------------------------------------
    # Use the codes from your config.py
    # Default to "Grass" (Code 3)
    class_map = np.ones(SHAPE, dtype=int) * 3

    # Add the "Rocky" (Code 5) region on the steep ridge
    class_map[:, SHAPE[1] // 2:] = 5
    
    # Add a "Sand" (Code 4) patch on the flat side
    class_map[20:70, 20:70] = 4

    # Add the "Road" (Code 1)
    class_map[95:105, :] = 1

    # 3. Save the Files
    # ---------------------------------------------
    np.save("heightmap.npy", heightmap)
    np.save("class_map.npy", class_map)
    
    print("...Done!")
    print("Created 'heightmap.npy' and 'class_map.npy'.")
    print("You can now run your cost_map_prototype.py script.")

if __name__ == "__main__":
    generate_mock_world_files()