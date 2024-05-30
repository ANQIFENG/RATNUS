# Pipeline for Diffusion-Derived Features

This document describes the processing pipeline for diffusion MRI data. 
The scripts used in this pipeline can be found in the following GitHub repository: [RATNUS - DMRI Pipeline](https://github.com/ANQIFENG/RATNUS/tree/main/processing_pipelines/dmri_pipeline).


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


## Diffusion Data Imaging parameters

## Expected output