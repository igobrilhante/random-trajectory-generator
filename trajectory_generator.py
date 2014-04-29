# Author: Igo Brilhante
# Generate random trajectories from given distribution:
#   Number of users
#   Distribution of trajectories per user
#   Distribution of size of trajectories
#   Distribution of extent of trajectories

__author__ = 'igobrilhante'

import distribution_utils as dist
import db_utils as db
import random
import math
import numpy as np
import datetime
import time
import queries


R_EARTH = 6371000

MAX_ITER = 10
MAX_TRAJS = 100


TIME_DELTA = datetime.timedelta(minutes=45)


# Get a next place from a given place w.r.t. an extent
def get_next_place(_extent, _place_list, _from_place, prob_come_back):
    r_ = random.randint(0, len(_place_list) - 1)

    # select the first place
    if _from_place is None:
        return _place_list[r_]
    # otherwise select the next one from a given place _from_place
    else:

        # try selecting places within the _extent
        allowed_list = filter_close_places(_from_place, _extent, _place_list)
        l = np.max([len(allowed_list) - 1, 1])

        if len(allowed_list) > 1:
            r = random.randint(0, l)
            return allowed_list[r]
        else:
            # probabilidade de voltar para o mesmo ponto
            f = random.random()
            if f < prob_come_back:
                return _from_place
            else:
                return get_nn(_from_place, _place_list)


# filter out places that are reacheable from a given one
def filter_close_places(_from_place, _extent, _place_list):
    allowed_list = []
    for p in _place_list:
        d = compute_distance(p, _from_place)
        if d <= _extent:
            allowed_list.append(p)
    return allowed_list


# nearest neighbor query
def get_nn(given_place, place_list):
    min_dist = float("inf")
    p = None

    for place in place_list:
        if place[0] != given_place[0]:
            d = compute_distance(place, given_place)
            if d < min_dist:
                min_dist = d
                p = place
    return p


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


def generate_random_trajectories(place_list, n_users,
                                 trajectories_per_user_distribution,
                                 trajectory_size_distribution,
                                 trajectory_extent_distribution,
                                 prob_come_back=0.5,
                                 increase_extent=2.5):

    trajectory_result = dict()

    n_trajs_total = 0

    for u in range(0, n_users):
        # number of trajectories

        n_trajectories = dist.random_from_probability(trajectories_per_user_distribution)

        print 'User '+str(u) + ' with ' + str(n_trajectories)

        trajectories_count = 0

        trajectory_result[u] = []

        # create n trajectories
        # TODO melhorar a criacao das trajetorias para satisfazer a distribuicao de extent
        while trajectories_count < n_trajectories:

            today = datetime.datetime.fromtimestamp(time.time())

            n_points, extent = dist.random_from_probability_2(trajectory_size_distribution, trajectory_extent_distribution)

            traj = generate_trajectory(n_points, extent, place_list, today, prob_come_back, increase_extent)

            trajectories_count += 1

            n_trajs_total += 1

            trajectory_result[u].append(traj)

    print "Total trajectories: " + str(n_trajs_total)

    return trajectory_result


# Generate several trajectories and pick the best one based on the number
# of points and the extent
def generate_trajectory(n_points, extent, place_list, today, prob_come_back, increase_extent):

    total_extent = (extent/(n_points-1)) * increase_extent

    while True:
        traj = []
        places_count = 0
        from_place = None

        while places_count < n_points:

            tomorrow = today + TIME_DELTA

            place = get_next_place(total_extent, place_list, from_place, prob_come_back)

            if place is None:
                break

            traj.append(([place], today, tomorrow))

            places_count += 1

            from_place = place

            # go forward in time
            today = tomorrow + TIME_DELTA

        if places_count == n_points:
            break

    return traj












