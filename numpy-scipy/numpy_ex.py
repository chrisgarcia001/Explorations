# Numpy: https://docs.scipy.org/doc/numpy-dev/user/quickstart.html#indexing-slicing-and-iterating

import numpy as np
a = np.arange(15).reshape(3, 5)
a
a.shape
a.ndim
a.dtype.name
a.itemsize
a.size
a[1] # get row 1
a[:, 2] # get column 2
type(a)
b = np.array([6, 7, 8])
b
type(b)