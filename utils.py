__author__ = 'igobrilhante'


import math
import numpy as np
import matplotlib.mlab as mpl

R_EARTH = 6371000


def meters2degree(meters):
    return meters * (180 / math.pi / R_EARTH)


def degree2meters(degree):
    return degree / (180 / math.pi / R_EARTH)


# Compute the distance between two places
# return the distance in meters
def compute_distance(_place_1, _place_2):
    d_lat = math.radians(_place_2[1]-_place_1[1])
    dlong = math.radians(_place_2[2]-_place_1[2])

    lat1 = math.radians(_place_1[1])
    lat2 = math.radians(_place_2[1])

    a = math.sin(d_lat/2) * math.sin(d_lat/2) + \
        math.sin(dlong/2) * math.sin(dlong/2) * math.cos(lat1) * math.cos(lat2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R_EARTH * c


def agg_degree(array):
    stats = (
        ('degree', len, 'total'),
    )

    return mpl.rec_groupby(array, ('degree',), stats)


def agg_compactness(array):
    stats = (
        ('traj_compactness', len, 'total'),
    )

    return mpl.rec_groupby(array, ('traj_compactness',), stats)