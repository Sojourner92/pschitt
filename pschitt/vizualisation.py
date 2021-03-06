# Licensed under a 3-clause BSD style license - see LICENSE.rst

import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
from scipy import stats


def plot_shower3d(shower, alltel, **options):
    """
    Display the sky object (shower) and the telescope in a 3D representation
    Parameters
    ----------
    shower: array of points (arrays [x,y,z])
    alltel: array of telescopes (telescope class)
    options:
        - density_color = True: use density for particles color. False by default.
        - display = True: show the plot. False by default
        - outfile = "file.eps" : save the plot as `file.eps`. False by default.
    """
    if options.get("figsize"):
        figsize = options.get("figsize")
    else:
        figsize=(12,12)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    for tel in alltel:
        p = plt.Circle((tel.mirror_center[0],tel.mirror_center[1]), 30, color='black')
        ax.add_patch(p)
        art3d.pathpatch_2d_to_3d(p, z=tel.mirror_center[2], zdir='z')

    ip = plt.Circle((shower.impact_point[0], shower.impact_point[1]), 15, color='red')
    ax.add_patch(ip)
    art3d.pathpatch_2d_to_3d(ip, z=tel.mirror_center[2], zdir='z')

    values = shower.particles.T

    if options.get("density_color") == True:
        kde = stats.gaussian_kde(values)
        density = kde(values)
        ax.scatter(values[0] , values[1], values[2], marker='o', c=density)
    else:
        ax.scatter(values[0] , values[1], values[2], marker='o')

    plt.axis([-1000, 1000, -1000, 1000])
    ax.set_xlabel("[m]")
    ax.set_zlabel("altitude [m]")
    if options.get("display") == True:
        plt.show()
    if options.get("outfile"):
        outfile = options.get("outfile")
        assert isinstance(outfile, str), "The given outfile option should be a string"
        plt.savefig(outfile + '.eps', format='eps', dpi=200)


def display_camera_image(telescope, figsize=(8,8)):
    """
    display an image of the camera of the telescope
    Parameters
    ----------
    telescope : telescope class
    histogram : histogram of the signal in each pixel
    """
    plt.figure(figsize=figsize)
    plt.scatter(telescope.pixel_tab[:, 0], telescope.pixel_tab[:, 1], c=telescope.signal_hist, s=27)
    plt.axis('equal')
    plt.colorbar(label='counts')
    plt.show()


def display_stacked_cameras(telescope_array):
    """
    Display stacked camera images. This only works if all the telescope camera are the same type.
    Parameters
    ----------
    telescope_array: list of telescopes classes
    """
    tel0 = telescope_array[0]
    l0 = len(tel0.signal_hist)
    assert np.all([len(tel.signal_hist) == l0 for tel in telescope_array])
    stacked_hist = np.zeros(l0)
    for tel in telescope_array:
        stacked_hist += tel.signal_hist

    plt.scatter(tel0.pixel_tab[:, 0], tel0.pixel_tab[:, 1], c=stacked_hist)
    plt.axis('equal')
    plt.colorbar(label='counts')


def display_pointing_tel(tel, show=True):
    """
    Display the pointing direction of a telescope as seen from above
    Parameters
    ----------
    tel: telescope class
    show: Boolean, to display or not
    """
    ax = plt.axes()
    ax.arrow(tel.camera_center[0], tel.camera_center[1], tel.normal[0], tel.normal[1], head_width=5, head_length=10, fc='k', ec='k')
    #plt.xlim([np.min([start[0], end[0]]), np.max([start[0], end[0]])])
    #plt.ylim([np.min([start[1], end[1]]), np.max([start[1], end[1]])])
    if show:
        plt.show()


def display_pointing_array(alltel):
    """
    Display the pointing direction of each telescope in the array as seen from above

    Parameters
    ----------
    alltel: list of telescope classes
    """
    centers = np.array([tel.mirror_center for tel in alltel])
    xmin = centers[:,0].min() - 50
    xmax = centers[:,0].max() + 50
    ymin = centers[:,1].min() - 50
    ymax = centers[:,1].max() + 50

    for tel in alltel:
        display_pointing_tel(tel, show=False)

    plt.axis('equal')
    plt.axis([xmin, xmax, ymin, ymax])
    plt.show()


def plot_array(telescope_array):
    """
    Plot a map of the telescopes array
    Parameters
    ----------
    telescope_array: list of telescopes classes
    """
    for tel in telescope_array:
        plt.scatter(tel.mirror_center[0], tel.mirror_center[1])
        plt.annotate(str(tel.id), (tel.mirror_center[0] + 20, tel.mirror_center[1] + 20))
    plt.axis('equal')
    plt.legend()
    plt.xlabel("x [m]")
    plt.ylabel("y [m]")
