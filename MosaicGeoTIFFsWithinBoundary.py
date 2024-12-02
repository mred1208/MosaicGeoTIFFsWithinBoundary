#####################################################################################
# Merielle Redwine 9/25/24
# Hurricane City GIS Analyst I
# 
# This script takes in a folder containing raster GeoTIFF tiles, checks if they 
# overlap with a polygon shapefile, creates an empty raster in a file geodatabase,
# and then mosaics the input raster tiles to the empty raster.
######################################################################################
import arcpy
import os
# tile folder location
arcpy.env.workspace = arcpy.GetParameter(0)
# polygon shapefile for boundaries
clip_extent = arcpy.GetParameter(1)
# new raster geodatabase
out_raster_path = arcpy.GetParameter(2)
# new raster name
out_raster = arcpy.GetParameter(3)
# spatial reference
projection = arcpy.GetParameter(4)
# number of bands 
num_bands = arcpy.GetParameter(5)
# creates a path for the new raster by combining geodb and raster name
target = os.path.join(str(out_raster_path), out_raster)
arcpy.AddMessage(target)
# Creates a new blank raster with user input
arcpy.management.CreateRasterDataset(
    out_raster_path, out_raster, number_of_bands=num_bands, raster_spatial_reference=projection)
arcpy.AddMessage('raster dataset created')
inputs = [] # empty array for raster tiles from input folder
# lists rasters from folder of tiles because it was set to current workspace
rasters = arcpy.ListRasters("*")  
# loops through rasters and checks if they overlap with polygon boundary
for raster in rasters:
    in_raster = arcpy.env.workspace + '\\' + raster # tile path
    arcpy.env.extent = clip_extent # extent of the polygon boundary
    raster_obj = arcpy.sa.Raster(in_raster) # turns raster into raster object
    raster_extent = raster_obj.extent # extent object of raster object
    clip_extent_obj = arcpy.Describe(clip_extent).extent # extent object for polygon
    # Checks if polygon and input raster overlap and adds to list of rasters if so
    if raster_extent.overlaps(clip_extent_obj) or not raster_extent.disjoint(clip_extent_obj):
        arcpy.AddMessage('raster was within the municipal boundaries')
        inputs.append(raster)         
    else:
        arcpy.AddMessage('outside of Hurricane')
arcpy.AddMessage(inputs)
# mosaic list of rasters and writes to output raster    
arcpy.management.Mosaic(inputs, target)
