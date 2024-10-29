# -*- coding: utf-8 -*-
#
# SPDX-FileCopyrightText: 2024, M.Heinze <matthias.heinze@iof.fraunhofer.de>, C.Munkelt <christoph.munkelt@iof.fraunhofer.de>
#
# SPDX-License-Identifier: BSD-3-Clause
#
# Distributed under the BSD-3-Clause License. See LICENSE for more information.
#
import os
import time

import numpy as np

def pointmap_reconstruction(disparity, qmatrix):

    numrows, numcols = disparity.shape

    y,x = np.mgrid[:numrows, :numcols]

    a = np.concatenate((x.flatten()[:,np.newaxis], y.flatten()[:,np.newaxis], 
        disparity.flatten()[:,np.newaxis], np.ones(numrows*numcols)[:,np.newaxis]), axis=1)

    b = np.dot(a, qmatrix.T).astype(np.float32)

    pointmap = b[:,:3] / b[:,3, np.newaxis]
    pointmap.shape = numrows, numcols, 3

    return pointmap

if __name__ == '__main__':

    print("np.__version__ {}", np.__version__)
