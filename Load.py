import rasterio
import os
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Transformer, CRS

dsm_directory = '/Users/dorian/Documents/2024_2/Capstone/lds-waikato-region-3layers-GTiff/waikato-lidar-1m-dsm-2021'
dem_directory = '/Users/dorian/Documents/2024_2/Capstone/lds-waikato-region-3layers-GTiff/waikato-lidar-1m-dem-2021'
aer_directory = '/Users/dorian/Documents/2024_2/Capstone/lds-waikato-region-3layers-GTiff/waikato-03m-rural-aerial-photos-2021-2023'

# base_name --> [DEM(image, transform), DSM(image, transform)]
data = {}

for filename in os.listdir(dem_directory):
    if filename.endswith('.tif'):
        base_name = filename[19:23] # four digit name
        dem = os.path.join(dem_directory, filename)
        dsm = dsm_directory + '/DSM' + filename[3:]
        with rasterio.open(dem) as src:
            data[base_name] = [(src.read()[0], src.transform)]
        with rasterio.open(dsm) as src:
            data[base_name].append((src.read()[0], src.transform))

for filename in os.listdir(aer_directory):
    if filename.endswith('.tif'):
        with rasterio.open(os.path.join(aer_directory, filename)) as src:
            aer_data = (src.read(), src.transform)

# string base_name from DEM-DSM, top-left point x and y in relative px within DEM-DSM image, side length in m
def overlap(base_name, x, y, side):
    dem_data, dsm_data = data[base_name]
    dem_image, dem_transform = dem_data
    dsm_image, dsm_transform = dsm_data
    aer_image, aer_transform = aer_data
    # window side len in px of dem-dsm image
    # side_px = int(side/dem_transform[0])
    
    # DEM-DSM image width and height
    wd = dem_image.shape[1]
    ht = dem_image.shape[0]
    # window cannot exceed DEM-DSM image boundary
    assert x >= 0
    assert y >= 0
    assert x+side <= wd
    assert y+side <= ht

    # earth real x y coord in m
    x_real = dem_transform.c+x
    y_real = dem_transform.f-y
    # top-left x and y in px of aerial image
    x_aer, y_aer = map(int, ~aer_transform * (x_real, y_real))
    # window side len in px of aerial image
    side_aer_px = int(side/aer_transform[0])
    # window cannot exceed aerial image boundary
    assert x_aer >= 0
    assert y_aer >= 0
    assert x_aer+side_aer_px <= aer_data[0].shape[2]
    assert y_aer+side_aer_px <= aer_data[0].shape[1]
    
    # ((x_start, x_end), (y_start, y_end))
    dem_dsm_window = ((x, x+side), (y, y+side))
    aer_window = ((x_aer, x_aer+side_aer_px), (y_aer, y_aer+side_aer_px))

    # Extract the windows from the images
    dem_crop = dem_image[dem_dsm_window[1][0]:dem_dsm_window[1][1], dem_dsm_window[0][0]:dem_dsm_window[0][1]]
    dsm_crop = dsm_image[dem_dsm_window[1][0]:dem_dsm_window[1][1], dem_dsm_window[0][0]:dem_dsm_window[0][1]]
    aer_crop = aer_data[0][:3, aer_window[1][0]:aer_window[1][1], aer_window[0][0]:aer_window[0][1]]

    return dem_crop, dsm_crop, aer_crop

def plot3(dem_crop, dsm_crop, aer_crop):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Plot DEM
    axs[0].imshow(dem_crop, cmap='viridis')
    axs[0].set_title(f'DEM - {base_name}')
    axs[0].axis('off')

    # Plot DSM
    axs[1].imshow(dsm_crop, cmap='viridis')
    axs[1].set_title(f'DSM - {base_name}')
    axs[1].axis('off')

    # Plot Aerial Image
    axs[2].imshow(aer_crop.transpose(1, 2, 0))  # Transpose to get (height, width, channels)
    axs[2].set_title(f'Aerial - {base_name}')
    axs[2].axis('off')

    plt.show()
