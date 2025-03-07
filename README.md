# RATNUS

Rapid, Automated Thalamic Nuclei Segmentation using Multimodal MRI Inputs [[Paper](https://arxiv.org/pdf/2409.06897)]

RATNUS is a deep learning-based method for rapid and automatic segmentation of thalamic nuclei using multimodal MRI. 
Our approach efficiently segments 13 distinct nuclei classes, providing detailed insights into thalamic structure. 


## How to run :runner:
### Prerequisites
- **Operating System:** Linux or OSX
- **Hardware:** GPU is recommended; CPU is also supported


### Installation
#### T1-weighted dual-input version:
Install the Singularity Image with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus_dual:v1.0.0
```
Or download the Singularity image directly from [[link](https://mega.nz/file/F2E1Fa4T#pg01iR4yN9rOQ2eEBzBCeBye-GVw7WN_n4TXOK3TdOc)].


#### Full-input version:
Install the Singularity Image with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus:v1.0.0
```
Or download the Singularity image directly from [[link](https://mega.nz/file/sjMh2LzT#LeN-Exsq1yy7jtec2QS43v1XRBUvwwEPW7zQfj7C0Mc)].


### Usage
To run the Singularity Image, use the command below, 
replacing placeholder paths with actual input files and output directory.
Remove the `--nv`if using a CPU. Input files must be in NIfTI format (`.nii` or `.nii.gz`).

#### T1-weighted dual-input version:
This supports MPRAGE and FGATIR as inputs, allowing either or both modalities.

```bash
singularity run --nv ratnus_dual.sif \
          ${mprage:+--mprage $mprage} \
          ${fgatir:+--fgatir $fgatir} \
          --out_dir ${path_to_output_directory}
 ```
- Both MPRAGE & FGATIR: Set `mprage` and `fgatir` paths.  
- Only MPRAGE: Set `mprage`; omit `fgatir`.  
- Only FGATIR: Set `fgatir`; omit `mprage`. 


#### Full-input version:
Command:
```bash
singularity run --nv ratnus.sif \
            --mprage ${path_to_mprage} \
            --fgatir ${path_to_fgatir} \
            --t1map ${path_to_t1_map} \
            --pdmap ${path_to_pd_map} \
            --multiTI ${path_to_multi-TI_images} \
            --diffusion ${path_to_diffusion_derived_features} \
            --out_dir ${path_to_output_directory}
 ```           

Example bash script:
```bash
#!/bin/bash

# Define paths to your data, output directory and singularity image
mprage_path="./MPRAGE.nii.gz"
fgatir_path="./FGATIR.nii.gz"
t1map_path="./t1map.nii.gz"
pdmap_path="./pdmap.nii.gz"
multiTI_path="./multiTIs.nii.gz"
diffusion_path="./diffusion_features.nii.gz"
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

## Details :brain:
RATNUS requires multi-modality images as inputs, including the MPRAGE and FGATIR sequences, T1 and PD maps, Multi-TI images, and diffusion-derived features.
- For the processing of MPRAGE and FGATIR to compute T1/PD maps and Multi-TI images, please refer to our dedicated repository [here](https://github.com/ANQIFENG/multi-TI-image-calc-pipeline).
- For diffusion-derived features, detailed calculations can be found [here](dmri_processing_pipeline/dmri_processing_pipeline_overview.md).

### Inputs 
#### T1w-Dual Input Version:
Trained with MPRAGE and FGATIR, allowing testing with either or both modalities. 
To ensure optimal results, your MPRAGE and FGATIR data should undergo the following preprocessing steps. 
If not, we recommend using [multi-TI-image-calc-pipeline](https://github.com/ANQIFENG/multi-TI-image-calc-pipeline) for processed images.

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
            <li><strong>Registration to MNI Space</strong>(1mm isotropic, 192×224×192)</li>
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
✅ Required; ⭕ Not Required .

#### Full Input Version: 
Trained with a comprehensive set of modalities as detailed in our paper and strictly requires an identical input feature set for testing.

For calculating T1 map, PD map and Multi-TI images, refer to [multi-TI-image-calc-pipeline](https://github.com/ANQIFENG/multi-TI-image-calc-pipeline).

For generating diffusion derived features, please refer to [dMRI Processing Pipeline](https://mega.nz/file/sjMh2LzT#LeN-Exsq1yy7jtec2QS43v1XRBUvwwEPW7zQfj7C0Mc). 


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
              <li> These images should be processed together for accurate maps estimation, including co-registration, Bias Field Correction with a harmonic bias field and consistent intensity normalization.</li>
              <li> Separate adjustments in brightness or contrast could result in computational errors for PD and T1 maps. :warning: </li>
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
            <li> Generated from combined processing of MPRAGE and FGATIR. </li>
          </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">Multi-TI</td>
        <td style="text-align: left;">
          <ul>
          <li> Derived from T1 & PD maps. Specifically, the Inversion Time (TI) ranges from 400 to 1400 ms in increments of 20 ms, producing a set of 51 images. 
                This TI range is selected to maximize contrast within the thalamus, enhancing the visibility of its internal structure.</li>
            <li> The final input combines these into a 51-channel NIfTI file.</li>     
        </ul>
        </td>
        <td style="text-align: center;">✅</td>
      </tr>
      <tr>
        <td style="text-align: center;">Diffusion</td>
        <td style="text-align: left;">
          <ul>
              <li>The diffusion-derived features include Axial Diffusivity (AD), Fractional Anisotropy (FA), Radial Diffusivity (RD), Trace, three Westin measures (Linear Anisotropy (WL), Planar Anisotropy (WP), and Spheric Anisotropy (WS)), Knutsson 5D vector, and the Knutsson edge map. 
                <li> These are combined into a 13-channel NIfTI file.</li>      
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

```bibtex
@article{feng2024ratnus,
  title={RATNUS: Rapid, Automatic Thalamic Nuclei Segmentation using Multimodal MRI inputs},
  author={Feng, Anqi and Bian, Zhangxing and Dewey, Blake E and Colinco, Alexa Gail and Zhuo, Jiachen and Prince, Jerry L},
  journal={arXiv preprint arXiv:2409.06897},
  year={2024}
}
```


# Contact :e-mail:
For questions or support, please contact [afeng11@jhu.edu](mailto:afeng11@jhu.edu) or post through [GitHub Issues](https://github.com/ANQIFENG/RATNUS/issues).
