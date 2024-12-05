import numpy as np
import napari

# Load the volume
volume = np.load('reconstructed_volume.npy')

# Normalize the volume for better visualization
volume_norm = (volume - volume.min()) / (volume.max() - volume.min())

# Start napari viewer with both regular and normalized volumes
viewer = napari.Viewer()
viewer.add_image(volume, name='Original')
viewer.add_image(volume_norm, name='Normalized')

napari.run()  # Start the Qt event loop
