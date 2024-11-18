from skimage.transform import iradon
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

sinograms = np.load('sinogram.npy')

num_slices, num_angles, detector_width = sinograms.shape

theta = np.arange(0, 180, 5)

reconstructed_slices = []

for i in range(num_slices):
    sinogram = sinograms[i]
    reconstructed_slice = iradon(sinogram.T, theta=theta, filter_name='ramp', circle=False)
    reconstructed_slices.append(reconstructed_slice)

reconstructed_volume = np.stack(reconstructed_slices, axis=1)

np.save('reconstructed_volume.npy', reconstructed_volume)

# Normalize the volume for visualization
volume_normalized = (reconstructed_volume - np.min(reconstructed_volume)) / (np.max(reconstructed_volume) - np.min(reconstructed_volume))

reconstructed_volume = np.load('reconstructed_volume.npy')

# Convert the NumPy array to a SimpleITK image
sitk_image = sitk.GetImageFromArray(reconstructed_volume)

# Save the image in MetaImage format
sitk.WriteImage(sitk_image, 'reconstructed_volume.mhd')

print("Reconstructed volume saved as MetaImage (.mhd)")