import torch
import os
import numpy as np


class SaveBestModel:

    """ Saves the model checkpoint if validation loss decreases. """

    def __init__(self, verbose=True, save_path='.'):
        """
        verbose (bool): If True, prints a message for each validation loss improvement.
        save_path (str): Path for the checkpoint to be saved to.
        """
        self.verbose = verbose
        self.val_loss_min = np.Inf
        self.save_path = save_path

    def __call__(self, val_loss, model, train_losses, val_losses, epoch):

        if val_loss < self.val_loss_min:
            if self.verbose:
                print(f'Validation loss decreased ({self.val_loss_min:.6f} --> {val_loss:.6f}). Saving model ...')
            self.save_checkpoint(model, train_losses, val_losses, epoch)
            self.val_loss_min = val_loss

    def save_checkpoint(self, model, train_losses, val_losses, epoch):
        state = {
            'epoch': epoch,
            'state_dict': model.state_dict(),
            'train_losses': train_losses,
            'val_losses': val_losses
        }
        torch.save(state, os.path.join(self.save_path, 'best_checkpoint.pt'))