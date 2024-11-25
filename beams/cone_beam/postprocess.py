import SimpleITK as sitk
import numpy as np
import astra

# Load all projections
n_projections = 180
projections = []

for i in range(n_projections):
    image = sitk.ReadImage(f"output/fluence_{i}.mhd")
    proj = sitk.GetArrayFromImage(image)
    proj = np.squeeze(proj)
    projections.append(proj)
projections = np.array(projections)

print(projections.shape)  # (180, 512, 512)

# Get dimensions from projections
_, det_row_count, det_col_count = projections.shape

# Define geometry parameters
vol_size = 512  # assuming cubic volume
det_spacing_x = 1.0  # detector pixel size in mm
det_spacing_y = 1.0  # detector pixel size in mm
source_origin = 1000  # distance from source to rotation center in mm
origin_det = 536    # distance from rotation center to detector in mm
angles = np.linspace(0, 2*np.pi, n_projections, False)  # projection angles

# Create volume geometry
vol_geom = astra.create_vol_geom(vol_size, vol_size, vol_size)

# Create projection geometry
proj_geom = astra.create_proj_geom('cone', 
                                  det_spacing_x, det_spacing_y,
                                  det_row_count, det_col_count,
                                  angles, 
                                  source_origin, origin_det)

# Create projector
projector_id = astra.create_projector('cuda3d', proj_geom, vol_geom)

# Transpose projections to match ASTRA's expected dimensions
projections = np.transpose(projections, (1, 0, 2))

# Create sinogram
sinogram_id = astra.data3d.create('-sino', proj_geom, projections)

# Get the sinogram data and save it
sinogram_data = astra.data3d.get(sinogram_id)

# Save as MetaImage format (MHD/RAW)
sinogram_sitk = sitk.GetImageFromArray(sinogram_data)
sitk.WriteImage(sinogram_sitk, "sinogram.mhd")

