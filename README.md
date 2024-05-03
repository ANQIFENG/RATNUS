# RATNUS

Rapid, Automated Thalamic Nuclei Segmentation using Multimodal MRI Inputs [[Paper]()]

RATNUS is a deep learning-based method for rapid and automatic segmentation of thalamic nuclei using multimodal MRI. 
Our approach efficiently segments 13 distinct nuclei classes, providing detailed insights into thalamic structure. 
RATNUS supports two versions: a T1-weighted dual-input version and a full-input version, 
detailed further in the [About RATNUS](#about-ratnus) section. 
Both version can complete segmentation in less than one minute.


# How to run
## Prerequisites
- **Operating System:** Linux or OSX
- **Hardware:** NVIDIA GPU + CUDA CuDNN recommended for optimal performance; CPU mode is also supported.
- **Data Preparation:** 
  - **Registration:** Data should be registered to the MNI space with a resolution of 1mm isotropic. RATNUS assumes a spatial dimensions of 192x224x192.
  - **Inhomogeneity Correction** 
  - **Intensity Normalization** 


## Installation instructions
### T1-weighted dual-input version:
- :construction: To do 


### Full-input version:
The Full-input version of the RATNUS model can be installed using Singularity with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus:v7.0.0
```
Alternatively, you can download the Singularity image directly from this [link](https://dl.dropboxusercontent.com/scl/fi/7mxniqlerbqeea11dxpzd/ratnus_v7.0.0.sif?rlkey=b098trwjbbf4v2z8z4p69nu5b&dl=1).


## Usage
To run the RATNUS model using the Singularity image, use the following command. 
Replace the placeholder paths with the actual paths to your input files and specify the directory for the output:
If you are using a CPU, you can remove the `--nv` option from the command.
All input data files are expected to be in NIfTI format (`.nii` or `.nii.gz`).

### T1-weighted dual-input version:
- :construction:  To do 

###  Full-input version:
Command:
```bash
singularity run --nv ratnus.sif \
            --mprage ${path_to_your_mprage_image} \
            --fgatir ${path_to_your_fgatir_image} \
            --t1map ${path_to_your_t1_map} \
            --pdmap ${path_to_your_pd_map} \
            --multiTI ${path_to_you_multi-TI_images} \
            --diffusion ${path_to_you_diffusion_derived_features} \
            --out_dir ${path_to_the_directory_where_you_want_the_output_to_be_stored}
 ```           

Example bash script:
```bash
#!/bin/bash

# Define paths to your data, output directory and singularity image
mprage_path="./MTBI-MRCON0001_v1_T1w.nii.gz"
fgatir_path="./MTBI-MRCON0001_v1_FGATIR.nii.gz"
t1map_path="./MTBI-MRCON0001_v1_t1map.nii.gz"
pdmap_path="./MTBI-MRCON0001_v1_pdmap.nii.gz"
multiTI_path="./MTBI-MRCON0001_v1_multiTI.nii.gz"
diffusion_path="./MTBI-MRCON0001_v1_diffusion_features.nii.gz"
out_dir="./ratnus_outputs"
sif_path="./ratnus_v7.0.0.sif"


# Run the RATNUS model with GPU support 
singularity run --nv $sif_path \
                --mprage ${mprage_path} \
                --fgatir ${fgatir_path} \
                --t1map ${t1map_path} \
                --pdmap ${pdmap_path} \
                --multiTI ${multiTI_path} \
                --diffusion ${diffusion_path} \
                --out_dir ${out_dir}
```

# About RATNUS
## Input 
### T1w-Dual Input Version: 
- Trained with MPRAGE and FGATIR, suitable for testing with either one or two modalities.
- Expected your test data go through:
  - Registration to the MNI space, with a resolution of 1mm isotropic. 
    RATNUS assumes a spatial dimensions of 192x224x192.
  - Inhomog


- **Full Input Version**: Trained with a comprehensive set of modalities, detailed in the paper. 
This version exclusively supports testing with an identical set of input features.


## Outputs
RATNUS generates a single NIfTI file ending with `_ratnus` in your predefined output directory. 
The output file will maintain the same dimensions and resolution as your input data.

The output segmentation file labels 13 distinct thalamic nuclei, with `0` representing the background and `1-13` corresponding to specific nuclei labels as follows:
- `1`: Anterior Nucleus (AN)
- `2`: Central Lateral (CL)
- `3`: Center Median (CM)
- `4`: Lateral Dorsal (LD)
- `5`: Lateral Posterior (LP)
- `6`: Mediodorsal (MD)
- `7`: Anterior Pulvinar (PuA)
- `8`: Inferior Pulvinar (PuI)
- `9`: Ventral Anterior (VA)
- `10`: Ventral Lateral Anterior (VLA)
- `11`: Ventral Lateral Posterior (VLP)
- `12`: Ventral Posterior Lateral (VPL)
- `13`: Ventral Posterior Medial (VPM)


Each nucleus is uniquely identified by a color code to facilitate visual analysis of the segmentation results. 
The color table can be viewed and downloaded from :
[RATNUS Color Table](https://github.com/ANQIFENG/RATNUS/blob/main/ratnus_color_table.txt).


# Citation
If you find this project useful in your research, please consider citing:



# Contact
For questions or support, please contact [afeng11@jhu.edu](mailto:afeng11@jhu.edu) or post through [GitHub Issues](https://github.com/ANQIFENG/RATNUS/issues).
