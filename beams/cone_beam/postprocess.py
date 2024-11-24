from matplotlib import pyplot as plt
from skimage.transform import iradon
import numpy as np
import SimpleITK as sitk
import os

# Path to the directory containing the projection files
output_dir = "./output"
n_projections = 10  # Number of projections

# Load projections
projections = []
for i in range(n_projections):
    filename = os.path.join(output_dir, f"fluence_projection_{i:03d}.mhd")
    image = sitk.ReadImage(filename)
    array = sitk.GetArrayFromImage(image)  # Convert to numpy array
    projections.append(array[0, :, :])  # Extract 2D projection

# Stack projections into a 3D numpy array
projections = np.stack(projections, axis=0)

# Define angles for each projection (in degrees)
angles = np.linspace(0, 360, n_projections, endpoint=False)

# Initialize an empty list to store reconstructed slices
reconstructed_slices = []

# Loop through all z-planes (axial slices)
for z_index in range(projections.shape[1]):  # Iterate through all axial slices
    # Extract sinogram for the current z-plane
    sinogram = projections[:, z_index, :]  # Shape: (n_projections, detector_pixels)

    # Perform filtered backprojection for the current slice
    reconstructed_slice = iradon(sinogram.T, theta=angles, circle=True)
    reconstructed_slices.append(reconstructed_slice)

# Stack all reconstructed slices to create a 3D volume
reconstructed_volume = np.stack(reconstructed_slices, axis=0)

# Visualize the middle slice in the reconstructed volume
plt.imshow(reconstructed_volume[reconstructed_volume.shape[0] // 2, :, :], cmap="gray")
plt.title("Central Slice of Reconstructed Volume")
plt.colorbar(label="Intensity")
plt.show()

# Save the reconstructed volume as a 3D image
reconstructed_image = sitk.GetImageFromArray(reconstructed_volume)
sitk.WriteImage(reconstructed_image, "reconstructed_volume.mhd")
