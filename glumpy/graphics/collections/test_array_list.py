# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import unittest
import numpy as np
from . array_list import ArrayList


class ArrayListDefault(unittest.TestCase):

    def test_init(self):
        L = ArrayList()
        assert L.dtype == float
        assert len(L) == 0

    def test_init_from_list(self):
        L = ArrayList([[0], [1, 2], [3, 4, 5]])
        assert L.dtype == int
        assert len(L) == 3

    def test_init_exception(self):
        self.assertRaises(ValueError, ArrayList, [0, 1, 2, 3, 4], 3)
        self.assertRaises(ValueError, ArrayList, [0, 1, 2, 3, 4], [1, 2, 3])

    def test_datasize(self):
        L = ArrayList([0, 1, 2, 3, 4, 5], [1, 2, 3])
        assert L.size == 6

    def test_itemsize(self):
        L = ArrayList([0, 1, 2, 3, 4, 5], [1, 2, 3])
        assert np.allclose(L.itemsize, [1, 2, 3])

    def test_append_1(self):
        L = ArrayList()
        L.append(1)
        assert L[0] == 1

    def test_append_2(self):
        L = ArrayList()
        L.append(np.arange(10), 2)
        assert len(L) == 5
        assert np.allclose(L[4], [8, 9])

    def test_append_3(self):
        L = ArrayList()
        L.append(np.arange(10), 1 + np.arange(4))
        assert len(L) == 4
        assert np.allclose(L[3], [6, 7, 8, 9])

    def test_insert_1(self):
        L = ArrayList()
        L.append(1)
        L.insert(0, 2)
        assert len(L) == 2
        assert L[0] == 2

    def test_insert_2(self):
        L = ArrayList()
        L.append(1)
        L.insert(0, np.arange(10), 2)
        assert len(L) == 6
        assert np.allclose(L[4], [8, 9])

    def test_insert_3(self):
        L = ArrayList()
        L.append(1)
        L.insert(0, np.arange(10), 1 + np.arange(4))
        assert len(L) == 5
        assert np.allclose(L[3], [6, 7, 8, 9])

    def test_insert_4(self):
        L = ArrayList()
        L.append(1)
        L.insert(-1, np.arange(10), 1 + np.arange(4))
        assert len(L) == 5
        assert np.allclose(L[3], [6, 7, 8, 9])

    def test_insert_1(self):
        L = ArrayList()
        L.append(0)
        L.append([[1,2],[3,4,5]])
        assert len(L) == 3
        assert np.allclose(L[1], [1,2])

    # Test representation of the list
    # -------------------------------
    def test_str(self):
        L = ArrayList([[0], [1, 2], [3, 4, 5], [6, 7, 8, 9]])
        assert str(L) == '[ [0] [1 2] [3 4 5] [6 7 8 9] ]'

    # Get item using negative index
    # -----------------------------
    def test_getitem_negative(self):
        L = ArrayList(np.arange(10), 1)
        assert L[-1] == 9

    # Get item range using reversed range
    # -----------------------------------
    def test_getitem_reverse(self):
        L = ArrayList(np.arange(10), 1)
        assert np.allclose(L[-1:-2], [8])

    # Get empty range
    # ---------------
    def test_getitem_empty(self):
        L = ArrayList(np.arange(10), 1)
        assert np.allclose(L[1:1], [])

    # Get out of range item
    # ---------------------
    def test_getitem_exception(self):
        L = ArrayList(np.arange(10), 1)
        self.assertRaises(IndexError, L.__getitem__, -11)
        self.assertRaises(TypeError, L.__getitem__, ())

    # Get all items using ellipsis
    # ----------------------------
    def test_getitem_ellipsis(self):
        L = ArrayList(np.arange(10), 1)
        assert np.allclose(L[...], np.arange(10))

    # Get item range using key
    # -------------------------------
    def test_getitem_key(self):
        dtype = [("x", float, 1), ("y", float, 1)]
        data = np.zeros(3, dtype=dtype)
        data["x"] = 1
        data["y"] = 2
        L = ArrayList(data, itemsize=1)
        assert np.allclose(L["x"], [1, 1, 1])

    # Set all items using ellipsis
    # ----------------------------
    def test_setitem_ellipsis(self):
        L = ArrayList(np.arange(10), 1)
        L[...] = 0
        assert np.allclose(L.data, np.zeros(10))

    # Set a single item
    # ------------------
    def test_setitem(self):
        L = ArrayList(np.arange(10), 1)
        L[0] = 3
        assert L[0] == 3

    # Set a single item using negative index
    # --------------------------------------
    def test_setitem_negative(self):
        L = ArrayList(np.arange(10), 1)
        L[-1] = 0
        assert L[9] == 0

    # Set out of range item
    # ---------------------
    def test_setitem_exception(self):
        L = ArrayList(np.arange(10), 1)
        self.assertRaises(IndexError, L.__setitem__, -11, 0)
        self.assertRaises(TypeError, L.__setitem__, (), 0)

    # Set item range
    # --------------
    def test_setitem_range(self):
        L = ArrayList(np.arange(10), 2)
        L[:2] = [1, 2, 3, 4]
        assert np.allclose(L[0], [1, 2])
        assert np.allclose(L[1], [3, 4])

    # Set item range using reversed range
    # -----------------------------------
    def test_setitem_reversed_range(self):
        L = ArrayList(np.arange(10), 2)
        L[2:0] = [11, 12, 13, 14]
        assert np.allclose(L[0], [11, 12])
        assert np.allclose(L[1], [13, 14])

    # Set item range using null range
    # -------------------------------
    def test_setitem_empty_range(self):
        L = ArrayList(np.arange(10), 2)
        L[0:0] = []
        assert np.allclose(L.data, np.arange(10))

    # Set item range using key
    # -------------------------------
    def test_setitem_key(self):
        dtype = [("x", float, 1), ("y", float, 1)]
        data = np.zeros(3, dtype=dtype)
        data["x"] = 1
        data["y"] = 2
        L = ArrayList(data, itemsize=1)
        assert L[0]["x"] == 1
        assert L[0]["y"] == 2

    # Delete one item
    # ---------------
    def test_delitem_single_item(self):
        L = ArrayList([[1], [1, 2, 3], [4, 5]])
        del L[0]
        assert np.allclose(L[0], [1, 2, 3])
        assert np.allclose(L[1], [4, 5])

    # Delete last item
    # ----------------
    def test_delitem_last_item(self):
        L = ArrayList([[1], [1, 2, 3], [4, 5]])
        del L[-1]
        assert np.allclose(L[0], [1])
        assert np.allclose(L[1], [1, 2, 3])
        assert np.allclose(L[-1], [1, 2, 3])

    # Delete many items
    # -----------------
    def test_delitem_many_items(self):
        L = ArrayList()
        L.append(np.arange(10), 1)
        del L[1:]
        assert len(L) == 1
        assert np.allclose(L[0], 0)

    # Delete all items
    # -----------------
    def test_delitem_all_items(self):
        L = ArrayList()
        L.append(np.arange(10), 1)
        del L[:]
        assert len(L) == 0

    # Delete all items
    # -----------------
    def test_delitem_all_items_2(self):
        L = ArrayList()
        L.append(np.arange(10), 1)
        del L[...]
        assert len(L) == 0

    # Delitem exception
    # ---------------------
    def test_detitem_exception(self):
        L = ArrayList(np.arange(10), 1)
        self.assertRaises(TypeError, L.__delitem__, ())

    # Sizeable property
    # -----------------
    def test_sizeable(self):
        L = ArrayList(sizeable=False)
        self.assertRaises(AttributeError, L.__delitem__, 0)
        self.assertRaises(AttributeError, L.insert, 0, 0)

    # Writeable property
    # ------------------
    def test_writeable(self):
        L = ArrayList([1, 2, 3], writeable=False)
        self.assertRaises(AttributeError, L.__setitem__, 0, 0)

    # Data property
    # -------------
    def test_data(self):
        data = np.empty(10)
        L = ArrayList(data)
        assert np.allclose(L.data, data)


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    unittest.main()
