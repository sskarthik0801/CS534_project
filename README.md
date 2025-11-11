_**Below is the base tasks and milestones:**_

Module 1 – Simulation & Environment Setup
Goal: Build a working simulation ecosystem 


Module 2 – Vision / Terrain Perception
Goal: Implement the DeepLabV3+ segmentation network for terrain classification.

Tasks:
Fine-tune pretrained DeepLabV3+ (ResNet18 backbone) on Cityscapes + Gazebo terrain data.
Develop a ROS node to perform real-time semantic segmentation from camera feed.
Output a label map with terrain classes: road, grass, rock, sand, etc.
Publish segmentation as a /terrain_class_map topic.

Deliverables:
Trained segmentation model.
ROS node publishing per-pixel class map.
Evaluation metrics (IoU, pixel accuracy).

Module 3 – Dynamic Terrain Difficulty Estimation (Novelty Module)
Goal: Convert perception + physics data into a continuous cost map.

Tasks:
Access Gazebo heightmap to compute slope/incline.
Extract or assign surface friction coefficients for materials.
Fuse these physics parameters with vision classes → compute a difficulty score per pixel.
Normalize cost values (0–1 scale) and publish as /cost_map.
Optional: integrate probabilistic risk (CVaR-based adjustment).

Deliverables:
Physics-aware cost map node.
Visualization script (cost heatmap overlay on terrain).
Validation plots comparing slope vs. cost.

Module 4 – Path Planning & System Integration
Goal: Implement planner + integrate all modules into a full ROS pipeline.

Tasks:
Implement A* and RRT* planners that subscribe to /cost_map.
Generate optimal path minimizing cumulative traversal cost.
Send waypoints/motion commands to rover controller.
Create unified launch file combining perception → cost → planning nodes.
Run full-system tests on multiple terrains and collect metrics.

Deliverables:
Functional A*/RRT* planner node.
Integrated ROS launch setup.
Evaluation report: traversal time, energy cost, risk metrics.


1. works