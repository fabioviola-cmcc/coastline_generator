# Coastline generator

This tool allows users to generate coastline files for Medslik, using OpenStreetMap shapefiles as input.

## Mandatory input parameters

* `--linesFile=`: the name of the lines shape file
* `--polyFile=`: the name of the polygon shape file
* `--outFile=`: the name of the output coastline file (e.g. medf.map)

## Optional input parameters

* `--pngFile=`: the name of the optional png file to plot the coastline
* `--latInterval=`: min and max latitudes, separated by a comma (needed only if --pngFile is specified)
* `--lonInterval=`: min and max longitudes, separated by a comma (needed only if --pngFile is specified)
* `--addPoint=`: comma-separated longitude and latitude for an additional point to plot (needed only if --pngFile is specified)

## Example

```python
$ python gen_coastline.py --linesFile=lines.shp --polyFile=polygons.shp  --outFile=medf.map --pngFile=coastline_image.png --latInterval=-21,-19 --lonInterval=56,58
```