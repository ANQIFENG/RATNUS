# RATNUS

Rapid, Automated Thalamic Nuclei Segmentation using Multimodal MRI Inputs [[Paper]()]

RATNUS is a deep learning-based method for rapid and automatic segmentation of thalamic nuclei using multimodal MRI. 
Our approach efficiently segments 13 distinct nuclei classes, providing detailed insights into thalamic structure. 
RATNUS supports two versions: a T1-weighted dual-input version and a full-input version, 
detailed further in the [About RATNUS](#about-ratnus) section. 
Both version can complete segmentation in less than one minute.


# How to run :runner:
## Prerequisites
- **Operating System:** Linux or OSX
- **Hardware:** NVIDIA GPU + CUDA CuDNN recommended for optimal performance; CPU mode is also supported.
 
## Installation 
### T1-weighted dual-input version:
You can install using Singularity with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus_dual:v1.0.0
```
Alternatively, you can download the Singularity image directly from this [[link](https://mega.nz/file/pvMRGJqb#3xlR-Wxolsq_s-V9bDtnVd25veFptmNXBXRsCPfOOTo)].



### Full-input version:
You can install using Singularity with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus:v1.0.0
```
Alternatively, you can download the Singularity image directly from this [[link](https://mega.nz/file/06sVlAJK#RTNXOD3HKJa6liX19XBXq4ghOSGHmVsADRxjHJcZkX4)].


## Usage
To run the RATNUS model using the Singularity image, use the following command. 
Replace the placeholder paths with the actual paths to your input files and specify the directory for the output:
If you are using a CPU, you can remove the `--nv` option from the command.
All input data files are expected to be in NIfTI format (`.nii` or `.nii.gz`).

### T1-weighted dual-input version:
We use MPRAGE and FGATIR as normal inputs, 
and support missing modalities where only MPRAGE or only FGATIR is available.

#### 1.Using both MPRAGE and FGATIR as inputs:
```bash
singularity run --nv ratnus_dual.sif \
            --mprage ${path_to_your_mprage_image} \
            --fgatir ${path_to_your_fgatir_image} \
            --out_dir ${path_to_the_directory_where_you_want_the_output_to_be_stored}
 ```           
#### 2.Using only MPRAGE:
```bash
singularity run --nv ratnus_dual.sif \
            --mprage ${path_to_your_mprage_image} \
            --out_dir ${path_to_the_directory_where_you_want_the_output_to_be_stored}
 ```   
#### 3.Using only FGATIR:
```bash
singularity run --nv ratnus_dual.sif \
            --fgatir ${path_to_your_fgatir_image} \
            --out_dir ${path_to_the_directory_where_you_want_the_output_to_be_stored}
 ```   

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

# About RATNUS :brain:
## Input 
### T1w-Dual Input Version: 
- Trained with MPRAGE and FGATIR, suitable for testing with either one or two modalities.

- For optimal results, ensure that your test data is prepared as follows:
  - **Registration to MNI Space**: The data should be registered to the MNI space, with a resolution of 1mm isotropic.
    RATNUS assumes a spatial dimensions of 192x224x192.
  - **Inhomogeneity Correction or Bias Field Correction**
  - **Intensity Normalization**:
    RATNUS uses Fuzzy C-means White Matter Mean Normalization [[link](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/10949/2513089/Evaluating-the-impact-of-intensity-normalization-on-MR-image-synthesis/10.1117/12.2513089.short)].

<div style="text-align: center;">
  <table>
    <thead>
      <tr>
        <th></th>
        <th>Preparation</th>
        <th colspan="3">Required</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: center;">MPRAGE</td>
        <td style="text-align: left;" rowspan="2"> 
          <ul>
            <li>Registration to MNI Space</li>
            <li>Inhomogeneity Correction </li>
            <li>Intensity Normalization</li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
        <td style="text-align: center;">✅</td>
        <td style="text-align: center;">⭕️</td>
      </tr>
      <tr>
        <td style="text-align: center;">FGATIR</td>
        <td style="text-align: center;">✅</td>
        <td style="text-align: center;">⭕️</td>
        <td style="text-align: center;">✅</td>
      </tr>
    </tbody>
  </table>
</div>

### Full Input Version: 
- Trained with a comprehensive set of modalities including MPRAGE, FGATIR, T1 map, PD map, Multi-TI images, and diffusion-derived features as detailed in our paper.

- This version strictly supports testing with an identical set of input features.

- The processing of MPRAGE and FGATIR is similar to that in the T1w-Dual Input Version. 
  However, to synthesize Multi-TI images effectively, these modalities must be processed together. 
  Separate adjustments in brightness or contrast could result in computational errors for PD and T1 maps :warning:. 
  Therefore, a harmonic bias field is employed for Bias Field Correction and consistent Intensity Normalization is applied to ensure uniformity.

- **Structural MRI Processing Pipeline**:
  The T1 map and PD map within RATNUS are generated using a combined processing of MPRAGE and FGATIR images. 
  Following this, a series of Multi-TI images are synthesized. 
  Specifically, the Inversion Time (TI) for Multi-TI image ranges from 400 to 1400 ms in increments of 20 ms, producing a set of 51 images. 
  This TI range is selected to maximize contrast within the thalamus, enhancing the visibility of its internal structure.
  To assist users, we have packaged the pipeline for synthesizing Multi-TI images from MPRAGE and FGATIR. 
  Inputting the raw MPRAGE and FGATIR will yield processed MPRAGE and FGATIR, T1 maps, PD maps, and the series of Multi-TI images.
  please refer to [smri_pipeline_descriptions](https://github.com/ANQIFENG/RATNUS/blob/main/docs/pipeline_for_multi-TI.md).

- **Diffusion Data Processing Pipeline**:
  The diffusion-derived features within RATNUS include Axial Diffusivity (AD), Fractional Anisotropy (FA), Radial Diffusivity (RD), Trace, three Westin measures (Linear Anisotropy (WL), Planar Anisotropy (WP), and Spheric Anisotropy (WS)), Knutsson 5D vector, and the Knutsson edge map. 
  To assist users, we have documented the details of the diffusion data processing pipeline on [dmri_pipeline_descriptions](https://github.com/ANQIFENG/RATNUS/blob/main/docs/pipeline_for_diffusion_derived_features.md). 
  Additionally, the processing code can be found on [dmri_pipeline_codes](https://github.com/ANQIFENG/RATNUS/tree/main/processing_pipelines/dmri_pipeline).


## Outputs
RATNUS generates a single NIfTI file in your predefined output directory. 
The output file will maintain the same dimensions and resolution as your input data.

For the full-input version, the output file name will end with `_ratnus`. 
If you are using the T1-weighted dual-input version, the output file name will end with `_ratnus_dual`. 
If only one modality is used in the dual-input version, the output file name will reflect the modality used, 
ending with `_ratnus_mprage` if only MPRAGE is used, or `_ratnus_fgatir` if only FGATIR is used.

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


# Citation :open_book:
If you find this project useful in your research, please consider citing:



# Contact :e-mail:
For questions or support, please contact [afeng11@jhu.edu](mailto:afeng11@jhu.edu) or post through [GitHub Issues](https://github.com/ANQIFENG/RATNUS/issues).
