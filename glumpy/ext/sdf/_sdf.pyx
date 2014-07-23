# import both numpy and the Cython declarations for numpy
import numpy as np
cimport numpy as np

# if you want to use the Numpy-C-API from Cython
# (not strictly necessary for this example)
np.import_array()

# cdefine the signature of our c function
cdef extern from "sdf.h":
    void _compute_sdf(double *data,
                      unsigned int width, unsigned int height)

# create the wrapper code, with numpy type annotations
def compute_sdf(np.ndarray[double, ndim=2, mode="c"] in_array not None):
    """Compute the signed distance field"""
    _compute_sdf(<double*> np.PyArray_DATA(in_array),
                  in_array.shape[1], in_array.shape[0])
