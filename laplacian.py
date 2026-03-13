import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import imageio.v2 as imageio

# Load image (grayscale)
try:
    img = imageio.imread('road01.jpg', pilmode='L')  # Replace with your image path
except FileNotFoundError:
    print("Error: Image file not found. Please check the path.")
    exit(1)

# Convert to float for processing
img = img.astype(float)

# Apply Laplacian of Gaussian filter
# sigma controls the Gaussian smoothing (higher sigma = more smoothing)
sigma = 2.0
log_img = ndimage.gaussian_laplace(img, sigma=sigma)

# The Laplacian of Gaussian produces negative values for edges,
# so we take the absolute value for visualization
log_abs = np.abs(log_img)

# Normalize for display
log_abs = (log_abs / log_abs.max()) * 255

# Display results
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title(f"Laplacian of Gaussian (σ={sigma})")
plt.imshow(log_abs, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.show()