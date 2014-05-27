# Author: Igo Brilhante
# Generate full random trajectories from:
#   Number of users
#   Max number of trajectories per users
#   Max size of the trajectories

__author__ = 'igobrilhante'

import distribution_utils as dist
import db_utils as db
import random
import math
import numpy as np
import datetime
import time
import queries


trajectories_per_user_distribution_f = ""
trajectory_size_distribution_f = ""
trajectory_extent_distribution_f = ""

# number of users
n_users = 10

R_EARTH = 6371000

TABLE_SCHEMA = "fullrandtraj."

TIME_DELTA = datetime.timedelta(minutes=45)

# distance from place to place
DISTANCE = [0, 30]


def meters2degree(meters):
    return meters * (180 / math.pi / R_EARTH)


def degree2meters(degree):
    return degree / (180 / math.pi / R_EARTH)


# Get a next place from a given place w.r.t. an extent
def get_next_place(_place_list):
    r_ = random.randint(0, len(_place_list) - 1)

    return _place_list[r_]


# Get close places to a given place
def get_close_places(given_place, place_list):
    res = [given_place]
    # for place in place_list:
    #     if place != given_place:
    #         d = compute_distance(place, given_place)
    #         if d <= random.randint(DISTANCE[0], DISTANCE[1]):
    #             res.append(place)

    return res


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


# Compute the extent of the trajectory
def compute_extent(_trajectory):
    ext = 0.0

    for j in range(1, len(_trajectory)):
        i = j - 1
        ext += compute_distance(_trajectory[i][0][0], _trajectory[j][0][0])

    return ext


def generate_random_trajectories(city, dow, hours):

    print city, dow, hours

    trajectory_result = dict()

    place_list = db.query_places(city, dow, hours)

    ################################## QUERIES ##################################

    tsd = queries.create_tsd(city, dow, hours)

    tpu = queries.create_tpu(city, dow, hours)

    ################################## END QUERIES ##################################

    # LOAD DATA
    # Compute the distributions
    n_users = db.get_number_of_users(city, dow, hours)
    n_trajectories = db.get_number_of_trajectories(city, dow, hours)
    max_trajectories_per_user = np.max(db.query(tpu)['key'])
    max_trajectory_size = np.max(db.query(tsd)['key'])

    tsd = queries.create_tsd(city, dow, hours)
    tpu = queries.create_tpu(city, dow, hours)

    trajectories_per_user_distribution = dist.compute_probability_distribution(db.query(tpu))

    trajectory_size_distribution = dist.compute_probability_distribution(db.query(tsd))

    print n_users

    n_trajs_total = 0

    u = 0

    while u < n_users and n_trajs_total < n_trajectories:
        # number of trajectories
        print "%s/%s and %s/%s" % (u, n_users, n_trajs_total, n_trajectories)
        user_trajectories = dist.random_from_probability(trajectories_per_user_distribution)

        # print 'User '+str(u) + ' with ' + str(n_trajectories)

        trajectories_count = 0

        today = datetime.datetime.fromtimestamp(time.time())

        trajectory_result[u] = []

        # create n trajectories
        while trajectories_count < user_trajectories and n_trajs_total < n_trajectories:

            # number of points
            n_points = dist.random_from_probability(trajectory_size_distribution)
            print "Traj Size ", n_points

            places_count = 0

            traj = []

            # pick n_points places
            while places_count < n_points:

                tomorrow = today + TIME_DELTA

                place = get_next_place(place_list)

                places = get_close_places(place, place_list)

                traj.append((places, today, tomorrow))

                places_count += 1

                # go forward in time
                today = tomorrow + TIME_DELTA

            trajectories_count += 1
            n_trajs_total += 1

            trajectory_result[u].append(traj)

        # user increment
        u += 1

    print "Total trajectories: %s(%s) " % (str(n_trajs_total), n_trajectories)

    table = TABLE_SCHEMA+city+"_"+str(hours)+"h_"+dow

    db.store_trajectories(trajectory_result, table)











