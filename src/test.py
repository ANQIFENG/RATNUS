import os
import sys
import torch
import numpy as np
import torch.nn as nn
import nibabel as nib
from scipy.ndimage import label, find_objects

sys.path.append('../src')
from dataloaders.dataloader_test import ThalamusDataloader
from models.unet3d import UnetL5


# Hard coding
test_batch_size = 1
num_input_channels = 68
device = torch.device("cuda")

data_dir = '/path/to/nifti/data'
label_1_dir = '/path/to/binary/labels'
label_2_dir = '/path/to/labels'
checkpoint_dir = '/path/to/model/checkpoints'
original_data_dir = '/path/to/where/data/is/stored/before/combining/into/68/channels'

out_dir = '/path/to/output/directory'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)


# Remove small connected component
def generate_foreground_mask(data, threshold=50):

    # find connected components
    labeled_data, num_features = label(data)
    regions = find_objects(labeled_data)

    # calculate the volume for each connected component
    areas = [np.sum(data[regions[i]] == 1) for i in range(num_features)]

    mask = np.ones_like(data, dtype=bool)
    mask[data == 0] = 0
    for i, area in enumerate(areas):
        if area < threshold:
            mask[regions[i]] = 0

    return mask


# Recover the predictions to original shape
def pad_to_original_size(pred, original_shape):

    padding = []
    for pred_dim, orig_dim in zip(pred.shape, original_shape):
        total_pad = orig_dim - pred_dim
        pad_before = total_pad // 2
        pad_after = total_pad - pad_before
        padding.append((pad_before, pad_after))

    padded_pred = np.pad(pred, padding, mode='constant', constant_values=0)

    return padded_pred


if __name__ == '__main__':

    model_1 = UnetL5(in_dim=num_input_channels, out_dim=2, num_filters=4, output_activation=nn.Sigmoid()).to(device)
    model_1.eval()
    model_1.require_grad = False

    model_2 = UnetL5(in_dim=num_input_channels, out_dim=13, num_filters=4, output_activation=nn.Softmax(dim=1)).to(
        device)
    model_2.eval()
    model_2.require_grad = False

    for split_idx in range(8):

        split_idx = str(split_idx)
        print('Processing fold ', split_idx)

        checkpoint_1 = os.path.join(checkpoint_dir, 'ROI_model', str(split_idx), 'best_checkpoint.pt')
        model_1.load_state_dict(torch.load(checkpoint_1)['state_dict'])
        model_1 = model_1.to(device)

        checkpoint_2 = os.path.join(checkpoint_dir, 'NUCLEI_model', str(split_idx), 'best_checkpoint.pt')
        model_2.load_state_dict(torch.load(checkpoint_2)['state_dict'])
        model_2 = model_2.to(device)

        test_loaders = ThalamusDataloader(data_dir=data_dir,
                                          label_1_dir=label_1_dir,
                                          label_2_dir=label_2_dir,
                                          batch_size=test_batch_size,
                                          split=split_idx,
                                          division="test")

        for batch_idx, (data, target_1, target_2, data_fn, label_1_fn, label_2_fn) in enumerate(test_loaders):

            data_fn_prefix = data_fn[0].split('_data')[0]
            label_1_fn_prefix = label_1_fn[0].split('_label')[0]
            label_2_fn_prefix = label_2_fn[0].split('_label')[0]
            assert data_fn_prefix == label_1_fn_prefix == label_2_fn_prefix
            print('The testing data is ', data_fn_prefix)

            # get the prediction from model
            data = data.type(torch.float32).to(device)
            target_1 = target_1.type(torch.int32).to(device)
            target_2 = target_2.type(torch.int32).to(device)
            pred_1 = model_1(data).to(device)
            pred_2 = model_2(data).to(device)

            # convert probability to index
            pred_1_labels = torch.argmax(pred_1, dim=1).type(torch.int32)       # Index [0, 1]
            pred_2_labels = torch.argmax(pred_2, dim=1).type(torch.int32) + 1   # Index [1, 2, ..., 13]

            # convert tensor to numpy array
            target_1_arr = target_1.squeeze().detach().cpu().numpy()
            target_2_arr = target_2.squeeze().detach().cpu().numpy()
            pred_1_arr = pred_1_labels.squeeze().detach().cpu().numpy()
            pred_2_arr = pred_2_labels.squeeze().detach().cpu().numpy()

            # remove small connected components for prediction 1
            foreground_mask = generate_foreground_mask(pred_1_arr)
            pred_1_arr = pred_1_arr * foreground_mask

            # generate final prediction
            pred_comb_arr = pred_1_arr.astype(np.int32) * pred_2_arr.astype(np.int32)

            # get affine matrix and original shape
            subject_id, session_id = data_fn_prefix.split('_', 1)
            original_data_folder = os.path.join(original_data_dir, subject_id, session_id)
            t1_files = [f for f in os.listdir(original_data_folder) if 'T1' in f and f.endswith('_wmnorm.nii.gz')]
            if t1_files:
                t1_file_path = os.path.join(original_data_folder, t1_files[0])
                affine_matrix = nib.load(t1_file_path).affine
                original_shape = nib.load(t1_file_path).shape
            else:
                raise FileNotFoundError(f"No T1 file found for {subject_id} {session_id}.")

            # pad to predictions to original size
            pred_1_arr_padded = pad_to_original_size(pred_1_arr, original_shape)
            pred_2_arr_padded = pad_to_original_size(pred_2_arr, original_shape)
            pred_comb_arr_padded = pad_to_original_size(pred_comb_arr, original_shape)

            # save results
            nib.save(nib.Nifti1Image(pred_1_arr_padded.astype(np.int32), affine=affine_matrix),
                     out_dir + '/' + data_fn_prefix + '_model_' + str(split_idx) + '_pred_step1.nii.gz')
            nib.save(nib.Nifti1Image(pred_2_arr_padded.astype(np.int32), affine=affine_matrix),
                     out_dir + '/' + data_fn_prefix + '_model_' + str(split_idx) + '_pred_step2.nii.gz')
            nib.save(nib.Nifti1Image(pred_comb_arr_padded.astype(np.int32), affine=affine_matrix),
                     out_dir + '/' + data_fn_prefix + '_model_' + str(split_idx) + '_pred_comb.nii.gz')

