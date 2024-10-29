# -*- coding: utf-8 -*-
#
# SPDX-FileCopyrightText: 2024, M.Heinze <matthias.heinze@iof.fraunhofer.de>, C.Munkelt <christoph.munkelt@iof.fraunhofer.de>
#
# SPDX-License-Identifier: BSD-3-Clause
#
# Distributed under the BSD-3-Clause License. See LICENSE for more information.
#
import os
import copy
import json

import numpy as np

import recon

def recon_workflow():

    # load
    #
    working_directory = "."
    print(f"load disparity map from '{os.path.join(working_directory, 'disparity.npy')}'")
    disparity = np.load(os.path.join(working_directory, 'disparity.npy'))

    print(f"load q-matrix from '{os.path.join(working_directory, 'qmatrix.json')}'")
    with open(os.path.join(working_directory, 'qmatrix.json'), 'r') as f:
        data = json.load(f)
        qmatrix = np.array(data['qmatrix'])

    pointmap = recon.pointmap_reconstruction(disparity, qmatrix)

    x = pointmap[:,:,0]
    y = pointmap[:,:,1]
    z = pointmap[:,:,2]

    # plot
    #
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from mpl_toolkits.axes_grid1 import make_axes_locatable

    fig = plt.figure(figsize=(13.5, 9), dpi=80)

    ax_disp = fig.add_subplot(211)
    im_disp = ax_disp.imshow(disparity,
        vmin=np.nanpercentile(disparity, 5),
        vmax=np.nanpercentile(disparity, 95),
        cmap=cm.jet)

    ax_disp.set_title("disparity map")
    ax_disp.set_xlabel("$x$ (px)")
    ax_disp.set_ylabel("$y$ (px)")

    ax_pnt = fig.add_subplot(212, projection='3d')
    im_pnt = ax_pnt.plot_surface(x, y, z, 
        rstride=4, cstride=4, linewidth=0, antialiased=False, shade=False,
        cmap=cm.Blues)

    ax_pnt.set_zlim(
        np.nanpercentile(z, 1) - np.nanpercentile(z, 1)*0.1,
        np.nanpercentile(z, 99) + np.nanpercentile(z, 99)*0.1)

    ax_pnt.set_title("3d point map")
    ax_pnt.set_xlabel("$x$ (m)")
    ax_pnt.set_ylabel("$y$ (m)")
    ax_pnt.set_zlabel("$z$ (m)", rotation=0)
    ax_pnt.zaxis.set_rotate_label(False)

    fig.colorbar(im_disp,
        cax=make_axes_locatable(ax_disp).append_axes("right", size="5%", pad=0.1),
        label="disparity (px)")

    plt.subplots_adjust(left=0.07, bottom=0.1, right=0.93, top=0.95, wspace=0.35)
    plt.show()


if __name__ == '__main__':

    print("np.__version__ {}", np.__version__)
    recon_workflow()
