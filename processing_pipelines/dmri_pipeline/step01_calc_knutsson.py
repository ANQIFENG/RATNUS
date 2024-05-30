"""
This script calculates Knutsson 5D vectors and edge map given eigenvector calculated in step00.
"""


import os
import subprocess
import nibabel as nib
import numpy as np

# Define source directory
SRC_DIR = "/path/to/your/data/directory"


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


# Function to compute Knutsson 5D vectors and edgemap
def compute_knutsson(eigenvector_file, output_prefix):
    # Load eigenvector data
    data = nib.load(eigenvector_file)
    data_np = data.get_fdata()[..., 0:3].astype(np.float32)

    # Compute Knutsson 5D vectors
    k1 = data_np[:, :, :, 0]**2 - data_np[:, :, :, 1]**2
    k2 = 2 * data_np[:, :, :, 0] * data_np[:, :, :, 1]
    k3 = 2 * data_np[:, :, :, 0] * data_np[:, :, :, 2]
    k4 = 2 * data_np[:, :, :, 1] * data_np[:, :, :, 2]
    k5 = (2 * data_np[:, :, :, 2]**2 - data_np[:, :, :, 0]**2 - data_np[:, :, :, 1]**2) / np.sqrt(3)

    knutsson_data = np.stack((k1, k2, k3, k4, k5), axis=3)
    knutsson_image = nib.Nifti1Image(knutsson_data, data.affine, data.header)
    knutsson_image.set_data_dtype(np.float32)
    knutsson_image.to_filename(output_prefix + '_knutsson_5D.nii')

    # Compute Jacobian for the Knutsson 5D vectors
    jacobian = np.zeros(knutsson_data.shape[0:3] + (knutsson_data.shape[3] * 3,))

    for i in range(knutsson_data.shape[3]):
        east = np.pad(knutsson_data[1:, :, :, i], ((0, 1), (0, 0), (0, 0)), 'constant')
        west = np.pad(knutsson_data[:-1, :, :, i], ((1, 0), (0, 0), (0, 0)), 'constant')
        north = np.pad(knutsson_data[:, :-1, :, i], ((0, 0), (1, 0), (0, 0)), 'constant')
        south = np.pad(knutsson_data[:, 1:, :, i], ((0, 0), (0, 1), (0, 0)), 'constant')
        forth = np.pad(knutsson_data[:, :, 1:, i], ((0, 0), (0, 0), (0, 1)), 'constant')
        back = np.pad(knutsson_data[:, :, :-1, i], ((0, 0), (0, 0), (1, 0)), 'constant')

        jacobian[:, :, :, i * 3] = (east - west) / 2
        jacobian[:, :, :, i * 3 + 1] = (south - north) / 2
        jacobian[:, :, :, i * 3 + 2] = (forth - back) / 2

    edge = np.sqrt(np.sum(jacobian**2, axis=3))

    edge_image = nib.Nifti1Image(edge, data.affine, data.header)
    edge_image.set_data_dtype(np.float32)
    edge_image.to_filename(output_prefix + '_knutsson_edgemap.nii')


# Process subjects
def process_subjects():
    for subj_dir in os.listdir(SRC_DIR):
        subj_path = os.path.join(SRC_DIR, subj_dir)
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

            # Check if the directory to store the diffusion results from step00 (TORTOISE) exists, skip if it does not exist
            diffusion_dir = os.path.join(sess_dir, "proc", "diffusion", "AP_proc_DRBUDDI_proc")
            if not is_directory(diffusion_dir):
                print(f"Skipping {subj_id} {sess_id} as {diffusion_dir} does not exist.")
                continue

            # Run Knutsson 5D vectors calculation
            eigenvector_file = os.path.join(diffusion_dir, "*DT_EV.nii")
            output_prefix = os.path.join(diffusion_dir, "AP_proc_DRBUDDI_up_final_N1_DT")
            compute_knutsson(eigenvector_file, output_prefix)


if __name__ == "__main__":
    process_subjects()