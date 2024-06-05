import random
import numpy as np
from scipy.ndimage import shift, rotate, zoom, map_coordinates, gaussian_filter


# Center Crop
def center_crop(img, output_size):
    is_label = len(img.shape) == 3
    center = [i // 2 for i in img.shape[-3:]]

    if is_label:
        start = [center[i] - output_size[i] // 2 for i in range(3)]
        end = [start[i] + output_size[i] for i in range(3)]
        cropped_img = img[start[0]:end[0], start[1]:end[1], start[2]:end[2]]
    else:
        start = [center[i] - output_size[i] // 2 for i in range(3)]
        end = [start[i] + output_size[i] for i in range(3)]
        cropped_img = img[:, start[0]:end[0], start[1]:end[1], start[2]:end[2]]

    return cropped_img


# Random Rotate
class RandomRotate:
    """
    Rotate the input by a random degrees within (-angle_spectrum, angle_spectrum) interval.
    Rotation axis is random picked.
    If the input is a label, with shape [H, W, L], nearest neighbor interpolation and nearest neighbor padding are adopted.
    If the input is a data, with shape [C, H, W, L], cubic spline interpolation and reflect padding are adopted.
    """

    def __init__(self, random_state, angle_spectrum=15, axes=[(1, 0), (2, 1), (2, 0)]):
        self.random_state = random_state
        self.angle_spectrum = angle_spectrum
        self.axes = axes

    def __call__(self, data, label):
        axis = self.axes[self.random_state.randint(len(self.axes))]
        angle = self.random_state.randint(-self.angle_spectrum, self.angle_spectrum)
        augmentation_details = f"rotate_angle:{angle}_axis:{axis}"

        # data
        assert data.ndim == 4
        data_mode = 'reflect'
        data_order = 3
        channels = [rotate(data[c], angle, axes=axis, reshape=False, order=data_order, mode=data_mode, ) for c in
                    range(data.shape[0])]
        data_out = np.stack(channels, axis=0)

        # label
        assert label.ndim == 3
        label_mode = 'nearest'
        label_order = 0
        label_out = rotate(label, angle, axes=axis, reshape=False, order=label_order, mode=label_mode)

        return data_out, label_out, augmentation_details


# Random Flip
class HorizontalFlip:
    """
    Horizontal flip or left-right flip the image along the x-axis.
    If the input is a label, with shape [H, W, L], nearest neighbor interpolation and nearest neighbor padding are adopted.
    If the input is a data, with shape [C, H, W, L], cubic spline interpolation and reflect padding are adopted.
    """

    def __init__(self, random_state):
        self.random_state = random_state
        self.axis = 0

    def __call__(self, data, label):
        augmentation_details = "flip_axis:{}".format(self.axis)

        # data
        assert data.ndim == 4
        channels = [np.flip(data[c], axis=self.axis).copy() for c in range(data.shape[0])]
        data_out = np.stack(channels, axis=0)

        # label
        assert label.ndim == 3
        label_out = np.flip(label, axis=self.axis).copy()

        return data_out, label_out, augmentation_details


# Random Zoom
class RandomZoom:
    """
    Zoom the input by a random zoom factor within the provided zoom range.
    If the input is a label, with shape [H, W, L], nearest neighbor interpolation and nearest neighbor padding are adopted.
    If the input is a data, with shape [C, H, W, L], cubic spline interpolation and reflect padding are adopted.
    """

    def __init__(self, random_state, zoom_range=(0.85, 1.15)):
        self.random_state = random_state
        self.zoom_range = zoom_range

    def __call__(self, data, label):
        zoom_factor = self.random_state.uniform(*self.zoom_range)
        augmentation_details = "zoom_factor:{}".format(zoom_factor)

        # data
        assert data.ndim == 4
        data_mode = 'reflect'
        data_order = 3
        channels = [zoom(data[c], zoom_factor, order=data_order, mode=data_mode, ) for c in range(data.shape[0])]
        data_out = np.stack(channels, axis=0)

        # label
        assert label.ndim == 3
        label_mode = 'nearest'
        label_order = 0
        label_out = zoom(label, zoom_factor, order=label_order, mode=label_mode)

        return data_out, label_out, augmentation_details


# Random Shift
class RandomShift:
    """
    Shift the input by a random offset within the provided shift range.
    If the input is a label, with shape [H, W, L], nearest neighbor interpolation and nearest neighbor padding are adopted.
    If the input is data, with shape [C, H, W, L], cubic spline interpolation (order=3) and reflect padding are adopted.
    """

    def __init__(self, random_state, shift_range=(-5, 5)):
        self.random_state = random_state
        self.shift_range = shift_range

    def __call__(self, data, label):
        # Generate random shifts for each axis
        shift_values = [self.random_state.uniform(self.shift_range[0], self.shift_range[1]) for _ in range(3)]
        augmentation_details = "shift_values:{}".format(shift_values)

        # data
        assert data.ndim == 4
        data_mode = 'reflect'
        data_order = 3
        channels = [shift(data[c], shift_values, order=data_order, mode=data_mode) for c in range(data.shape[0])]
        data_out = np.stack(channels, axis=0)

        # label
        assert label.ndim == 3
        label_mode = 'nearest'
        label_order = 0
        label_out = shift(label, shift_values, order=label_order, mode=label_mode)

        return data_out, label_out, augmentation_details


# Elastic Deformation
class ElasticDeformation:
    """
    Apply elasitc deformations of 3D patches on a per-voxel mesh. Assumes ZYX axis order (or CZYX if the data is 4D).
    param spline_order: the order of spline interpolation (use 0 for labeled images)
    param alpha: scaling factor for deformations
    param sigma: smoothing factor for Gaussian filter
    param execution_probability: probability of executing this transform
    param apply_3d: if True apply deformations in each axis
    """

    def __init__(self, random_state, alpha=2000, sigma=50):
        self.random_state = random_state
        self.alpha = alpha
        self.sigma = sigma

    def __call__(self, data, label):
        augmentation_details = "elastic_alpha:{} sigma:{}".format(self.alpha, self.sigma)

        assert data.ndim == 4
        assert label.ndim == 3
        assert data[0].shape == label.shape
        volume_shape = data[0].shape

        # generates deformation fields
        dz, dy, dx = [
            gaussian_filter(
                self.random_state.randn(*volume_shape),
                self.sigma,
                mode="reflect"
            ) * self.alpha for _ in range(3)
        ]
        z_dim, y_dim, x_dim = volume_shape
        z, y, x = np.meshgrid(np.arange(z_dim), np.arange(y_dim), np.arange(x_dim), indexing='ij')
        indices = z + dz, y + dy, x + dx

        # deformation field
        # deformation = np.stack([dz, dy, dx], axis=0)

        # data
        data_order = 3
        data_mode = 'reflect'
        channels = [map_coordinates(c, indices, order=data_order, mode=data_mode) for c in data]
        data_out = np.stack(channels, axis=0)

        # label
        label_order = 0
        label_mode = 'nearest'
        label_out = map_coordinates(label, indices, order=label_order, mode=label_mode)

        return data_out, label_out, augmentation_details


# Composition
class Compose:
    """
    Randomly picks two transformations from the provided list of transformations
    and applies them with a probability of 0.5 each.
    """

    def __init__(self, random_state, transformations=None):

        self.random_state = random_state

        if transformations is None:
            self.transformations = [
                RandomRotate(random_state),
                HorizontalFlip(random_state),
                RandomZoom(random_state),
                RandomShift(random_state),
                ElasticDeformation(random_state)
            ]
        else:
            self.transformations = transformations

    def __call__(self, data, label):

        applied_augmentations = []
        random.shuffle(self.transformations)

        for _ in range(2):
            transform = random.choice(self.transformations)
            if random.random() < 0.5:
                data, label, details = transform(data, label)
                applied_augmentations.append(details)

        augmentation_details = '|'.join(filter(None, applied_augmentations))

        return data, label, augmentation_details
