import os
import sys
import torch
import argparse
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import torch.optim as optim
import torch.nn as nn

sys.path.append('../src')
from loss import DiceLoss
from utils.save_best_model import SaveBestModel
from dataloaders.dataloader_train import ThalamusDataloader
from models.unet3d import UnetL5


gt_values = list(range(2))
device = torch.device("cuda")

# Fix random seeds
seed = 1234
torch.manual_seed(seed)
torch.cuda.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
np.random.seed(seed)


def train(train_loaders, model, lossfn, optimizer, epoch):
    model.train()
    progress_bar = tqdm(train_loaders, desc="Training")
    total_loss = 0.0

    for batch_idx, (data, target) in enumerate(progress_bar):

        data = data.type(torch.float32).to(device)
        target = target.type(torch.float32).to(device)

        optimizer.zero_grad()
        pred = model(data)

        loss = lossfn(pred, target)
        loss.backward()
        optimizer.step()

        total_loss += loss.data.item()
        avg_loss = total_loss / (batch_idx + 1)
        progress_bar.set_description('epoch index {} loss:{:.6f}'.format(epoch,  avg_loss))

    return avg_loss


def val(val_loaders, model, lossfn, epoch):
    model.eval()
    progress_bar = tqdm(val_loaders, desc='Validation')
    total_loss = 0.0

    with torch.no_grad():
        for batch_idx, (data, target) in enumerate(progress_bar):

            data = data.type(torch.float32).to(device)
            target = target.type(torch.float32).to(device)

            pred = model(data)
            loss = lossfn(pred, target)

            total_loss += loss.data.item()
            avg_loss = total_loss / (batch_idx + 1)
            progress_bar.set_description('Epoch: {} test loss: {:.6f}'.format(epoch, avg_loss))

    return avg_loss


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Train ROI model.")
    parser.add_argument('--data_dir', type=str, required=True, help='Root folder for the data.')
    parser.add_argument('--label_dir', type=str, required=True, help='Root folder for the ground truth labels.')
    parser.add_argument('--out_dir', type=str, required=True, help='Folder to save the training results.')
    parser.add_argument('--split', type=str, required=True, help='Data split for 8 folds.')
    parser.add_argument('--train_batch_size', type=int, default=4, help='Batch size for training.')
    parser.add_argument('--val_batch_size', type=int, default=1, help='Batch size for validation.')
    parser.add_argument('--resume_epoch', type=int, default=-1, help='Epoch to resume training from (default: -1 for none).')
    parser.add_argument('--epochs', type=int, default=100, help='Number of training epochs.')
    parser.add_argument('--lr', type=float, default=1e-3, help='Learning rate.')
    parser.add_argument('--wd', type=float, default=1e-4, help='Weight decay.')
    parser.add_argument('--num_in', type=int, default=68, help='Number of input channels.')
    args = parser.parse_args()

    print("=="*50)
    print("Eight Fold Experiment Split ", args.split)
    print("=="*50)

    # creating folders to save results
    if not os.path.exists(args.out_dir):
        print('creating:', args.out_dir)
        os.makedirs(args.out_dir)

    split_dir = os.path.join(args.out_dir, args.split)
    if not os.path.exists(split_dir):
        print('creating:', split_dir)
        os.mkdir(split_dir)

    checkpoint_dir = os.path.join(split_dir, 'checkpoint')
    if not os.path.exists(checkpoint_dir):
        print('creating:', checkpoint_dir)
        os.mkdir(checkpoint_dir)

    # model, loss, optimizer, scheduler and early stop
    model = UnetL5(in_dim=args.num_in, out_dim=2, num_filters=4, output_activation=nn.Sigmoid()).to(device)
    lossfn = DiceLoss(num_classes=2, isOneHot=False, gt_values=gt_values, isPlotPerChannelLoss=False)
    optimizer = optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.wd)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', patience=5, factor=0.9)
    save_best_model = SaveBestModel(verbose=True, save_path=split_dir)

    # whether resume training
    startEpoch = -1
    if args.resume_epoch > 0:
        print("Resume Training from %d" % args.resume_epoch)
        startEpoch = args.resume_epoch
        resumed_checkpoint = os.path.join(checkpoint_dir, str(args.resume_epoch) + '.pt')
        resume_state = torch.load(resumed_checkpoint, map_location=device)
        model.load_state_dict(resume_state['state_dict'])
        train_losses = resume_state['train_losses']
        val_losses = resume_state['test_losses']
    else:
        train_losses, val_losses = [], []

    # start training
    for epoch in range(startEpoch + 1, args.epochs):

        train_loaders = ThalamusDataloader(data_dir=args.data_dir,
                                           label_dir=args.label_dir,
                                           batch_size=args.train_batch_size,
                                           split=args.split,
                                           division="train",
                                           shuffle=True)

        val_loaders = ThalamusDataloader(data_dir=args.data_dir,
                                         label_dir=args.label_dir,
                                         batch_size=args.val_batch_size,
                                         split=args.split,
                                         division="val")

        # training
        train_avg_loss = train(train_loaders, model, lossfn, optimizer, epoch)
        train_losses.append(train_avg_loss)

        # validation
        val_avg_loss = val(val_loaders, model, lossfn, epoch)
        val_losses.append(val_avg_loss)

        # adjust lr
        scheduler.step(val_avg_loss)

        # save model/checkpoint
        state = {'state_dict': model.state_dict(),
                 'train_losses': train_losses,
                 'val_losses': val_losses}
        torch.save(state, os.path.join(checkpoint_dir, str(epoch) + '.pt'))
        save_best_model(val_avg_loss, model, train_losses, val_losses, epoch)

        # save train loss and test loss for each epoch
        np.savez(os.path.join(split_dir, 'train_losses.npz'), train_losses)
        np.savez(os.path.join(split_dir, 'val_losses.npz'), val_losses)

        # plot training and testing loss
        fig = plt.figure(figsize=(20, 24))
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(313)

        ax1.plot(train_losses, color='darkred', marker='o')
        ax1.set_title('train loss')
        ax1.set_xlabel('epoch')
        ax1.set_ylabel('loss')

        ax2.plot(val_losses, color='b', marker='o')
        ax2.set_title('val loss')
        ax2.set_xlabel('epoch')
        ax2.set_ylabel('loss')

        ax3.plot(train_losses, color='darkred', marker='o')
        ax3.plot(val_losses, color='b', marker='o')
        ax3.set_title('training and validation loss')
        ax3.set_xlabel('epoch')
        ax3.set_ylabel('loss')
        ax3.legend(['train', 'val'])

        plt.tight_layout()
        plt.savefig(os.path.join(split_dir, 'losses.png'))
        plt.close(fig)

