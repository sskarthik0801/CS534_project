# This file contains the static configuration for Module 3.

import numpy as np

# This maps the "Mask code" to a friction value (mu).
# Based on the new plan, these codes come from the static Mapbox/Gazebo world.
FRICTION_LOOKUP = {
    # Mask Code: Friction Value (mu)
    1: 0.7,   # Road (Assuming 0.7 is low cost, e.g., 1.0 - 0.7 = 0.3 cost)
              # Let's re-think: If mu=friction, 0.7 is high.
              # Let's assume the number IS the cost. Road=0.1, Mud=0.9
              # I will update this table to be more intuitive:
              # Low number = Low Cost (Easy to traverse)
              # High number = High Cost (Hard to traverse)
    
    # Class Code: Cost (0.0 to 1.0)
    1: 0.1,   # Road
    2: 0.9,   # Dense;Woody;Features
    3: 0.3,   # Grass
    4: 0.6,   # Terrain (Sand)
    5: 0.8,   # Mountain (Rocky)
    6: 0.7,   # Plant;Bush
    7: 0.4,   # Cropfield (Soil)
    8: 0.9,   # Ditch (Muddy)
    9: 0.2,   # Terrace (Bricks)
    0: 1.0    # Default/Unknown (Max cost)
}

# For the prototype, we can also define the class names for plotting
CLASS_NAMES = {
    1: "Road",
    2: "Woody",
    3: "Grass",
    4: "Sand",
    5: "Rocky",
    6: "Bush",
    7: "Soil",
    8: "Mud",
    9: "Bricks",
    0: "Unknown"
}

# Tunable weights for the cost-fusion formula
# Cost = w1*slope_cost + w2*terrain_cost
WEIGHT_SLOPE = 0.6
WEIGHT_TERRAIN = 0.4