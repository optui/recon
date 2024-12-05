import numpy as np
import SimpleITK as sitk
import leapctype
from leap_preprocessing_algorithms import ringRemoval
import napari

# Step 1: Load projection data
projections = sitk.ReadImage("./output/projection.mhd")
projections_data = sitk.GetArrayFromImage(projections)

# Check projection dimensions
numAngles, numRows, numCols = projections_data.shape
print(f"Loaded Projections: {projections_data.shape} (Angles, Rows, Columns)")

# Step 2: Initialize LEAP tomographic model
lct = leapctype.tomographicModels()

# Set parallel beam geometry
pixelSize = 1.0  # Assuming 1 mm pixel size; adjust based on your setup
phis = lct.setAngleArray(numAngles, 360.0)  # Rotating 360 degrees for parallel beam

lct.set_parallelbeam(
    numAngles=numAngles,  # Number of projections (angles)
    numRows=numRows,      # Detector rows
    numCols=numCols,      # Detector columns
    pixelHeight=pixelSize, 
    pixelWidth=pixelSize,
    centerRow=0.5 * (numRows - 1),  # Center of the detector
    centerCol=0.5 * (numCols - 1),  # Center of the detector
    phis=phis                      # Projection angles
)

# Step 3: Set the reconstruction volume parameters
numX = numCols  # Reconstruction volume X dimension
numY = numRows  # Reconstruction volume Y dimension
numZ = numCols  # Reconstruction volume Z dimension (depth)
voxelWidth = pixelSize
voxelHeight = pixelSize
voxelDepth = pixelSize  # For isotropic voxels

lct.set_volume(
    numX=numX, numY=numY, numZ=numZ,
    voxelWidth=voxelWidth, voxelHeight=voxelHeight,
    offsetX=0.0, offsetY=0.0, offsetZ=0.0  # Set volume offset if needed
)

# Step 4: Allocate projections and reconstruction volume memory
g = lct.allocate_projections()  # Projections array
f = lct.allocate_volume()       # Reconstructed volume array

# Copy projection data into allocated array
g[:] = projections_data

# Step 5: Optional preprocessing (e.g., ring artifact removal)
print("Removing ring artifacts...")
ringRemoval(lct, g=g)

# Step 6: Perform reconstruction using Filtered Back Projection (FBP)
print("Performing reconstruction using FBP...")
lct.FBP(g, f)

# Step 7: Save or display reconstructed volume
print("Displaying reconstructed volume...")
napari.view_image(f, name='Reconstructed Volume', colormap='gray')

# Optionally save the reconstructed volume
reconstructed_volume = sitk.GetImageFromArray(f)
sitk.WriteImage(reconstructed_volume, "reconstructed_volume.mhd")
print("Reconstruction complete and saved to 'reconstructed_volume.mhd'.")
