import os
os.environ['PROJ_LIB'] = 'wkt_venv\Lib\site-packages\osgeo\data\proj'
os.environ['GDAL_DATA'] = 'wkt_venv\Lib\site-packages\osgeo\data'

from osgeo import gdal

# set input and output file names
input_filename = "GMv22.1_DEM.tif"
output_filename = "GMv22.1_DEM_edit.tif"

# open the input file as a dataset
r = gdal.Open(input_filename)

# create a copy of the input dataset
driver = gdal.GetDriverByName('Gtiff')
dataset = driver.CreateCopy( output_filename, r, 0 )

# extract the crs info as wkt
wkt = gdal.Info(r, format='wkt')

# remove unwanted data from wkt
top_wkt = wkt.split("BOUNDCRS[")[0]
proj_wkt = wkt.split("SOURCECRS[\n")[1].split(",\n    TARGETCRS[")[0].replace('  ','').replace('\n',' ')
bottom_wkt = "Data axis to CRS axis mapping: 1,2" + wkt.split("Data axis to CRS axis mapping: 1,2")[1]
new_wkt = top_wkt + proj_wkt + '\n' + bottom_wkt

# set the projection of the output dataset and close it
dataset.SetProjection(new_wkt)
dataset = None