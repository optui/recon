import numpy as np
import astra
import matplotlib.pyplot as plt

# Configuration
dim_angles, dim_rows, dim_cols = 180, 256, 256
middle_row = dim_rows // 2

# Load and reshape raw data
sinogram = np.fromfile('output/projection.raw', dtype=np.float32).reshape((dim_angles, dim_rows, dim_cols))[:, middle_row, :]

# Visualization of sinogram
plt.imshow(sinogram, cmap='gray')
plt.title('Sinogram')
plt.xlabel('Detector Bins')
plt.ylabel('Angles')
plt.savefig("sinogram.png")

# Define angles and geometries for ASTRA
angles = np.linspace(0, np.pi, dim_angles, endpoint=False)
proj_geom = astra.create_proj_geom('parallel', 1.0, dim_cols, angles)
vol_geom = astra.create_vol_geom(dim_cols, dim_cols)
proj_id = astra.create_projector('linear', proj_geom, vol_geom)

# Create sinogram ID
sinogram_id = astra.data2d.create('-sino', proj_geom, sinogram)

# Create volume ID for the reconstruction
reconstruction_id = astra.data2d.create('-vol', vol_geom)

# Configure and run the FBP algorithm
cfg = astra.astra_dict('FBP')
cfg['ReconstructionDataId'] = reconstruction_id
cfg['ProjectorId'] = proj_id
cfg['ProjectionDataId'] = sinogram_id
cfg['FilterType'] = 'Ram-Lak'
fbp_id = astra.algorithm.create(cfg)
astra.algorithm.run(fbp_id)

# Retrieve the reconstructed image
reconstructed_image = astra.data2d.get(reconstruction_id)

# Visualize reconstructed image
plt.imshow(reconstructed_image, cmap='gray')
plt.title('Reconstructed Image (FBP with Ram-Lak)')
plt.savefig("fbp_ram_lak_reconstruction.png")

# Cleanup
astra.algorithm.delete(fbp_id)
astra.data2d.delete(sinogram_id)
astra.data2d.delete(reconstruction_id)
