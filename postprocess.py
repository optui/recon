import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Define file paths and angles
num_projections = 90 # Total number of projections
file_pattern = "output/projections_{}.mhd"  # File naming pattern
angles = np.linspace(0, 180, num_projections, endpoint=False)  # Assuming evenly spaced angles

# Step 2: Load all projections
projections = []
for i in range(num_projections):
    file = file_pattern.format(i)
    image = sitk.ReadImage(file)
    projection = sitk.GetArrayFromImage(image)[0]  # Assume single slice per projection
    projections.append(projection)

# Convert to NumPy array
projections = np.array(projections)  # Shape: (num_projections, height, width)
print("Projections shape:", projections.shape)

# Step 3: Construct the sinogram
height, width = projections.shape[1:]
sinograms = []
for row in range(height):  # Create sinograms for all rows
    sinogram = projections[:, row, :]  # Extract sinogram for the current row
    sinograms.append(sinogram)

# Convert to NumPy array
sinograms = np.array(sinograms)  # Shape: (height, num_projections, width)
print("Sinograms shape:", sinograms.shape)

# Step 4: Save sinograms for reconstruction
np.save("sinogram.npy", sinograms)

# Step 5: Visualize one sinogram (middle row)
middle_row = sinograms[height // 2]  # Middle row sinogram
plt.imshow(
    middle_row.T,
    cmap="gray",
    aspect="auto",
    extent=[angles[0], angles[-1], 0, width],
)
plt.colorbar(label="Intensity")
plt.title("Sinogram (Middle Row)")
plt.xlabel("Projection Angle (degrees)")
plt.ylabel("Detector Position")
plt.savefig("sinogram_middle_row.png")
plt.show()

# Step 6: Visualize entire sinogram collapsed over all rows
collapsed_sinogram = sinograms.mean(axis=0)  # Collapse sinograms over rows
plt.imshow(
    collapsed_sinogram.T,
    cmap="gray",
    aspect="auto",
    extent=[angles[0], angles[-1], 0, width],
)
plt.colorbar(label="Intensity")
plt.title("Collapsed Sinogram")
plt.xlabel("Projection Angle (degrees)")
plt.ylabel("Detector Position")
plt.savefig("collapsed_sinogram.png")
plt.show()
