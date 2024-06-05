import os
import sys
import torch
import numpy as np
import nibabel as nib
from torch.utils.data import Dataset, DataLoader

sys.path.append('../../src')
from utils.augmentation import center_crop

device = torch.device("cuda")

# Generate from ../utils/split_dataset_to_8_folds.ipynb
config_split = {
    '0': {'train_idxs': [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], 'val_idxs': [3, 4], 'test_idxs': [0, 1, 2]},
    '1': {'train_idxs': [0, 1, 2, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], 'val_idxs': [6, 7], 'test_idxs': [3, 4, 5]},
    '2': {'train_idxs': [0, 1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], 'val_idxs': [9, 10], 'test_idxs': [6, 7, 8]},
    '3': {'train_idxs': [0, 1, 2, 3, 4, 5, 6, 7, 8, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], 'val_idxs': [12, 13], 'test_idxs': [9, 10, 11]},
    '4': {'train_idxs': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 17, 18, 19, 20, 21, 22, 23], 'val_idxs': [15, 16], 'test_idxs': [12, 13, 14]},
    '5': {'train_idxs': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20, 21, 22, 23], 'val_idxs': [18, 19], 'test_idxs': [15, 16, 17]},
    '6': {'train_idxs': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 23], 'val_idxs': [21, 22], 'test_idxs': [18, 19, 20]},
    '7': {'train_idxs': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], 'val_idxs': [0, 1], 'test_idxs': [21, 22, 23]}
}


# Read nifti data
def load_data(data_path):
    data = nib.load(data_path).get_fdata().astype(np.float32)
    data = data.transpose((3, 0, 1, 2))  # transpose h*w*l*c to c*h*w*l
    return data


# Read nifti labels
def load_label(label_path):
    label = nib.load(label_path).get_fdata().astype(np.int32)
    return label


class ThalamusDataset(Dataset):

    def __init__(self, data_dir, label_1_dir, label_2_dir, split, division):
        super(ThalamusDataset, self).__init__()
        self.data_dir = data_dir
        self.label_1_dir = label_1_dir
        self.label_2_dir = label_2_dir
        self.split = split
        self.division = division
        self.data_file_list = sorted(list(os.listdir(self.data_dir)))
        self.label_1_file_list = sorted(list(os.listdir(self.label_1_dir)))
        self.label_2_file_list = sorted(list(os.listdir(self.label_2_dir)))

    def __len__(self):
        return len(config_split[self.split][self.division + "_idxs"])

    def __getitem__(self, idx):

        data_fn = [self.data_file_list[index] for index in config_split[self.split][self.division + "_idxs"]][idx]
        label_1_fn = [self.label_1_file_list[index] for index in config_split[self.split][self.division + "_idxs"]][idx]
        label_2_fn = [self.label_2_file_list[index] for index in config_split[self.split][self.division + "_idxs"]][idx]

        assert data_fn.split('_')[0] == label_1_fn.split('_')[0]
        data_path = os.path.join(self.data_dir, data_fn)
        label_1_path = os.path.join(self.label_1_dir, label_1_fn)
        label_2_path = os.path.join(self.label_2_dir, label_2_fn)

        data_np = load_data(data_path)
        label_1_np = load_label(label_1_path)
        label_2_np = load_label(label_2_path)

        data_np = center_crop(data_np, output_size=(96, 96, 96))
        label_1_np = center_crop(label_1_np, output_size=(96, 96, 96))
        label_2_np = center_crop(label_2_np, output_size=(96, 96, 96))

        data_tensor = torch.tensor(data_np, dtype=torch.float32)
        label_1_tensor = torch.tensor(label_1_np, dtype=torch.int32)
        label_2_tensor = torch.tensor(label_2_np, dtype=torch.int32)

        return data_tensor, label_1_tensor, label_2_tensor, data_fn, label_1_fn, label_2_fn


def ThalamusDataloader(data_dir, label_1_dir, label_2_dir, batch_size, split, division, shuffle=False, num_workers=8):
    dataset = ThalamusDataset(data_dir=data_dir, label_1_dir=label_1_dir, label_2_dir=label_2_dir, split=split, division=division)
    dataloader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
    return dataloader
