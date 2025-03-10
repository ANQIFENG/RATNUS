# RATNUS

Rapid, Automated Thalamic Nuclei Segmentation using Multimodal MRI Inputs [[Paper](https://arxiv.org/pdf/2409.06897)]

RATNUS is a deep learning-based method for fast and accurate thalamic nuclei segmentation, distinguishing 13 nuclei classes for detailed structural insights.
This branch **(v2.0-ratnus_t1map)** is an updated version using T1 maps, which we validated to achieve optimal segmentation performance.
For the multimodal version, please see branch [v1.0-ratnus](https://github.com/ANQIFENG/RATNUS/tree/v1.0-ratnus).

## How to run :runner:
### Prerequisites
- **Operating System:** Linux or OSX
- **Hardware:** GPU is recommended; CPU is also supported

### Installation
Install the Singularity Image with the following command:
```bash
singularity pull --docker-login docker://registry.gitlab.com/anqifeng/ratnus_t1map:v1.0.0
```

### Usage
To run the Singularity Image, use the command below, 
replacing placeholder paths with actual input files and output directory.
Remove the `--nv`if using a CPU. Input files must be in NIfTI format (`.nii` or `.nii.gz`).
```bash
singularity run --nv ratnus_t1map.sif \
               --data_path ${data_path} \
               --out_dir ${out_dir} \
               --device ${device}
 ``` 


## Details :brain:
RATNUS_T1MAP uses T1 maps as inputs, which we validated as optimal for thalamic nuclei segmentation. 
You can generate T1 maps from MPRAGE and FGATIR pairs using our dedicated repository [here](https://github.com/ANQIFENG/multi-TI-image-calc-pipeline).

### Inputs
<div style="overflow-x:auto;">
  <table>
    <thead>
      <tr>
        <th>Arg</th>
        <th>Description</th>
        <th>Required</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>data_path</td>
        <td>Path to the input T1 map.</td>
        <td>✅</td>
      </tr>
      <tr>
        <td>out_dir</td>
        <td>Path to the output directory.</td>
        <td>✅</td>
      </tr>
      <tr>
        <td>device</td>
        <td>Computation device: either 'gpu' or 'cpu' (default: 'gpu').</td>
        <td>⭕</td>
      </tr>
    </tbody>
  </table>
</div>

✅ Required; ⭕ Optional.


### Outputs

#### Output Structure
The output directory (`/path/to/output`) is organized into two subdirectories:

``` 
/path/to/output
    └── proc
        └── [output NIfTI files]
    └── qa
        └── [ratnus_t1map]
            └── [QA images]
```
- proc: Stores the output NIfTI files.
- qa: Stores QA images for quick result review.


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


## Citation :open_book:
If you find this project useful in your research, please consider citing:

```bibtex
@article{feng2024ratnus,
  title={RATNUS: Rapid, Automatic Thalamic Nuclei Segmentation using Multimodal MRI inputs},
  author={Feng, Anqi and Bian, Zhangxing and Dewey, Blake E and Colinco, Alexa Gail and Zhuo, Jiachen and Prince, Jerry L},
  journal={arXiv preprint arXiv:2409.06897},
  year={2024}
}
```


## Contact :e-mail:
For questions or support, please contact [afeng11@jhu.edu](mailto:afeng11@jhu.edu) or post through [GitHub Issues](https://github.com/ANQIFENG/RATNUS/issues).
