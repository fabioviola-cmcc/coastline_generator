#!/usr/bin/python

# requirements
import pdb
import sys
import getopt
import shapefile
import traceback
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# application name
APPNAME = "gen_coastline"


# help function
def showHelp():
    pass


# main
if __name__ == "__main__":

    # init params
    linesFilename = None
    polyFilename = None
    outFilename = None
    pngFilename = None
    
    # read params
    try:
        options, rem = getopt.getopt(sys.argv[1:], 'hl:p:o:', ['linesFile=', 'help', 'polyFile=', 'outFile=', 'pngFile='])
    
        for opt, arg in options:
            if opt in ('-l', '--linesFile'):
                linesFilename = arg
            elif opt in ('-p', '--polyFile'):                
                polyFilename = arg
            elif opt in ('-o', '--outFile'):                
                outFilename = arg
            elif opt in ('--pngFile'):
                pngFilename = arg
            elif opt in ('-h', '--help'):
                showHelp(logger)
                sys.exit(0)
    
    except getopt.GetoptError:
        showHelp(logger)
        sys.exit(1)

    if not(linesFilename) and not(polyFilename) and not(outFilename):
        showHelp(logger)
        sys.exit(1)
        
    # opening output file
    try:
        outFile = open(outFilename, "w")
    except:
        print(traceback.print_exc())
        print("[%s] -- Error while opening output file" % APPNAME)
        
    # open the two shapefiles
    try:
        s_lines = shapefile.Reader(linesFilename)
        s_poly = shapefile.Reader(polyFilename)
    except:
        print("[%s] -- Error while opening shape files" % APPNAME)

    # initialise a map
    if pngFilename:
        m = Basemap(llcrnrlon=57, llcrnrlat=-21,
                    urcrnrlon=58,urcrnrlat=-19.5,
                    rsphere=(6378137.00,6356752.3142),        
                    resolution='f',projection='merc',                
                    lat_0=-20.25, lon_0=57.5, epsg=4326)
        plt.figure(figsize=(7, 7))
        
    # write the total number of polygons
    sumpoly = 0
    for f in [s_lines, s_poly]:
        shapes = f.shapes()
        records = f.records()
        for record, shape in zip(records,shapes):            
            if record[1] in ['beach', 'cliff', 'reef', 'coastline', 'sand', 'bare_rock']:
                sumpoly = sumpoly + 1
    outFile.write("%s\n" % sumpoly)
    
    # process both the files
    for f in [s_lines, s_poly]:

        # debug print
        print("[%s] -- Processing file %s" % (APPNAME, f))
        
        # read shapes
        print("[%s] -- Reading shapes" % APPNAME)
        shapes = f.shapes()

        # read records
        print("[%s] -- Reading records" % APPNAME)
        records = f.records()

        # iterate over records and shapes -- TODO: optimize this code!
        print("[%s] -- Iterating over records and shapes" % APPNAME)
        for record, shape in zip(records,shapes):

            if record[1] in ['beach', 'cliff', 'reef', 'coastline', 'sand', 'bare_rock']:
            
                # write info of the polygon
                outFile.write("%s 0\n" % len(shape.points))
                
                # iterate over coordinates
                for p in (shape.points):
                    outFile.write("%s %s\n" % (p[0], p[1]))

                    # plot on map
                    if pngFilename:
                        ppx, ppy = m(p[0],p[1])
                        m.plot(ppx, ppy, 'k+', markersize=1)

# plot
if pngFilename:
    
    # draw coastline
    m.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1200)
    m.drawcoastlines(color='r', linewidth=0.2)
    
    # save png
    plt.savefig(pngFilename)
                
# close file
print("[%s] -- Closing output file" % APPNAME)
outFile.close()

# exit gracefully
print("[%s] -- Bye!" % APPNAME)
