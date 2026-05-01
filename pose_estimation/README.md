# 6DoF Pose Estimation Pipeline — MegaPose + GroundingDINO

Pose estimation for tabletop manipulation using RAI simulator, GroundingDINO detection, and MegaPose RGB-D refinement.

---

## Server

- **Host:** mimir (accessed via SSH)
- **GPU:** 2× NVIDIA RTX 6000 Ada (48 GB each)
- **CUDA:** 12.2
- **Python:** 3.10 (conda env `megapose_env`)

---

## Installation Steps

### 1. Conda Environment

```bash
conda create -n megapose_env python=3.10
conda activate megapose_env
```

### 2. PyTorch (CUDA 12.1)

```bash
pip install torch==2.5.1+cu121 torchvision --index-url https://download.pytorch.org/whl/cu121
```

### 3. Core Dependencies

```bash
pip install trimesh scipy opencv-python pandas pillow
```

> **Note:** Before any C extension builds, unset compiler vars injected by conda:
> ```bash
> unset CC CXX CFLAGS
> ```
> Failing to do this causes cryptic build errors.

### 4. robotic (RAI Framework)

```bash
pip install robotic
```

### 5. GroundingDINO

```bash
cd ~/rai_workspace
git clone https://github.com/IDEA-Research/GroundingDINO.git
cd GroundingDINO
pip install --no-build-isolation -e .
```

> **Note:** `--no-build-isolation` is required — the standard build fails.

Download weights:

```bash
mkdir -p ~/rai_workspace/grounding_dino_weights
cd ~/rai_workspace/grounding_dino_weights
wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth   # 662 MB
# also download the config:
wget https://raw.githubusercontent.com/IDEA-Research/GroundingDINO/main/groundingdino/config/GroundingDINO_SwinT_OGC.py
```

### 6. cosypose (MegaPose dependency — not on PyPI)

```bash
cd ~/rai_workspace
git clone https://github.com/ylabbe/cosypose.git
# Add to PYTHONPATH (C extension not needed for MegaPose)
echo 'export PYTHONPATH=$PYTHONPATH:~/rai_workspace/cosypose' >> ~/.bashrc
```

### 7. happypose (MegaPose)

```bash
cd ~/rai_workspace
git clone https://github.com/agimus-project/happypose.git
cd happypose
pip install -e ".[megapose]"
```

> **Note:** `bop_toolkit_lib` is also not on PyPI — it is bundled inside happypose source.

### 8. MegaPose Weights

```bash
mkdir -p ~/happypose_data/megapose-models
# Download from the happypose model zoo (coarse-rgb, refiner-rgb, refiner-rgbd, ~83 MB each)
python -m happypose.toolbox.utils.download --megapose_models
```

### 9. YOLO (optional, used for alternative detection)

```bash
pip install ultralytics
```

---

## Environment Variables

Add to `~/.bashrc`:

```bash
export HAPPYPOSE_DATA_DIR=~/happypose_data
export PYTHONPATH=$PYTHONPATH:~/rai_workspace/cosypose
```

Then reload:

```bash
source ~/.bashrc
```

> **Jupyter notebooks** do not inherit `~/.bashrc`. Set the variable explicitly at the top of any notebook cell before importing happypose:
> ```python
> import os
> os.environ["HAPPYPOSE_DATA_DIR"] = "/home/salman/happypose_data"
> ```

---

## Project Structure

```
Project/
├── environments/
│   ├── gfiles/
│   │   └── mesh_clutter_high_30.g      # RAI scene file
│   └── mesh_dataset/
│       └── lamp/
│           └── lamp_0001.ply           # raw mesh (converted from .off)
├── megapose_objects/
│   └── lamp/
│       └── mesh.ply                    # scaled mesh (metres) for MegaPose
├── outputs/
│   ├── rgb/                            # rendered camera images
│   ├── depth/                          # rendered depth maps (.npy)
│   ├── camera_info.json                # intrinsics + extrinsics per camera
│   └── pose_visualization.png          # final result overlay
└── scripts/
    ├── step1_prepare_mesh.ipynb        # scale mesh to metres
    ├── step2_capture_images.ipynb      # render RGB + depth from RAI
    └── step3_pose_estimation.ipynb     # detect + estimate 6DoF pose
```

---

## Pipeline

Run the notebooks in order:

| Step | Notebook | What it does |
|------|----------|--------------|
| 1 | `step1_prepare_mesh.ipynb` | Scales `lamp_0001.ply` by `0.000271579` (meshscale from `.g` file) → metres |
| 2 | `step2_capture_images.ipynb` | Loads RAI scene, removes robot arm, renders RGB + depth from 5 cameras at 5 m distances |
| 3 | `step3_pose_estimation.ipynb` | Detects lamp with GroundingDINO, runs MegaPose coarse + RGB-D refiner, outputs 6DoF pose in world frame |

---

## Known Gotchas

| Issue | Fix |
|-------|-----|
| RAI `addFile()` doesn't accept absolute paths | `os.chdir()` to the `.g` file's directory before `ry.Config()`, then pass just the filename |
| RAI captures CWD at `ry.Config()` creation | Call `os.chdir()` **before** `ry.Config()`, not after |
| `HAPPYPOSE_DATA_DIR` not set in Jupyter | Set `os.environ["HAPPYPOSE_DATA_DIR"]` in a notebook cell before importing happypose |
| GroundingDINO build fails | Use `pip install --no-build-isolation -e .` |
| C extension build errors in conda | Run `unset CC CXX CFLAGS` before any `pip install` with C extensions |
| `cosypose` / `bop_toolkit_lib` not on PyPI | Install cosypose from source and add to `PYTHONPATH` |

---

## Scene Details

- **Scene file:** `environments/gfiles/mesh_clutter_high_30.g`
- **Object of interest:** `goal_yellow_lamp_9_mesh` (mesh: `lamp_0001.off`, meshscale: `0.000271579`)
- **True object pose** (world frame): `[-0.620966, -0.342511, 0.671156, 0.287543, -0.46152, 0.714029, 0.441]`
- **Target/goal pose** (world frame): `[0.219547, 0.280159, 0.698313, 0.38692, 0.0, 0.0, -0.922113]`
- **Table:** 1.6 × 1.6 m at z = 0.6 m
