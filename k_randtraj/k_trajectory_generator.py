from utils import db_utils as db

__author__ = 'igobrilhante'

import random
import utils.db_utils as db
import utils.utils as utils



TABLE_SCHEMA = "krandomtraj."


def randomize_place(place_list, place):

    aux = -1
    for poi in place_list:
        if poi[0] == place:
            aux = poi
            break
    candidates = []
    for poi in place_list:
        if list(set(poi[4]) & set(aux[4])):
            candidates.append(poi)

    r = random.randint(0, len(candidates)-1)
    return candidates[r]


# Get close places to a given place
def get_close_places(given_place, place_list, m):

    res = [given_place]

    return res
    # for place in place_list:
    #     if place[0] != given_place[0]:
    #         d = utils.compute_distance(place, given_place)
    #         if d <= random.randint(60, 80):
    #             res.append(place)
    #
    # return res[0: min(m, len(res))]


def generate(k, city, dow, hours):
    # carregar trajetorias
    users_trajectories = db.load_trajectories(city, dow, hours)

    count = 0
    place_list = db.query_places(city, dow, hours)
    print "###\tNumber of places is %s" % len(place_list)
    trajectory_result = dict()
    for user in users_trajectories:
        user_traj = users_trajectories[user]
        user_traj_res = []
        for traj in user_traj:

            traj_size = len(traj)
            k_size = int(traj_size*k)

            if k_size == 0 and k > 0.0:
                k_size = 1

            count += 1

            # repete o inicio da trajetoria
            rand_traj = []
            for i in range(0, traj_size-k_size):
                point = traj[i]
                poi = utils.get_poi(place_list, point[0])

                rand_traj.append((poi, traj[i][1], traj[i][2]))

            # randomizar os outros locais
            for i in range(traj_size-k_size, traj_size):
                place = traj[i][0]

                # randomiza o local
                new_place = randomize_place(place_list, place[0])
                new_places = get_close_places(new_place, place_list, len(traj[i]))

                rand_traj.append((new_places, traj[i][1], traj[i][2]))

            if len(rand_traj) != len(traj):
                raise Exception('len(rand_traj) != len(traj)')
            user_traj_res.append(rand_traj)

        trajectory_result[user] = user_traj_res

    # pertecenge to randomize
    print "###\tTotal of affected trajectories is %i for %s users!" % (count, len(users_trajectories))

    table = TABLE_SCHEMA + city+"_"+str(hours)+"h_"+dow+"_"+str(k).replace(".", "_")

    print "###\tStoring trajectories into %s" % table

    # db.store_trajectories(trajectory_result, table)

for w in ["wd", "we"]:
    for k in [0.25]:
        generate(k, "firenze", w, 6)