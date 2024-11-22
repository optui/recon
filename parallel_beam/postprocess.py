import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Load the projection data
projection_file = "output/projection.mhd"
projections = sitk.GetArrayFromImage(sitk.ReadImage(projection_file))

# projections shape: (Z, Y, X) -> (n_projections, detector_height, detector_width)
print("Projections shape:", projections.shape)

# Choose a specific row to extract the sinogram
row_index = projections.shape[1] // 2  # Middle row
sinogram = projections[:, row_index, :]

# Save the sinogram as a .npy file
np.save("sinogram.npy", sinogram)
print("Sinogram saved to 'sinogram.npy'.")

# Plot the sinogram with aspect ratio matching its dimensions
plt.figure(figsize=(sinogram.shape[1] / 190, sinogram.shape[0] / 190))  # Adjust size dynamically
plt.imshow(sinogram, aspect='auto', cmap='gray')
plt.axis('off')  # Turn off axis for clean output
plt.savefig("sinogram.png", bbox_inches='tight', pad_inches=0, dpi=300)

# Load the sinogram image
image_path = "sinogram.png"
image = Image.open(image_path).convert("L")  # Convert to grayscale
sinogram_array = np.array(image)

# Find non-black columns (where the maximum value along the column is greater than 0)
non_black_cols = np.where(sinogram_array.max(axis=0) > 0)[0]

# Crop horizontally to remove black margins
cropped_sinogram = sinogram_array[:, non_black_cols[0]:non_black_cols[-1] + 1]

# Plot the horizontally cropped sinogram with adjusted size
plt.figure(figsize=(cropped_sinogram.shape[1] / 190, cropped_sinogram.shape[0] / 190))
plt.imshow(cropped_sinogram, aspect='auto', cmap='gray')
plt.axis('off')  # Turn off the axis for display
plt.savefig("sinogram.png", bbox_inches='tight', pad_inches=0, dpi=300)
