__author__ = 'igobrilhante'

import psycopg2
import numpy as np

DSN = "dbname=igo"

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def query(q):
    conn = psycopg2.connect(DSN)

    curs = conn.cursor()
    curs.execute(q)
    res = curs.fetchall()
    r = []
    for e in res:
        r.append(e[0])

    return np.array(r).view(dtype=[("key", int)], type=np.recarray).copy()


def load_degree(table):
    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    query = "select degree from "+table
    curs.execute(query)
    res = curs.fetchall()
    r = [int(e[0]) for e in res]

    return np.array(r).view(dtype=[("degree", int)], type=np.recarray).copy()


def load_compactness(table):
    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    query = "select traj_compactness from "+table
    curs.execute(query)
    res = curs.fetchall()
    r = [int(e[0]) for e in res]

    return np.array(r).view(dtype=[("compactness", int)], type=np.recarray).copy()


def query_places(table):
    conn = psycopg2.connect(DSN)

    q = "   select id, lat, lng, labels, categories " \
        "   from " + table

    curs = conn.cursor()
    curs.execute(q)
    res = curs.fetchall()

    r = []

    for e in res:
        # r.resize(count)
        # r[count - 1] = (e[0], e[1], e[2], e[3], e[4])
        # count += 1
        r.append([e[0], e[1], e[2], e[3].split(";"), e[4].split(";")])

    return r

#
# print query_places("pisa")


def create_or_replace_table(table, attributes):
    conn = psycopg2.connect(DSN)
    curs = conn.cursor()

    curs.execute("DROP TABLE IF EXISTS " + table)
    curs.execute("CREATE TABLE " + table + "(" + attributes + ")")
    conn.commit()


def get_number_of_users(table):
    query = " SELECT count(DISTINCT USERID) " \
            " FROM  " + table

    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    curs.execute(query)
    res = curs.fetchone()

    return int(res[0])


def get_number_of_trajectories():
    query = " SELECT count(DISTINCT TRAJID) " \
            " FROM  "

    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    curs.execute(query)
    res = curs.fetchone()

    return int(res[0])


def load_trajectories(table):
    conn = psycopg2.connect(DSN)
    curs = conn.cursor()

    query = "SELECT user_id, traj_id, poi_id, start_time, end_time " \
            "FROM " + table + " " + \
            "order by user_id, start_time"

    print query

    curs.execute(query)
    res = curs.fetchall()

    r = dict()

    last_user = None
    last_trajid = None
    last_time = None

    for e in res:
        current_user = e[0]
        current_traj = e[1]
        current_poi = int(e[2])
        current_time = e[3]
        end_time = e[4]

        if current_user == last_user:
            # ultima trajetoria
            traj = r[current_user][len(r[current_user])-1]

            # mesmo tempo anterior
            if last_time != current_time:
                # mesma trajetoria
                if current_traj == last_trajid:
                    traj.append(([current_poi], current_time, end_time))
                # nova trajetoria
                else:
                    r[current_user].append([([current_poi], current_time, end_time)])
        else:
            if current_user not in r:
                # lista de trajetorias
                r[current_user] = []

            # adiciona nova trajetoria
            r[current_user].append([([current_poi], current_time, end_time)])

        last_time = current_time
        last_user = current_user
        last_trajid = current_traj

    return r


def store_trajectories(trajectory_list, table):
    print "Storing trajectories into "+str(table)

    conn = psycopg2.connect(DSN)
    curs = conn.cursor()

    create_or_replace_table(table, "userid text, trajid text, poiid text, start_time timestamp, end_time timestamp")

    query = "INSERT INTO " + table + " VALUES(%s, %s, %s, %s, %s)"

    for userid in trajectory_list:

        user_trajectories = trajectory_list[userid]
        traj_count = 0
        for trajectory in user_trajectories:
            traj_id = str(userid) + "_" + str(traj_count)
            for position in trajectory:

                place_list = position[0]
                start_time = position[1]
                end_time = position[2]

                for place in place_list:

                    curs.execute(query, (str(userid),
                                         str(traj_id),
                                         str(place[0]),
                                         start_time.strftime(DATE_FORMAT),
                                         end_time.strftime(DATE_FORMAT)))
                conn.commit()

            traj_count += 1


