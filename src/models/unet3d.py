import torch
import torch.nn as nn


def conv_block_3d(in_dim: int, out_dim: int, activation: nn.Module) -> nn.Sequential:
    return nn.Sequential(
        nn.Conv3d(in_dim, out_dim, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm3d(out_dim),
        activation
    )


def conv_block_2_3d(in_dim: int, out_dim: int, activation: nn.Module) -> nn.Sequential:
    return nn.Sequential(
        conv_block_3d(in_dim, out_dim, activation),
        nn.Conv3d(out_dim, out_dim, kernel_size=3, stride=1, padding=1),
        nn.BatchNorm3d(out_dim)
    )


def conv_trans_block_3d(in_dim: int, out_dim: int, activation: nn.Module) -> nn.Sequential:
    return nn.Sequential(
        nn.ConvTranspose3d(in_dim, out_dim, kernel_size=3, stride=2, padding=1, output_padding=1),
        nn.BatchNorm3d(out_dim),
        activation
    )


def conv_block_out_3d(in_dim: int, out_dim: int) -> nn.Sequential:
    return nn.Sequential(
        nn.Conv3d(in_dim, out_dim, kernel_size=3, stride=1, padding=1)
    )


def conv_block_out_activate_3d(in_dim: int, out_dim: int, activation: nn.Module) -> nn.Sequential:
    return nn.Sequential(
        nn.Conv3d(in_dim, out_dim, kernel_size=3, stride=1, padding=1),
        activation
    )


def max_pooling_3d() -> nn.MaxPool3d:
    return nn.MaxPool3d(kernel_size=2, stride=2, padding=0)


class UnetL3(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, num_filters: int,
                 activation: nn.Module = nn.LeakyReLU(0.2, inplace=True), output_activation: nn.Module = None):
        super(UnetL3, self).__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.num_filters = num_filters
        self.activation = activation
        self.output_activation = output_activation

        # Down sampling
        self.down_1 = conv_block_2_3d(self.in_dim, self.num_filters, self.activation)
        self.pool_1 = max_pooling_3d()
        self.down_2 = conv_block_2_3d(self.num_filters, self.num_filters * 2, self.activation)
        self.pool_2 = max_pooling_3d()
        self.down_3 = conv_block_2_3d(self.num_filters * 2, self.num_filters * 4, self.activation)
        self.pool_3 = max_pooling_3d()

        # Bridge
        self.bridge = conv_block_2_3d(self.num_filters * 4, self.num_filters * 8, self.activation)

        # Up sampling
        self.trans_1 = conv_trans_block_3d(self.num_filters * 8, self.num_filters * 8, self.activation)
        self.up_1 = conv_block_2_3d(self.num_filters * 12, self.num_filters * 4, self.activation)
        self.trans_2 = conv_trans_block_3d(self.num_filters * 4, self.num_filters * 4, self.activation)
        self.up_2 = conv_block_2_3d(self.num_filters * 6, self.num_filters * 2, self.activation)
        self.trans_3 = conv_trans_block_3d(self.num_filters * 2, self.num_filters * 2, self.activation)
        self.up_3 = conv_block_2_3d(self.num_filters * 3, self.num_filters, self.activation)

        # Output
        if self.output_activation:
            self.out = conv_block_out_activate_3d(num_filters, out_dim, self.output_activation)
        else:
            self.out = conv_block_out_3d(num_filters, out_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Down sampling
        down_1 = self.down_1(x)
        pool_1 = self.pool_1(down_1)

        down_2 = self.down_2(pool_1)
        pool_2 = self.pool_2(down_2)

        down_3 = self.down_3(pool_2)
        pool_3 = self.pool_3(down_3)

        # Bridge
        bridge = self.bridge(pool_3)

        # Up sampling
        trans_1 = self.trans_1(bridge)
        concat_1 = torch.cat([trans_1, down_3], dim=1)
        up_1 = self.up_1(concat_1)

        trans_2 = self.trans_2(up_1)
        concat_2 = torch.cat([trans_2, down_2], dim=1)
        up_2 = self.up_2(concat_2)

        trans_3 = self.trans_3(up_2)
        concat_3 = torch.cat([trans_3, down_1], dim=1)
        up_3 = self.up_3(concat_3)

        # Output
        out = self.out(up_3)
        return out


class UnetL4(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, num_filters: int,
                 activation: nn.Module = nn.LeakyReLU(0.2, inplace=True), output_activation: nn.Module = None):
        super(UnetL4, self).__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.num_filters = num_filters
        self.activation = activation
        self.output_activation = output_activation

        # Down sampling
        self.down_1 = conv_block_2_3d(self.in_dim, self.num_filters, self.activation)
        self.pool_1 = max_pooling_3d()
        self.down_2 = conv_block_2_3d(self.num_filters, self.num_filters * 2, self.activation)
        self.pool_2 = max_pooling_3d()
        self.down_3 = conv_block_2_3d(self.num_filters * 2, self.num_filters * 4, self.activation)
        self.pool_3 = max_pooling_3d()
        self.down_4 = conv_block_2_3d(self.num_filters * 4, self.num_filters * 8, self.activation)
        self.pool_4 = max_pooling_3d()

        # Bridge
        self.bridge = conv_block_2_3d(self.num_filters * 8, self.num_filters * 16, self.activation)

        # Up sampling
        self.trans_1 = conv_trans_block_3d(self.num_filters * 16, self.num_filters * 16, self.activation)
        self.up_1 = conv_block_2_3d(self.num_filters * 24, self.num_filters * 8, self.activation)
        self.trans_2 = conv_trans_block_3d(self.num_filters * 8, self.num_filters * 8, self.activation)
        self.up_2 = conv_block_2_3d(self.num_filters * 12, self.num_filters * 4, activation)
        self.trans_3 = conv_trans_block_3d(self.num_filters * 4, self.num_filters * 4, self.activation)
        self.up_3 = conv_block_2_3d(self.num_filters * 6, self.num_filters * 2, self.activation)
        self.trans_4 = conv_trans_block_3d(self.num_filters * 2, self.num_filters * 2, self.activation)
        self.up_4 = conv_block_2_3d(self.num_filters * 3, self.num_filters, self.activation)

        # Output
        if self.output_activation:
            self.out = conv_block_out_activate_3d(num_filters, out_dim, self.output_activation)
        else:
            self.out = conv_block_out_3d(num_filters, out_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Down sampling
        down_1 = self.down_1(x)
        pool_1 = self.pool_1(down_1)

        down_2 = self.down_2(pool_1)
        pool_2 = self.pool_2(down_2)

        down_3 = self.down_3(pool_2)
        pool_3 = self.pool_3(down_3)

        down_4 = self.down_4(pool_3)
        pool_4 = self.pool_4(down_4)

        # Bridge
        bridge = self.bridge(pool_4)

        # Up sampling
        trans_1 = self.trans_1(bridge)
        concat_1 = torch.cat([trans_1, down_4], dim=1)
        up_1 = self.up_1(concat_1)

        trans_2 = self.trans_2(up_1)
        concat_2 = torch.cat([trans_2, down_3], dim=1)
        up_2 = self.up_2(concat_2)

        trans_3 = self.trans_3(up_2)
        concat_3 = torch.cat([trans_3, down_2], dim=1)
        up_3 = self.up_3(concat_3)

        trans_4 = self.trans_4(up_3)
        concat_4 = torch.cat([trans_4, down_1], dim=1)
        up_4 = self.up_4(concat_4)

        # Output
        out = self.out(up_4)
        return out


class UnetL5(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, num_filters: int,
                 activation: nn.Module = nn.LeakyReLU(0.2, inplace=True), output_activation: nn.Module = None):
        super(UnetL5, self).__init__()
        self.in_dim = in_dim
        self.out_dim = out_dim
        self.num_filters = num_filters
        self.activation = activation
        self.output_activation = output_activation

        # Down sampling
        self.down_1 = conv_block_2_3d(self.in_dim, self.num_filters, self.activation)
        self.pool_1 = max_pooling_3d()
        self.down_2 = conv_block_2_3d(self.num_filters, self.num_filters * 2, self.activation)
        self.pool_2 = max_pooling_3d()
        self.down_3 = conv_block_2_3d(self.num_filters * 2, self.num_filters * 4, self.activation)
        self.pool_3 = max_pooling_3d()
        self.down_4 = conv_block_2_3d(self.num_filters * 4, self.num_filters * 8, self.activation)
        self.pool_4 = max_pooling_3d()
        self.down_5 = conv_block_2_3d(self.num_filters * 8, self.num_filters * 16, self.activation)
        self.pool_5 = max_pooling_3d()

        # Bridge
        self.bridge = conv_block_2_3d(self.num_filters * 16, self.num_filters * 32, self.activation)

        # Up sampling
        self.trans_1 = conv_trans_block_3d(self.num_filters * 32, self.num_filters * 32, self.activation)
        self.up_1 = conv_block_2_3d(self.num_filters * 48, self.num_filters * 16, self.activation)
        self.trans_2 = conv_trans_block_3d(self.num_filters * 16, self.num_filters * 16, self.activation)
        self.up_2 = conv_block_2_3d(self.num_filters * 24, self.num_filters * 8, self.activation)
        self.trans_3 = conv_trans_block_3d(self.num_filters * 8, self.num_filters * 8, self.activation)
        self.up_3 = conv_block_2_3d(self.num_filters * 12, self.num_filters * 4, self.activation)
        self.trans_4 = conv_trans_block_3d(self.num_filters * 4, self.num_filters * 4, self.activation)
        self.up_4 = conv_block_2_3d(self.num_filters * 6, self.num_filters * 2, self.activation)
        self.trans_5 = conv_trans_block_3d(self.num_filters * 2, self.num_filters * 2, self.activation)
        self.up_5 = conv_block_2_3d(self.num_filters * 3, self.num_filters * 1, self.activation)

        # Output
        if self.output_activation:
            self.out = conv_block_out_activate_3d(num_filters, out_dim, self.output_activation)
        else:
            self.out = conv_block_out_3d(num_filters, out_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # Down sampling
        down_1 = self.down_1(x)
        pool_1 = self.pool_1(down_1)

        down_2 = self.down_2(pool_1)
        pool_2 = self.pool_2(down_2)

        down_3 = self.down_3(pool_2)
        pool_3 = self.pool_3(down_3)

        down_4 = self.down_4(pool_3)
        pool_4 = self.pool_4(down_4)

        down_5 = self.down_5(pool_4)
        pool_5 = self.pool_5(down_5)

        # Bridge
        bridge = self.bridge(pool_5)

        # Up sampling
        trans_1 = self.trans_1(bridge)
        concat_1 = torch.cat([trans_1, down_5], dim=1)
        up_1 = self.up_1(concat_1)

        trans_2 = self.trans_2(up_1)
        concat_2 = torch.cat([trans_2, down_4], dim=1)
        up_2 = self.up_2(concat_2)

        trans_3 = self.trans_3(up_2)
        concat_3 = torch.cat([trans_3, down_3], dim=1)
        up_3 = self.up_3(concat_3)

        trans_4 = self.trans_4(up_3)
        concat_4 = torch.cat([trans_4, down_2], dim=1)
        up_4 = self.up_4(concat_4)

        trans_5 = self.trans_5(up_4)
        concat_5 = torch.cat([trans_5, down_1], dim=1)
        up_5 = self.up_5(concat_5)

        # Output
        out = self.out(up_5)
        return out
