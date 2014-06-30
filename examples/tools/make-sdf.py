#! /usr/bin/env python

import os
import numpy as np
from PIL import Image
from sdf import compute_sdf
from scipy.ndimage.interpolation import zoom

def GenerateDistanceField(infile, outfile):

    image = Image.open(infile)
    image.load()
    channels = image.split()
    if len(channels) == 4:
        Z = (np.asarray(channels[3]) / 255.0).astype(np.double)
    else:
        Z = (np.asarray(channels[0]) / 255.0).astype(np.double)
    compute_sdf(Z)

    # Save as PNG image
    #I = (Z*256).astype(np.ubyte)
    #image = Image.fromarray(I)
    #image.save("%s.png" % outfile)

    # Save as NUMPY array
    # Z -= 0.5

    Z = zoom(Z, 128/1024.)
    np.save("%s.npy" % outfile, Z.astype(np.float32))


if __name__ == "__main__":

    import sys
    if len(sys.argv) < 2:
        print("Usage: make-sdf.py image")
    else:
        filename = os.path.basename(sys.argv[1])
        basename = filename.split('.')[0]
        extension = filename.split('.')[1]
        infile = basename + '.' + extension
        outfile = basename + '-sdf'
        print "Generating SDF for %s" % infile
        GenerateDistanceField(infile, outfile)
