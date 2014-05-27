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
import utils


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


# Get a next place from a given place w.r.t. an extent
def get_next_place( limit_extent, place_list, from_place, prob_come_back ):

    if limit_extent < 0:
        return None

    r_ = random.randint(0, len(place_list) - 1)

    # select the first place
    if from_place is None:
        return place_list[r_]
    # otherwise select the next one from a given place _from_place
    else:

        allowed_list = filter_close_places(from_place, limit_extent, place_list)
        l = np.max([len(allowed_list) - 1, 1])
        # len is at least 1, which include from_place itself
        # if more than one PoI is found
        if len(allowed_list) > 1:
            r = random.randint(0, l)
            return allowed_list[r]
        # otherwise
        else:
            nn = get_nearest_place(from_place, place_list)

            distance = utils.compute_distance(from_place, nn)
            # returns the nearest place if the distance between it and from_place is shorter than limit_extent
            # otherwise do not retrieve any place
            return nn #if distance < limit_extent else None

            # return None

            # # probabilidade de voltar para o mesmo ponto
            # f = random.random()
            # if f > prob_come_back:
            #     return get_closer_place(_from_place, _place_list)
            # else:
            #     return _from_place


# filter out places that are reacheable from a given one
def filter_close_places(from_place, limit_extent, place_list):
    allowed_list = []
    for p in place_list:
        d = utils.compute_distance(p, from_place)
        if d <= limit_extent:
            allowed_list.append(p)
    return allowed_list


def get_nearest_place(given_place, place_list):
    min_dist = float("inf")
    p = None

    for place in place_list:
        if place[0] != given_place[0]:
            d = utils.compute_distance(place, given_place)
            if d < min_dist:
                min_dist = d
                p = place
    return p


# Get close places to a given place
def get_close_places(given_place, place_list):

    res = [given_place]
    # for place in place_list:
    #     if place[0] != given_place[0]:
    #         d = compute_distance(place, given_place)
    #         if d <= random.randint(60, 80):
    #             res.append(place)

    return res




def generate_random_trajectories(city, dow, hours, prob_come_back=0.5, extent_factor=2.5):

    print city, dow, hours, prob_come_back, extent_factor

    trajectory_result = dict()

    place_list = db.query_places(city, dow, hours)

    ################################## QUERIES ##################################

    tsd = queries.create_tsd(city, dow, hours)

    tpu = queries.create_tpu(city, dow, hours)

    # ted = queries.create_ted(city, dow, hours)

    ################################## END QUERIES ##################################

    # LOAD DATA
    # Compute the distributions
    n_users = db.get_number_of_users(city, dow, hours)

    trajectories_per_user_distribution = dist.compute_probability_distribution(db.query(tpu))

    # trajectory_size_distribution = dist.compute_probability_distribution(db.query(tsd))
    # print "Trajectory Size Distri ", trajectory_size_distribution

    trajectory_extent_distribution = dist.compute_probability_density_function(db.query_trajectory_extent( city, dow, hours ))
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

            # extent = dist.random_from_probability_2(trajectory_size_distribution,
            #                                                   trajectory_extent_distribution)

            # # number of points
            # n_points = dist.random_from_probability(trajectory_size_distribution)
            #
            # # extent of the trajectory
            extent = dist.random_from_probability(trajectory_extent_distribution)

            # print "Generating Traj ", trajectories_count+1, extent
            traj = generate_trajectory(extent, place_list, today, prob_come_back, extent_factor)

            trajectories_count += 1

            n_trajs_total += 1

            # print "Generated Traj ", utils.compute_trajectory_extent(traj)
            trajectory_result[u].append(traj)

    max_extent = np.max(trajectory_extent_distribution[0])
    print max_extent

    today = datetime.datetime.fromtimestamp(time.time())

    traj = generate_trajectory(max_extent, place_list, today, prob_come_back, extent_factor)
    print "Generated Traj ", utils.compute_trajectory_extent(traj)

    trajectory_result[n_users] = [traj]
    n_trajs_total += 1

    print "Total trajectories: " + str(n_trajs_total)

    table = TABLE_SCHEMA + city+"_"+str(hours)+"h_"+dow

    db.store_trajectories(trajectory_result, table)


# Generate several trajectories and pick the best one based on the number
# of points and the extent
def generate_trajectory(extent, place_list, today, prob_come_back, extent_factor):

    total_extent = 0.0
    from_place = None
    traj = []

    while True:

        tomorrow = today + TIME_DELTA

        place = get_next_place(extent - total_extent, place_list, from_place, prob_come_back)

        if place is None:
            break

        traj.append(([place], today, tomorrow))

        total_extent += utils.compute_distance(place, from_place) if from_place is not None else 0
        # total_extent = extent - traj_extent

        # print extent, total_extent
        # print from_place, place
        from_place = place
        # go forward in time
        today = tomorrow + TIME_DELTA

        # print extent, total_extent, utils.compute_trajectory_extent(traj)
    return traj












