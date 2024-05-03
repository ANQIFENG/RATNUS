# RATNUS

Rapid, Automated Thalamic Nuclei Segmentation using Multimodal MRI Inputs [[Paper]()]

RATNUS is a deep learning-based method for rapid and automatic segmentation of thalamic nuclei using multimodal MRI. 
Our approach efficiently segments 13 distinct nuclei classes, providing detailed insights into thalamic structure. 
RATNUS supports two versions: a T1-weighted dual-input version and a full-input version, 
detailed further in the [About RATNUS](#about-ratnus) section.


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
*** To do *** 


### Full-input version:
The Full-input version of the RATNUS model can be installed using Singularity with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus:v7.0.0
```

Alternatively, you can download the Singularity image directly from this [link](https://dl.dropboxusercontent.com/s/example/full-input-version.sif).


## Usage
To run the RATNUS model using the Singularity image, use the following command. 
Replace the placeholder paths with the actual paths to your input files and specify the directory for the output:
If you are not using a GPU, you can remove the `--nv` option from the command.

### T1-weighted dual-input version:
*** To do *** 

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


# Run the RATNUS model with GPU support (remove the `--nv` option from the command if you are using a CPU)
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
## Model
The RATNUS project includes two versions:
- **T1w-Dual Input Version**: Trained with MPRAGE and FGATIR, suitable for testing with either one or two modalities.
- **Full Input Version**: Trained with a comprehensive set of modalities, as described in the paper.

## Outputs




# Citation
If you find this project useful in your research, please consider citing:



# Contact
For questions or support, please contact [afeng11@jhu.edu](mailto:afeng11@jhu.edu) or post through [GitHub Issues](https://github.com/ANQIFENG/RATNUS/issues).
