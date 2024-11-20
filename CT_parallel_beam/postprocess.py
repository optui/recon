import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

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

# Plot the sinogram
plt.figure(figsize=(10, 6))
plt.imshow(sinogram, aspect='auto', cmap='gray')
plt.colorbar()
plt.title("Sinogram")
plt.xlabel("Detector Elements")
plt.ylabel("Projection Angle")
plt.savefig("singoram.png")
