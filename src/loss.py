import torch
import torch.nn as nn
from utils.utils import one_hot_encoding


class DiceLoss(nn.Module):
    """
    Construct based on Vnet paper 'https://arxiv.org/abs/1606.04797'
    Handle both one-hot encoded and non-one-hot encoded ground truth.

    Attributes:
        num_classes (int): The number of classes in the segmentation task.
        eps (float): A small value added to the denominator for numerical stability.
        isOneHot (bool): A flag indicating whether `ground_truth` is already one-hot encoded.
        gt_values (list): The list of unique values in `ground_truth` for one-hot encoding.
        isPlotPerChannelLoss (bool): A flag indicating whether to return the Dice loss per channel.
    """

    def __init__(self, num_classes, eps=1e-6, isOneHot=False, gt_values=None, isPlotPerChannelLoss=False):
        super(DiceLoss, self).__init__()
        self.num_classes = num_classes
        self.eps = eps
        self.isOneHot = isOneHot
        self.gt_values = gt_values
        self.isPlotPerChannelLoss = isPlotPerChannelLoss

    def forward(self, prediction, ground_truth):
        # Perform one-hot encoding conversion if needed
        if not self.isOneHot:
            if self.gt_values is None:
                raise ValueError("gt_values must be provided if ground truth is not one-hot encoded.")
            ground_truth = one_hot_encoding(ground_truth, self.gt_values, self.num_classes)

        # Calculate the intersection and union
        intersection = torch.sum(prediction * ground_truth, dim=(2, 3, 4))
        union = torch.sum(prediction ** 2, dim=(2, 3, 4)) + torch.sum(ground_truth ** 2, dim=(2, 3, 4))

        # Calculate Dice Score per channel
        dice_score_channel = (2 * intersection + self.eps) / (union + self.eps)
        dice_score_channel = torch.mean(dice_score_channel, dim=0)

        # Calculate overall Dice Score (mean over all channels)
        dice_score_overall = torch.mean(dice_score_channel)

        # Calculate Dice Loss per channel and overall
        dice_loss_channel = 1 - dice_score_channel
        dice_loss_overall = 1 - dice_score_overall

        return (dice_loss_overall, dice_loss_channel) if self.isPlotPerChannelLoss else dice_loss_overall

