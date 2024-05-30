"""
This script processes diffusion MRI data using TORTOISE software.
Website: https://tortoise.nibib.nih.gov/

It performs the following steps:
1. Imports NIFTI files into TORTOISE-compatible format.
2. Runs the DIFFPREP tool for preprocessing (distortion and motion correction) the diffusion data.
3. Runs the DR BUDDI tool for EPI distortion correction.
4. Runs the DIFFCal tool for tensor estimation and creates tensor maps.
5. Converts TORTOISE B-matrix to FSL B-vectors.
"""


import os
import subprocess

# Define paths
base_path = "/path/to/your/tortoise/installation/TORTOISE_V3.2.0"  # Replace with the path where TORTOISE is installed
src_dir = "/path/to/your/data/directory"  # Replace with the path to your data directory

# Define environment variables
os.environ["PATH"] = f"{base_path}/DIFFPREPV320/bin/bin:{os.environ['PATH']}"
os.environ["PATH"] = f"{base_path}/DIFFCALC/DIFFCALCV320:{os.environ['PATH']}"
os.environ["PATH"] = f"{base_path}/DRBUDDIV320/bin:{os.environ['PATH']}"
os.environ["PATH"] = f"{base_path}/DRTAMASV320/bin:{os.environ['PATH']}"


# Define checking functions
def is_directory(path):
    return os.path.isdir(path)


def starts_with_MTBI(string):
    return string.startswith("MTBI")


def is_valid_session(session_name):
    return session_name in ["v1", "v2", "v3"]


# Function to run bash commands
def run_command(command):
    print(f"Running: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    return process.returncode


# Process subjects
def process_subjects():
    for subj_dir in os.listdir(src_dir):
        subj_path = os.path.join(src_dir, subj_dir)
        if not is_directory(subj_path):
            print(f"Skipping {subj_path} as it's not a directory.")
            continue

        subj_id = os.path.basename(subj_path)
        print(f"Processing {subj_id}")

        if not starts_with_MTBI(subj_id):
            print(f"Skipping {subj_id} as it doesn't start with 'MTBI'.")
            continue

        for sess_dir in os.listdir(subj_path):
            sess_path = os.path.join(subj_path, sess_dir)
            if not is_directory(sess_path):
                print(f"Skipping {sess_path} as it's not a directory.")
                continue

            sess_id = os.path.basename(sess_path)
            print(f"Processing {sess_id}")

            if not is_valid_session(sess_id):
                print(f"Skipping {sess_id} as it's not a valid session name (should be v1, v2 or v3).")
                continue

            # Define paths and commands
            dwi_bmax2500_nifti = f"{sess_path}/nii/*BMAX2500*.nii.gz"
            dwi_bmax2500_bval = f"{sess_path}/nii/*BMAX2500*.bval"
            dwi_bmax2500_bvec = f"{sess_path}/nii/*BMAX2500*.bvec"
            b0_nifti = f"{sess_path}/nii/*B0*.nii.gz"
            b0_bval = f"{sess_path}/nii/*B0*.bval"
            b0_bvec = f"{sess_path}/nii/*B0*.bvec"

            out_dir = f"{sess_path}/proc/diffusion"
            ap_out_dir = f"{out_dir}/AP"
            pa_out_dir = f"{out_dir}/PA"
            os.makedirs(out_dir, exist_ok=True)
            os.makedirs(ap_out_dir, exist_ok=True)
            os.makedirs(pa_out_dir, exist_ok=True)

            print(f"Creating symbolic links for {sess_id}...")
            run_command(f"ln -s {dwi_bmax2500_nifti} {ap_out_dir}")
            run_command(f"ln -s {dwi_bmax2500_bval} {ap_out_dir}")
            run_command(f"ln -s {dwi_bmax2500_bvec} {ap_out_dir}")
            run_command(f"ln -s {b0_nifti} {pa_out_dir}")
            run_command(f"ln -s {b0_bval} {pa_out_dir}")
            run_command(f"ln -s {b0_bvec} {pa_out_dir}")

            #
            # ********************* ImportNIFTI *********************
            print(f"Importing NIFTI files for {sess_id}...")
            run_command(f"ImportNIFTI -i {dwi_bmax2500_nifti} -b {dwi_bmax2500_bval} -v {dwi_bmax2500_bvec} -p vertical -o {ap_out_dir}")
            run_command(f"ImportNIFTI -i {b0_nifti} -b {b0_bval} -v {b0_bvec} -p vertical -o {pa_out_dir}")

            #
            # ********************* DIFFPREP *********************
            print(f"Running DIFFPREP for {sess_id}...")
            t2 = f"{sess_path}/proc/*T2*.nii.gz"
            run_command(f"DIFFPREP -i {ap_out_dir}/AP.list -s {t2} --will_be_drbuddied 1 -d for_final --is_human_brain 1 --upsampling all --res 1.0 1.0 1.0 --keep_intermediate 1 --do_QC 0")
            run_command(f"DIFFPREP -i {pa_out_dir}/PA.list -s {t2} --will_be_drbuddied 1 -d for_final --is_human_brain 1 --upsampling all --res 1.0 1.0 1.0 --keep_intermediate 1 --do_QC 0")

            #
            # ********************* DRBUDDI *********************
            print(f"Running DR BUDDI without GUI for {sess_id}...")
            run_command(f"DR_BUDDI_withoutGUI --up_data $(ls {ap_out_dir}/AP_proc.list) --down_data $(ls {pa_out_dir}/PA_proc.list) --structural {t2} --res 1.0 1.0 1.0 -g 1")

            #
            # ********************* DIFFCal *********************
            print(f"Running DIFFCal for {sess_id}...")
            run_command(f"bet2 {out_dir}/AP_proc_DRBUDDI_proc/structural.nii {out_dir}/AP_proc_DRBUDDI_proc/structure -m -f 0.3")
            bet2mask = f"{out_dir}/AP_proc_DRBUDDI_proc/structure_mask.nii.gz"
            final_list = f"{out_dir}/AP_proc_DRBUDDI_proc/AP*final.list"
            run_command(f"EstimateTensorNLLS -i {final_list} --save_CS 1 -m {bet2mask}")

            print(f"Computing all tensor maps for {sess_id}...")
            dt = f"{out_dir}/AP_proc_DRBUDDI_proc/*final_N1_DT.nii"
            run_command(f"ComputeAllTensorMaps.bash {dt}")

            #
            # ******************** TORTOISEBmatrixToFSLBVecs ********************
            bmtxt = f"{out_dir}/AP_proc_DRBUDDI_proc/AP*final.bmtxt"
            print(f"Converting TORTOISE B-matrix to FSL B-vectors for {sess_id}...")
            run_command(f"TORTOISEBmatrixToFSLBVecs {bmtxt}")


if __name__ == "__main__":
    process_subjects()