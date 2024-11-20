from skimage.transform import iradon
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt

# Load the projection data
projection_file = "output/projections.mhd"
projections = sitk.GetArrayFromImage(sitk.ReadImage(projection_file))

# Check projection data shape
print(f"Projections shape: {projections.shape} (n_projections, detector_height, detector_width)")

# Define the projection angles (theta)
angles = np.linspace(0, 360, projections.shape[0], endpoint=False)

# Extract a sinogram for a specific row (e.g., center row)
row_index = projections.shape[1] // 2  # Middle row of the detector
sinogram = projections[:, row_index, :]  # (n_projections, detector_width)

# Save the sinogram (optional)
np.save("cbct_sinogram.npy", sinogram)

# Visualize the sinogram
plt.figure(figsize=(10, 6))
plt.imshow(sinogram, cmap="gray", aspect="auto")
plt.colorbar(label="Intensity")
plt.title("CBCT Sinogram")
plt.xlabel("Detector Elements")
plt.ylabel("Projection Angle (Degrees)")
plt.savefig("cbct_sinogram.png")
plt.show()
