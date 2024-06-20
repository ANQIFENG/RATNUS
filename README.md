# RATNUS

Rapid, Automated Thalamic Nuclei Segmentation using Multimodal MRI Inputs [[Paper]()]

RATNUS is a deep learning-based method for rapid and automatic segmentation of thalamic nuclei using multimodal MRI. 
Our approach efficiently segments 13 distinct nuclei classes, providing detailed insights into thalamic structure. 
RATNUS comprises two components: 
- Multimodal MRI Calculation 
- Segmentation

The Multimodal MRI Calculation takes less than 20 minutes, and the Segmentation, 
with its two versions，a T1-weighted dual-input version and a full-input version, completes in less than one minute. 


# How to run :runner:
## Prerequisites
- **Operating System:** Linux or OSX
- **Hardware:**
  - Multimodal MRI Calculation: GPU is required.
  - Segmentation: GPU is recommended for optimal performance; CPU mode is also supported


## Installation 
### Multimodal MRI Calculation
You can install using Singularity with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/smri_pipeline:v1.0.0
```
Alternatively, you can download the Singularity image directly from this [[link](https://mega.nz/file/QzcXmIjK#oJvzHiriYlNroSfR6cp5pWFShmFEoeaPU1l8apmZGp4)].


### Segmentation
#### T1-weighted dual-input version:
You can install using Singularity with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus_dual:v1.0.0
```
Alternatively, you can download the Singularity image directly from this [[link](https://mega.nz/file/F2E1Fa4T#pg01iR4yN9rOQ2eEBzBCeBye-GVw7WN_n4TXOK3TdOc)].


#### Full-input version:
You can install using Singularity with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus:v1.0.0
```
Alternatively, you can download the Singularity image directly from this [[link](https://mega.nz/file/sjMh2LzT#LeN-Exsq1yy7jtec2QS43v1XRBUvwwEPW7zQfj7C0Mc)].


## Usage
To run the RATNUS model using the Singularity image, use the following command. 
Replace the placeholder paths with the actual paths to your input files and specify the output directory.
If you are using a CPU, you can remove the `--nv` option from the command.
All input data files are expected to be in NIfTI format (`.nii` or `.nii.gz`).

### Multimodal MRI Calculation
Command:
```bash
singularity run -e --nv smri_pipeline.sif \
            --mprage ${path_to_your_mprage_image} \
            --fgatir ${path_to_your_fgatir_image} \
            --out_dir ${path_to_the_directory_where_you_want_the_output_to_be_stored} \
            --tr ${repetition_time_for_your_mprage_and_fgatir_images} \
            --ti_mprage ${inversion_time_for_your_mprage_image} \
            --ti_fgatir ${inversion_time_for_your_fgatir_image} \
            --ti_min ${minimum_inversion_time_for_synthesizing_multi_ti_images} \
            --ti_max ${maximum_inversion_time_for_synthesizing_multi_ti_images} \
            --ti_step ${step_size_for_inversion_times_between_ti_min_and_ti_max} \
            --num_workers ${number_of_workers_for_parallel_processing} \
            --save_intermediate ${flag_to_save_intermediate_results}
 ```   
For a detailed explanation of the parameters, see [here](https://github.com/ANQIFENG/RATNUS?tab=readme-ov-file#inputs).

Example bash script:
```bash
#!/bin/bash

# Define paths to your data, output directory and singularity image
mprage_path="./MTBI-MRCON0001_v1_T1w.nii.gz"
fgatir_path="./MTBI-MRCON0001_v1_FGATIR.nii.gz"
output_dir="./ratnus_outputs"
sif_path="./smri_pipeline_v1.0.0.sif"
repetition_time=4000.0 # ms
inversion_time_mprage=1400.0 # ms
inversion_time_fgatir=400.0 # ms
inversion_time_min=400.0 # ms
inversion_time_max=1400.0 # ms
inversion_time_step=20.0 # ms
num_workers=8
whether_save_intermediate=False #bool

# Run the RATNUS model with GPU support 
singularity run --nv $sif_path \
                --mprage ${mprage_path} \
                --fgatir ${fgatir_path} \
                --out_dir ${output_dir} \
                --tr ${repetition_time} \
                --ti_mprage ${inversion_time_mprage} \
                --ti_fgatir ${inversion_time_fgatir} \
                --ti_min ${inversion_time_min} \
                --ti_max ${inversion_time_max} \
                --ti_step ${inversion_time_step} \
                --num_workers ${num_workers} \
                --save_intermediate ${whether_save_intermediate}
```


### Segmentation
#### T1-weighted dual-input version:
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

#### Full-input version:
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
sif_path="./ratnus_v1.0.0.sif"


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
RATNUS comprises two main components: Multimodal MRI Calculation and Segmentation. 
First, we process and calculate multi-modality images from raw MPRAGE, FGATIR, and diffusion images. 
These multi-modality images include processed MPRAGE, processed FGATIR, T1/PD maps, Multi-TI images, and diffusion-derived features. 
These images are used because they provide excellent contrast within the thalamus. 
Next, we combine these images as inputs for segmentation, enabling rapid and accurate segmentation of 13 thalamic nuclei.

## Multimodal MRI Calculation
For MPRAGE, FGATIR, and diffusion images, we employ different processing methods. 
- For MPRAGE and FGATIR, the processing and subsequent image calculations are packaged into a Singularity container. 
- For diffusion images, we primarily use TORTOISE and custom scripts to process and calculate scalar maps.

### sMRI Processing Pipeline
We have packaged the entire pipeline into the [Singularity Container](https://github.com/ANQIFENG/RATNUS?tab=readme-ov-file#multimodal-mri-calculation).

The pipeline contains the following steps in sequence:
- HD-BET Brain Extraction
- Registration to MNI space
- N4 Bias Field Correction
  - Calculate N4 Bias Field for MPRAGE and FGATIR
  - Calculate Harmonic Bias Field based on the Bias Fields of MPRAGE and FGATIR
  - Perform Bias Field Correction using the Harmonic Bias Field
- Calculate Background Mask
- Calculate White Matter Mask
- Fuzzy C-means White Matter Mean Normalization [[link](https://github.com/jcreinhold/intensity-normalization)]:
  - Perform Intensity Normalization using the same normalization factor to normalize MPRAGE and FGATIR
- Calculate T1 and PD maps
- Synthesize Multi-TI images from T1 and PD maps 

#### Inputs 
<div style="text-align: center;">
  <table>
    <thead>
      <tr>
        <th></th>
        <th>Preparation</th>
        <th >Required</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: center;">mprage</td>
        <td style="text-align: left;"> 
          <ul>
              <li> Path to your MPRAGE image file. </li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">fgatir</td>
        <td style="text-align: left;"> 
          <ul>
              <li> Path to your FGATIR image file. </li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">out_dir</td>
        <td style="text-align: left;"> 
          <ul>
              <li> Path to the directory where you want the output to be stored. </li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">tr</td>
        <td style="text-align: left;">
          <ul>
            <li>Repetition time (TR) for both your MPRAGE and FGATIR images.</li>
            <li> For synthesizing Multi-TI images, the TR of MPRAGE and FGATIR must be equal. While TI values vary, TR should remain consistent to ensure image comparability. </li>
            <li> Used for T1/PD calculation and Multi-TI synthesis.</li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">ti_mprage</td>
        <td style="text-align: left;">
          <ul>
            <li> Inversion time (TI) for your MPRAGE image.</li>
            <li> Used for T1/PD calculation. </li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">ti_fgatir</td>
        <td style="text-align: left;">
          <ul>
            <li> Inversion time (TI) for your FGATIR image.</li>
            <li> Used for T1/PD calculation. </li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">ti_min</td>
        <td style="text-align: left;" rowspan="3"> 
          <ul>
              <li> These parameters define the range and increments for synthesizing Multi-TI images. Specifically, ti_min sets the minimum inversion time, ti_max sets the maximum inversion time, and ti_step defines the increment between each TI value. </li>
              <li> The default values are 400 ms for ti_min, 1400 ms for ti_max, and 20 ms for ti_step. </li>
              <li> By varying the TI within this default range, a set of 51 images is generated. This range is chosen to maximize contrast in the thalamus, revealing its internal structure with enhanced clarity.</li>
        </ul>
        </td>
        <td style="text-align: center;">🟡</td>
      </tr>
      <tr>
        <td style="text-align: center;">ti_max</td>
        <td style="text-align: center;">🟡</td>
      </tr>
      <tr>
        <td style="text-align: center;">ti_step</td>
        <td style="text-align: center;">🟡</td>
      </tr>
      <tr>
        <td style="text-align: center;">num_workers</td>
        <td style="text-align: left;">
          <ul>
          <li> Number of CPU cores for parallel processing.</li>
          <li> The default value is 8.</li>
          </ul>
        </td>
        <td style="text-align: center;">🟡</td>
      </tr>
      <tr>
        <td style="text-align: center;">save_intermediate</td>
        <td style="text-align: left;">
          <ul>
          <li> Flag to save intermediate results. Boolean value, can be True or False. </li>
          <li> The default value is False.</li>    
        </ul>
        </td>
        <td style="text-align: center;">🟡</td>
      </tr>
    </tbody>
  </table>
</div>
✅ indicates required parameters. 🟡 indicates optional parameters, if not provided, the default values will be used.

#### Outputs 
This repository's Singularity containers are built based on [RADIFOX](https://github.com/jh-mipc/radifox?tab=readme-ov-file#processingmodule), 
and our file organization follows the rules outlined in RADIFOX.

##### Output Structure
The output directory (`/path/to/output`) is organized into four subdirectories:

``` 
/path/to/output
    └── proc
        └── [output NIfTI files]
    └── logs
        └── [images-processing-pipeline]
            └── [processing logs]
    └── qa
        └── [images-processing-pipeline]
            └── [QA images]
    └── tmp 
        └── [temporary results]
```

- `proc`: This directory stores the output NIfTI files.
- `log`: This directory stores the logs from the processing steps.
- `qa`: This directory stores the images for Quality Assurance (QA). It allows for a quick review of the results.
- `tmp`: This directory stores temporary results. This directory is created only if save_intermediate is set to True.

##### Output Files
RATNUS generates multiple output NIfTI files in `proc` directory. 
The output file names have specific suffixes that represent their content. 
Below is a list of the output files and their descriptions:

- `*_reg_thre.nii.gz`: MPRAGE and FGATIR images registered to MNI space.
- `*_transform.mat`: Transformation matrix for MPRAGE and FGATIR registration.
- `*_n4sqrt.nii.gz`: MPRAGE and FGATIR images after N4 bias field correction.
- `*_bias.nii.gz`: Bias field for MPRAGE and FGATIR images.
- `*_harmonic_bias.nii.gz`: Harmonic bias field.
- `*_wmn.nii.gz`: MPRAGE and FGATIR images after white matter mean normalization. Finish processing stage, ready for further calculations such as PD and T1 maps.
- `*_wm_mask.nii.gz`: White matter mask in MNI space.
- `*_bg_mask.nii.gz`: Background mask in MNI space.
- `*_brain_mask.nii.gz`: Brain mask in MNI space.
- `*_t1_map.nii.gz`: T1 map.
- `*_pd_map.nii.gz`: PD map.
- `multi-ti/synT1_xxx.nii.gz`: Multi-TI images, where `xxx` represents the TI value.

### dMRI Processing Pipeline
The scripts of dMRI processing pipeline can be found in [dmri_processing_pipeline](https://github.com/ANQIFENG/RATNUS/tree/main/dmri_processing_pipeline).


#### Steps Overview

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


#### Data Structure

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
│ ...
``````

#### Data Description

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
Our T2 images are in MNI space with 1mm resolution, and have undergone N4 bias field correction and white matter mean normalization.

####  Expected outputs

The output files relevant for our analysis are:

- `*_DT_FA.nii`: Fractional Anisotropy (FA)
- `*_DT_AD.nii`: Axial Diffusivity (AD)
- `*_DT_RD.nii`: Radial Diffusivity (RD)
- `*_DT_TR.nii`: Trace
- `*_DT_WL.nii`: Linear Anisotropy (WL)
- `*_DT_WP.nii`: Planar Anisotropy (WP)
- `*_DT_WS.nii`: Spheric Anisotropy (WS)
- `*_knutsson_5D.nii`: Knutsson 5D Vector
- `*_knutsson_edgemap.nii`: Knutsson Edge Map


## Segmentation

### Inputs 
#### T1w-Dual Input Version:
Trained with MPRAGE and FGATIR, suitable for testing with either one or two modalities.

If your MPRAGE and FGATIR have not undergone the following processing steps, 
we recommend using [sMRI Processing Pipeline](https://github.com/ANQIFENG/RATNUS?tab=readme-ov-file#multimodal-mri-calculation) to get processed MPRAGE and FGATIR.

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
            <p><u>For optimal results, ensure that your test data is prepared as follows:</u></p>
            <li><strong>Registration to MNI Space</strong>: The data should be registered to the MNI space, with a resolution of 1mm isotropic. RATNUS assumes a spatial dimension of 192x224x192.</li>
            <li><strong>Inhomogeneity Correction or Bias Field Correction</strong></li>
            <li><strong>Intensity Normalization</strong></li>
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
✅ indicates required; ⭕ indicates not required.

#### Full Input Version: 
Trained with a comprehensive set of modalities as detailed in our paper. Strictly supports testing with an identical set of input features.

For calculating T1 map, PD map and Multi-TI images, please refer to [sMRI Processing Pipeline](https://github.com/ANQIFENG/RATNUS?tab=readme-ov-file#smri-processing-pipeline). 

For generating diffusion derived features, please refer to [dMRI Processing Pipeline](https://github.com/ANQIFENG/RATNUS?tab=readme-ov-file#dmri-processing-pipeline). 



<div style="text-align: center;">
  <table>
    <thead>
      <tr>
        <th></th>
        <th>Preparation</th>
        <th >Required</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="text-align: center;">MPRAGE</td>
        <td style="text-align: left;" rowspan="2"> 
          <ul>
              <li> The processing of MPRAGE and FGATIR is similar to that in the T1w-Dual Input Version. </li>
              <li> However, to synthesize Multi-TI images effectively, these modalities must be processed together. :warning: Separate adjustments in brightness or contrast could result in computational errors for PD and T1 maps. </li>
              <li> Therefore, a harmonic bias field is employed for Bias Field Correction and consistent Intensity Normalization is applied to ensure uniformity.</li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">FGATIR</td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">T1 & PD</td>
        <td style="text-align: left;">
          <ul>
            <li> The T1 map and PD map are generated using a combined processing of MPRAGE and FGATIR images. </li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">Multi-TI</td>
        <td style="text-align: left;">
          <ul>
          <li>Following the T1&PD maps calculation, a series of Multi-TI images are synthesized. </li>
          <li> Specifically, the Inversion Time (TI) for Multi-TI image ranges from 400 to 1400 ms in increments of 20 ms, producing a set of 51 images. 
                This TI range is selected to maximize contrast within the thalamus, enhancing the visibility of its internal structure.</li>
          <li> The input requires combining 51 images into a single NIfTI file with 51 channels.</li>     
        </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">Diffusion</td>
        <td style="text-align: left;">
          <ul>
              <li>The diffusion-derived features include Axial Diffusivity (AD), Fractional Anisotropy (FA), Radial Diffusivity (RD), Trace, three Westin measures (Linear Anisotropy (WL), Planar Anisotropy (WP), and Spheric Anisotropy (WS)), Knutsson 5D vector, and the Knutsson edge map.</li>
              <li>The input requires combining these features into a single NIfTI file with 13 channels. </li>      
        </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
    </tbody>
  </table>
</div>

### Outputs

#### Output Structure
The output directory (`/path/to/output`) is organized into three subdirectories:

``` 
/path/to/output
    └── proc
        └── [output NIfTI files]
    └── logs
        └── [thalamic-nuclei-segmentation]
            └── [processing logs]
    └── qa
        └── [thalamic-nuclei-segmentation]
            └── [QA images]
```

#### Output Files
The output NIfTI files will be found in `proc` directory.
The output segmentation will maintain the same dimensions and resolution as your input data.
The output file name will end with one of the following suffixes based on the input version:

- `*_ratnus`: For the full-input version.
- `*_ratnus_dual`: If you are using the T1-weighted dual-input version.
- `*_ratnus_mprage`: If only MPRAGE is used in the dual-input version.
- `*_ratnus_fgatir`: If only FGATIR is used in the dual-input version.

#### Label and Color Tabel
The output segmentation labels 13 distinct thalamic nuclei, with `0` representing the background and `1-13` corresponding to specific nuclei labels as follows:
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
