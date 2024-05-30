# Pipeline for Diffusion-Derived Features

This document describes the processing pipeline for diffusion MRI data. 
The scripts can be found in: [RATNUS - DMRI Pipeline](https://github.com/ANQIFENG/RATNUS/tree/main/processing_pipelines/dmri_pipeline).


## Steps Overview

The pipeline consists of two main steps:

1. **Step 00: Running TORTOISE**
   - In this step, TORTOISE is used to preprocess the diffusion MRI data.
   - The following TORTOISE modules are used:
     - **DIFFPREP**: Distortion and motion correction
     - **DR-BUDDI**: EPI distortion correction module
     - **DIFFCALC**: Tensor fitting and scalar maps calculation
   - For more details, please refer to [TORTOISE website](https://tortoise.nibib.nih.gov/tortoise).

2. **Step 01: Calculating Knutsson 5D Vectors and Edge Map**
   - This step uses the eigenvector calculated from step00 to compute the Knutsson 5D vectors and the edge map. 



## Data Structure

The data structure used in the scripts is organized as follows:

- **Study Directory** (e.g., `mtbi_study`)
  - **Subject Directory** (e.g., `MTBI-0001`, `MTBI-0002`, ...)
    - **Session Directory** (e.g., `v1`, `v2`, `v3`)
      - **Raw Data Directory** (`nii`)
      - **Processed Data Directory** (`proc`)

Here is a visual representation of the data structure:
``````
mtbi_study/
├── MTBI-0001/
│ ├── v1/
│ │ ├── nii/
│ │ └── proc/
│ ├── v2/
│ │ ├── nii/
│ │ └── proc/
│ └── v3/
│ ├── nii/
│ └── proc/
├── MTBI-0002/
│ ├── v1/
│ │ ├── nii/
│ │ └── proc/
│ ├── v2/
│ │ ├── nii/
│ │ └── proc/
│ └── v3/
│ ├── nii/
│ └── proc/
...
``````

## Data Description

In this study, we have two types of diffusion MRI data stored in the `nii` folder:

1. **B0 Image (`DIFF_*_B0_*`)**
   - **Phase-encoding Direction**: Posterior-Anterior (PA) 
   - **B-values**: 0
   - **In-plane Resolution**: 2mm

2. **High b-value Image (`DIFF_*_BMAX2500_*`)**
   - **Phase-encoding Direction**: Anterior-Posterior (AP) view
   - **B-values**: 0, 1000, 2500
   - **Encoding Directions**: 136 directions 
   - **In-plane Resolution**: 2mm

The B0 image in PA view is only used for EPI distortion correction in Tortoise DR BUDDI module. 
All images are collected using a 3T Siemens Prisma scanner.

Additionally, T2-weighted images are required in the step00, specifically the DIFFPREP and DRBUDDI modules. 
Our T2 images are in MNI space with 1mm resolution,  and have undergone N4 bias field correction and white matter mean normalization.

## Expected output

The output files relevant for our analysis are:

- `*_DT_FA.nii` - Fractional Anisotropy (FA)
- `*_DT_AD.nii` - Axial Diffusivity (AD)
- `*_DT_RD.nii` - Radial Diffusivity (RD)
- `*_DT_TR.nii` - Trace
- `*_DT_WL.nii` - Linear Anisotropy (WL)
- `*_DT_WP.nii` - Planar Anisotropy (WP)
- `*_DT_WS.nii` - Spheric Anisotropy (WS)
- `*_knutsson_5D.nii` - Knutsson 5D Vector
- `*_knutsson_edgemap.nii` - Knutsson Edge Map