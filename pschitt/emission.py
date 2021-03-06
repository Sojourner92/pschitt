# Licensed under a 3-clause BSD style license - see LICENSE.rst

from . import geometry as geo
import numpy as np


def transmission(distances):
    """
    Compute the transmission coefficient between 0 and 1 taking into accounts all radiative transfer effects
    1 corresponds to a complete transmission (no absorption)
    Parameters
    ----------
    distances: numpy array of atmospheric length to go through

    Returns
    -------
    numpy array of floats between 0 and 1 for all distances
    """
    return np.ones(len(distances))


def emission_profile(dist):
    """
    Dummy function to select one emission profile
    Parameters
    ----------
    dist: float, distance to the impact parameter

    Returns
    -------
    float between 0 and 1
    """
    return constant_profile(dist)
    # return ground_profile_1(dist, shift=250)



def constant_profile(dist):
    """
    Given a distance to the impact point, give the probability to detect the shower
    Dummy function where the probability is always one

    Parameters
    ----------
    dist: float, distance to the impact point

    Returns
    -------
    float between 0 and 1
    """
    return 1


def power_law_profile(dist, alpha=2):
    """
    Given a distance to the impact point, give the probability to detect the shower
    Power-law decrease from impact point. By default the power index alpha = 2

    Parameters
    ----------
    dist: float, distance to the impact point

    Returns
    -------
    float between 0 and 1
    """
    return 1./(1. + dist)**2


def ground_profile_heaviside(dist, shift=120):
    """
    Given a distance to the impact point, give the probability to detect the shower
    Simple emission profile constant below 120m then with an decrease

    Parameters
    ----------
    dist: float, distance to the impact point

    Returns
    -------
    float between 0 and 1
    """
    return (dist<=shift) * 1. + (dist>shift) * 0.


def ground_profile_1(dist, shift=120):
    """
    Given a distance to the impact point, give the probability to detect the shower
    Simple emission profile constant below 120m then with an decrease

    Parameters
    ----------
    dist: float, distance to the impact point

    Returns
    -------
    float between 0 and 1
    """
    return (dist<=shift) * 1. + (dist>shift) * 1./(dist - shift)


def angular_profile_heaviside(angles, limit):
    """
    Emission profile depending on the angle from particle axis.
    The emission profile is 1 below the limit angle and 0 above.
    Parameters
    ----------
    angle: numpy array - angles to the particle axis

    Returns
    -------
    numpy array with same shape as angles giving the emission probabilities
    """
    return 1 * (angles <= limit)


def angular_profile_exp_falloff(angles, break_angle, alpha):
    """
    Profile equals to one until the break_angle then exponential decrease with coef -alpha

    Parameters
    ----------
    angles: numpy array
    break_angle: float
    alpha: float

    Returns
    -------
    numpy array with same shape as angles
    """
    return 1 * (angles < break_angle) + np.exp(-alpha*(angles - break_angle)) * (angles >= break_angle)


def mask_transmitted_particles(tel, shower, angular_profile, *args):
    """
    Compute a masking array for the photons from the shower to know if they reach the telescope
    depending on their transmission probability.
    It takes into account the position of the telescope and shower direction and impact parameter.

    Parameters
    ----------
    tel: telescope class
    shower: shower class
    angular_profile: function to use for the angular_profile of the Cherenkov emission
    *args: arguements of the function angular_profile

    Returns
    -------
    numpy array of booleans of length = len(shower.particles)
    """
    # Compute the air transmission coefficient for each particle:
    particle_distances = geo.distance_shower_camera_center(shower, tel)
    transmissions = transmission(particle_distances)

    # Compute the transmission profile relative to Cherenkov cone for each particle:
    shower_direction = geo.altaz_to_normal(shower.alt, shower.az)
    angles = np.array([geo.angle(shower_direction, particle - tel.mirror_center) for particle in shower.particles])

    # The resulting transmission probability is the product of both:
    p_trans = transmissions * angular_profile(angles, *args)

    mask_transmitted_particles = p_trans > np.random.rand(len(shower.particles))

    return mask_transmitted_particles

