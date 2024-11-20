import numpy as np
from skimage.transform import iradon
import matplotlib.pyplot as plt

# Load the saved sinogram
sinogram = np.load("sinogram.npy")
print("Loaded sinogram shape:", sinogram.shape)

# Define the projection angles (theta)
theta = np.linspace(0., 180., num=sinogram.shape[0], endpoint=False)

# Apply inverse Radon transform
reconstructed_slice = iradon(sinogram.T, theta=theta, circle=False, filter='ramp')

# Visualize the reconstructed slice
plt.figure(figsize=(8, 8))
plt.imshow(reconstructed_slice, cmap='gray')
plt.colorbar()
plt.title("Reconstructed Slice (Box)")
plt.savefig("reconstructed_box.png")
