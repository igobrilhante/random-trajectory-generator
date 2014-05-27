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


trajectories_per_user_distribution_f = ""
trajectory_size_distribution_f = ""
trajectory_extent_distribution_f = ""

# number of users
n_users = 10

R_EARTH = 6371000

MAX_ITER = 10
MAX_TRAJS = 100

TABLE_SCHEMA = "randomtraj."

TIME_DELTA = datetime.timedelta(minutes=45)

# distance from place to place
DISTANCE = [50, 75]


def meters2degree(meters):
    return meters * (180 / math.pi / R_EARTH)


def degree2meters(degree):
    return degree / (180 / math.pi / R_EARTH)


# Get a next place from a given place w.r.t. an extent
def get_next_place(_extent, _place_list, _from_place):
    r_ = random.randint(0, len(_place_list) - 1)
    if _from_place is None:
        return _place_list[r_]
    else:
        allowed_list = []
        for p in _place_list:
            if p[0] != _from_place[0]:
                d = compute_distance(p, _from_place)
                if d <= _extent:
                    allowed_list.append(p)

        l = np.max([len(allowed_list) - 1, 1])
        r = random.randint(0, l) if l > 1 else 0
        return allowed_list[r] if len(allowed_list) > 0 else None


# Get close places to a given place
def get_close_places(given_place, place_list):

    res = [given_place]
    for place in place_list:
        if place[0] != given_place[0]:
            d = compute_distance(place, given_place)
            if d <= random.randint(50, 80):
                res.append(place)

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

    ted = queries.create_ted(city, dow, hours)

    ################################## END QUERIES ##################################

    # LOAD DATA
    # Compute the distributions
    n_users = db.get_number_of_users(city, dow, hours)

    trajectories_per_user_distribution = dist.compute_probability_distribution(db.query(tpu))

    trajectory_size_distribution = dist.compute_probability_distribution(db.query(tsd))
    print "Trajectory Size Distri ", trajectory_size_distribution

    trajectory_extent_distribution = dist.compute_probability_density_function(db.query(ted))
    print "Trajectory Extent Dist ", trajectory_extent_distribution

    print "N of users:", n_users

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

            # number of points
            n_points = dist.random_from_probability(trajectory_size_distribution)

            # extent of the trajectory
            extent = dist.random_from_probability(trajectory_extent_distribution)

            traj = generate_trajectory(n_points, extent, place_list, today)

            trajectories_count += 1

            n_trajs_total += 1

            trajectory_result[u].append(traj)

    print "Total trajectories: " + str(n_trajs_total)

    table = TABLE_SCHEMA + city+"_"+str(hours)+"h_"+dow

    db.store_trajectories(trajectory_result, table)


# Generate several trajectories and pick the best one based on the number
# of points and the extent
def generate_trajectory(n_points, extent, place_list, today):

    best_traj = []
    best_extent = 0.0
    best_points = float("inf")

    traj_iter_count = 0

    while traj_iter_count < MAX_TRAJS:
        traj = []
        places_count = 0
        from_place = None
        total_extent = extent
        traj_extent = 0.0

        while traj_extent <= extent:

            tomorrow = today + TIME_DELTA

            place = get_next_place(total_extent, place_list, from_place)

            if place is None:
                break

            places = get_close_places(place, place_list)

            traj.append((places, today, tomorrow))

            traj_extent += compute_distance(place, from_place) if from_place is not None else 0
            total_extent = extent - traj_extent

            places_count += 1

            from_place = place

            # go forward in time
            today = tomorrow + TIME_DELTA

        traj_iter_count += 1
        # print "%s(%s), %s(%s)" % (traj_extent, extent, places_count, n_points)
        if traj_extent > best_extent and places_count == n_points:
            best_traj = traj
            best_extent = traj_extent
            best_points = math.fabs(places_count-n_points)

            if math.fabs(best_extent - extent) <= 100:
                break
    return best_traj












