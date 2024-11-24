import astra.creators
import numpy as np
import matplotlib.pyplot as plt
import astra
import SimpleITK as sitk
import h5py

# Step 1: Define file paths and angles
num_projections = 90  # Total number of projections
file_pattern = "output/projections_{}.mhd"  # File naming pattern
angles = np.linspace(0, 180, num_projections, endpoint=False)  # Angles in degrees

# Convert angles to radians for ASTRA
angles_rad = np.deg2rad(angles)

# Step 2: Load all projections
projections = []
for i in range(num_projections):
    file = file_pattern.format(i)
    image = sitk.ReadImage(file)
    projection = sitk.GetArrayFromImage(image)[0]  # Assume single slice per projection
    projections.append(projection)

# Convert to NumPy array
projections = np.array(projections)  # Shape: (num_projections, detector_row_count, detector_col_count)
print("Projections shape:", projections.shape)

# Step 3: Prepare Data for ASTRA
# ASTRA expects data in shape (num_projections, detector_pixels)
# For 3D reconstruction, we'll handle slices individually or use 3D methods

# Get the dimensions
num_projections, detector_row_count, detector_col_count = projections.shape

# Step 4: Set up Geometry
# Define the geometry of the projection and the volume

# Volume geometry
vol_geom = astra.creators.create_vol_geom(detector_col_count, detector_col_count, detector_row_count)

# Projection geometry
proj_geom = astra.create_proj_geom(
    'parallel3d',
    1.0,  # Detector row spacing (adjust as necessary)
    1.0,  # Detector col spacing (adjust as necessary)
    detector_row_count,  # Number of detector rows (vertical direction)
    detector_col_count,  # Number of detector columns (horizontal direction)
    angles_rad  # Projection angles
)

# Step 5: Create ASTRA Data Objects
# Create a sinogram3d data object for projections
sinogram_id = astra.data3d.create('-sino', proj_geom, projections)

# Create a data object for the reconstruction
recon_id = astra.data3d.create('-vol', vol_geom)

# Step 6: Configure the Reconstruction Algorithm
# You can choose 'FDK_CUDA' for GPU acceleration or 'BP3D' for CPU
cfg = astra.astra_dict('FDK_CUDA')  # Or 'BP3D' for CPU-based backprojection
cfg['ReconstructionDataId'] = recon_id
cfg['ProjectionDataId'] = sinogram_id

# Step 7: Run the Reconstruction
alg_id = astra.algorithm.create(cfg)
astra.algorithm.run(alg_id)

# Get the reconstructed volume data
reconstruction = astra.data3d.get(recon_id)

# Step 8: Clean Up
astra.algorithm.delete(alg_id)
astra.data3d.delete(sinogram_id)
astra.data3d.delete(recon_id)

# Step 9: Visualize a Reconstructed Slice
slice_index = reconstruction.shape[0] // 2  # Middle slice
plt.imshow(reconstruction[slice_index], cmap='gray')
plt.title('Reconstructed Slice')
plt.colorbar()
plt.show()

# Step 10: Save the Reconstructed Volume
# Save as HDF5 file
with h5py.File('reconstructed_volume.h5', 'w') as hf:
    hf.create_dataset('reconstruction', data=reconstruction)

# Optionally, save as a series of images or other formats
