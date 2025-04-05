# Point2Tree

![Tree Crown Point Cloud Example](https://github.com/xzx0554/Point2Tree/blob/main/doc/images/cover.png?raw=true)

A self-prior point cloud reconstruction model for:

- Tree crown volume calculation
- 3D reconstruction of tree crowns
- Tree crown projection area calculation

## 1.Features

- High-accuracy crown volume estimation
- Parameter-free
- Automated 3D modeling from LiDAR/point clouds
- Cross-section analysis & projection mapping
- Low VRAM usage & fast processing
- Training-free for all tree species

## 2. Usage

### Prerequisites

* Requires **PyTorch** ≥2.0 (versions below 2.0 not supported)
* Requires **PyTorch3D** ==0.7.5

### Step 1: Convert XYZ to PLY

Run `xyz2ply` under the `tools` directory to convert your XYZ point cloud file (first three columns as XYZ coordinates) to a PLY file with normal vectors.

### Step 2: Get Mesh Face Count

Execute `get_mesh_number.py` in `tools/get_mesh_num/`. You must modify the path to your target folder. Note this is a modified version of Adtree - if execution fails, please recompile. The original Adtree cannot retrieve face counts.

### Step 3: Batch Convex Hull Processing

Run `convex_hull_batch.py` after:

1. Setting your target folder path
2. Specifying your face count CSV file path
3. Compiling Manifold ([Robust Watertight Manifold Software](https://github.com/hjwdzh/Manifold)) under the `code` directory

### Step 4: Simulation Execution

Run `simulate.py` with these configurable options:
• Multi-threading support: Set the number of parallel processes per device
• Multi-GPU support: Configure the number of GPUs to utilize
• Progress notifications: Enable and configure notification settings as needed

For optimal performance:

1. Adjust thread/GPU counts according to your hardware specifications
2. Allocate sufficient memory for large datasets
3. Monitor system resources during execution

## 3. Evaluation

| Method          | Real-world Dataset (3,000+ trees) | ForInstance-999 Dataset | Synthetic Dataset (Include True Label) |
|-----------------|----------------------------------|-------------------------|-------------------------------------|
| **Point2Tree**  | ✅smallest                        | ✅ smallest                              | ✅ Best|
| Voxel-based     | -                               | -                       | -                                   |
| Graham Slicing  | -                               | -                       | -                                   |
| Convex Hull     | -                               | -                       | -                                   |

*Key: ✅ = Our method performs better than the baseline approaches in both volume estimation and projection area calculation*

| Method          | Volume Estimation | Projection Area |
|-----------------|-------------------|-----------------|
| **Point2Tree**  | ✅ smallest| ✅ smallest|
| Voxel-based     | -                 | -               |
| Graham Slicing  | -                 | -               |
| Convex Hull     | -                 | -               |

*Note: Demonstrated superior performance across all test datasets (3,000+ real trees, ForInstance-999, and synthetic Blender models) compared to traditional methods*

## 4. Performance

<p align="left">
  <strong>I. GPU Memory Usage Comparison</strong><br>
  <img src="https://github.com/xzx0554/Point2Tree/raw/main/doc/images/gpu_usage.png" width="500" style="max-height: 300px" alt="GPU Memory Comparison"><br>
  <em>Point2Tree reduces GPU memory consumption by 50% compared to Point2Mesh (4.2GB vs 8.5GB).</em>
</p>

<p align="left">
  <strong>II. Processing Time Comparison</strong><br>
  <img src="https://github.com/xzx0554/Point2Tree/raw/main/doc/images/processing_time.png" width="500" style="max-height: 300px" alt="Processing Time"><br>
  <em>Point2Tree achieves 2× faster processing speed (35ms vs 70ms per iteration).</em>
</p>
