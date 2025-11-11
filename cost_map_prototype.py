import numpy as np
import matplotlib.pyplot as plt
from config import FRICTION_LOOKUP, WEIGHT_SLOPE, WEIGHT_TERRAIN, CLASS_NAMES

def calculate_slope_map(heightmap):
    """
    Calculates slope from a heightmap.
    Returns a normalized slope map (0-1), where 0 is flat and 1 is steep.
    """
    # Calculate the gradient in the x and y directions
    gy, gx = np.gradient(heightmap)
    
    # Calculate the slope magnitude
    slope = np.sqrt(gx**2 + gy**2)
    
    # Normalize the slope to 0-1 range to be used as a cost
    min_slope = np.min(slope)
    max_slope = np.max(slope)
    if max_slope - min_slope == 0:
        return np.zeros_like(slope) # Avoid division by zero if flat
        
    norm_slope = (slope - min_slope) / (max_slope - min_slope)
    return norm_slope

def vectorized_friction_lookup(class_map, lookup_table):
    """
    Converts the entire class_map to a terrain_cost_map using the lookup table.
    """
    # Create an array of all possible class IDs (0-9)
    max_id = max(lookup_table.keys())
    
    # Create a mapping array (vector) where the index = class ID
    # and the value = terrain cost (friction)
    lookup_vector = np.zeros(max_id + 1)
    for class_id, cost in lookup_table.items():
        lookup_vector[class_id] = cost
    
    # Use the class_map as indices to pull values from the lookup_vector
    terrain_cost_map = lookup_vector[class_map]
    return terrain_cost_map

def calculate_cost_map(slope_map, terrain_cost_map, w_slope, w_terrain):
    """
    Applies the core fusion formula.
    Cost = w1*slope_cost + w2*terrain_cost
    """
    # The inputs are already normalized (0-1), so we just apply weights
    cost_map = (w_slope * slope_map) + (w_terrain * terrain_cost_map)
    
    # Final normalization to get a 0-1 cost map
    # This ensures the final map is easy for the planner to use
    final_cost_map = (cost_map - np.min(cost_map)) / (np.max(cost_map) - np.min(cost_map))
    
    return final_cost_map

def visualize_prototype(height_map, class_map, terrain_cost_map, cost_map):
    """
    Uses Matplotlib to visualize all the inputs and the final output.
    """
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Module 3: Cost-Map Fusion Prototype (Offline)", fontsize=16)

    # 1. Plot Heightmap
    ax = axes[0, 0]
    im = ax.imshow(height_map, cmap='terrain')
    ax.set_title("Input 1: Heightmap (from Module 1)")
    ax.set_xlabel("Low (green) -> High (white)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # 2. Plot Class Map
    ax = axes[0, 1]
    im = ax.imshow(class_map, cmap='tab10', vmin=0, vmax=9)
    ax.set_title("Input 2: Class Map (from Module 1)")
    # Create a custom colorbar with labels
    ticks = list(CLASS_NAMES.keys())
    tick_labels = list(CLASS_NAMES.values())
    cbar = fig.colorbar(im, ax=ax, ticks=ticks, fraction=0.046, pad=0.04)
    cbar.set_ticklabels(tick_labels)

    # 3. Plot Intermediate Terrain Cost Map
    ax = axes[1, 0]
    im = ax.imshow(terrain_cost_map, cmap='Reds', vmin=0, vmax=1)
    ax.set_title("Intermediate: Terrain Cost Map")
    ax.set_xlabel("0.0 (low cost) -> 1.0 (high cost)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    # 4. Plot Final Cost Map
    ax = axes[1, 1]
    im = ax.imshow(cost_map, cmap='jet', vmin=0, vmax=1)
    ax.set_title("OUTPUT: Final Fused Cost Map")
    ax.set_xlabel("Blue (low cost) -> Red (high cost)")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    
    # Add text to show the path of least cost
    ax.text(100, 100, "<- Path of Least Cost (Road)", color='white', ha='center',
            bbox=dict(facecolor='black', alpha=0.5))
    ax.text(175, 175, "High Cost\n(Steep & Rocky)", color='black', ha='center',
            bbox=dict(facecolor='white', alpha=0.5))

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

def main():
    print("Running Module 3 Prototype...")
    
    # 1. Load mock inputs from files
    print("Loading world files from mock Module 1...")
    try:
        class_map = np.load("class_map.npy")
        height_map = np.load("heightmap.npy")
    except FileNotFoundError:
        print("Error: Files not found.")
        print("Please run 'generate_mock_world.py' first!")
        return

    # 2. Calculate Slope Map (The NEW step)
    print("Calculating slope map from heightmap...")
    slope_map = calculate_slope_map(height_map)
    
    # 3. Convert class map to friction map (Same as before)
    print("Calculating terrain cost map from class map...")
    terrain_cost_map = vectorized_friction_lookup(class_map, FRICTION_LOOKUP)
    
    # 4. Run the fusion formula (Same as before)
    print("Fusing maps into final cost map...")
    cost_map = calculate_cost_map(
        slope_map,
        terrain_cost_map,
        WEIGHT_SLOPE,
        WEIGHT_TERRAIN
    )
    
    # 5. Save the final map for Module 4 (Niranjan)
    np.save("final_cost_map.npy", cost_map)
    print("...Final 'final_cost_map.npy' saved for Module 4.")
    print("...Showing visualization.")
    
    # 6. Visualize results
    visualize_prototype(height_map, class_map, terrain_cost_map, cost_map)

if __name__ == "__main__":
    main()