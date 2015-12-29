# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import unittest
import numpy as np
from . collection import BaseCollection

vtype = [('position', 'f4', 2)]
utype = [('color',    'f4', 3)]
itype = np.uint32

vertices = np.zeros(4, dtype=vtype)
indices  = np.array([0,1,2,0,2,3], dtype=itype)
uniforms = np.ones(1,dtype=utype)


class BaseCollectionDefault(unittest.TestCase):


    def test_init(self):
        C = BaseCollection(vtype,utype)
        assert len(C) == 0

    def test_append_one_item(self):
        C = BaseCollection(vtype, utype, itype)
        C.append(vertices, uniforms, indices)
        C.append(vertices, uniforms, indices)
        assert np.allclose( C[0].indices , indices )
        assert np.allclose( C[1].indices , 4+indices )

    def test_append_several_item_1(self):
        C = BaseCollection(vtype, utype, itype)
        C.append(np.zeros(40,dtype=vtype), uniforms, indices, itemsize=4)
        assert len(C) == 10
        for i in xrange(10):
            assert np.allclose(C[i].indices, 4*i+indices)

    def test_append_several_item_2(self):
        C = BaseCollection(vtype, utype)
        C.append(np.zeros(40, dtype=vtype),
                 np.zeros(10, dtype=itype), itemsize=(4,1))
        for i in xrange(10):
            assert np.allclose(C[i].indices, 4*i)

    def test_delete_one_item(self):
        C = BaseCollection(vtype, utype)
        C.append(vertices, indices, uniforms)
        C.append(vertices, indices, uniforms)
        del C[0]
        assert np.allclose(C[0].indices , indices)

    def test_delete_several_item(self):
        C = BaseCollection(vtype, utype)
        C.append(np.zeros(40, dtype=vtype), indices, uniforms, itemsize=4)
        del C[:9]
        assert np.allclose(C[0].indices , indices)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()
