https://www.planet.com
sentinel 2

lidar: DSM-DEM 20cm 
why use lidar? height of mangrove or if mangrove present

year match

field site to start with

coordinate ref sys
nzgd2000 height


9th August
The linz elevation files are provided as geospatial files.

The geospatial files are provided as tiles (If you look on Linz, you can see where the tiles are), so you need to know which tile is the right one for the area that you are interested in.


These files that can be read by geospatial software like ARCGIS or QGIS. Most software packages have scripts that enable you to read this very standard format. Python will have a toolbox that you can use to read these file. If stuck, ask Zhanchao, but try and find it yourself

-need to be able to load the file, and find the pixels that are within the area that you are interested in.

Load the right tile in, and then plot it....

Do the same thing with the area photograph.

Then learn about the format the the ML tools need and convert to this format. You might need to interpolate so that the two data sources are on the same coordinate system

write a paragraph what researchers already are using for mangrove classification

gdal cv2
