import torch
import numpy as np


def one_hot_encoding(gt, gt_values, num_classes):
    """
    Convert ground truth to one-hot encoding.

    gt (torch.Tensor): Ground truth labels, with shape [batch_size, H, W, L]
    gt_values (list): A list of unique values present in the ground truth labels, corresponding to the distinct classes.
                          For example [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0].
    num_classes (int): The total number of classes present in the ground truth data. This number should
                           match the length of the gt_values list.
    """
    one_hot = torch.zeros(gt.size(0), num_classes, *gt.size()[1:], device=gt.device)
    for idx in range(num_classes):
        one_hot[:, idx, ...] = (gt == gt_values[idx]).float()
    return one_hot


def center_crop(img, crop_size):

    """ Perform a center crop on the input image. """

    num_dims = len(img.shape)
    center = [i // 2 for i in img.shape[-3:]]

    start = [center[i] - crop_size[i] // 2 for i in range(3)]
    end = [start[i] + crop_size[i] for i in range(3)]

    if num_dims == 3:
        return img[start[0]:end[0], start[1]:end[1], start[2]:end[2]]
    elif num_dims == 4:
        return img[:, start[0]:end[0], start[1]:end[1], start[2]:end[2]]
    else:
        raise ValueError("Input must be a 3D or 4D array")


def pad_to_original_size(pred, original_shape):

    """ Pad the prediction array back to its original size. """

    padding = []
    for pred_dim, orig_dim in zip(pred.shape, original_shape):
        total_pad = orig_dim - pred_dim
        pad_before = total_pad // 2
        pad_after = total_pad - pad_before
        padding.append((pad_before, pad_after))

    padded_pred = np.pad(pred, padding, mode='constant', constant_values=0)

    return padded_pred

