__author__ = 'igobrilhante'

import psycopg2
import numpy as np
import matplotlib.mlab as mlab
import utils

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

    return res


def load_degree(table):
    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    query = "select degree from "+table
    curs.execute(query)
    res = curs.fetchall()
    r = [int(e[0]) for e in res]

    return np.array(r).view(dtype=[("degree", int)], type=np.recarray).copy()


def load_compactness(name):
    rec = mlab.csv2rec(name, comments='#', skiprows=1)

    return np.array(rec['traj_compactness']).view(dtype=[("compactness", int)], type=np.recarray).copy()


def query_trajectory_extent_by_query( query, city, dow, hours ):
    users_trajectories = load_trajectories_by_query( query )
    poi_list = query_places( city, dow, hours )

    return compute_trajectories_extent( users_trajectories, poi_list )


def compute_trajectories_extent( users_trajectories, poi_list ):
    res = []
    for user in users_trajectories:
        user_traj = users_trajectories[user]
        for traj in user_traj:
            for i in xrange(len(traj)):
                poi = utils.get_poi(poi_list, traj[i][0])
                # print traj[0x]
                traj[i] = (poi, traj[i][1], traj[i][2])

        res.append(utils.compute_trajectory_extent(traj))
    print np.min(res), np.max(res)
    return res

def query_trajectory_extent( city, dow, hours  ):

    users_trajectories = load_trajectories( city, dow, hours )
    poi_list = query_places( city, dow, hours )

    return compute_trajectories_extent( users_trajectories, poi_list )


def query_places(city, dow, hours):
    conn = psycopg2.connect(DSN)

    q = "   select a.id, a.lat, a.lng, c.labels, c.categories from \
            (\
            select clus as id, st_y(object) as lat, st_x(object) as lng, row_number() over (ORDER BY clus) as line from foursquare.poifcluster_1p_200m_" + city + " \
            order by clus) a\
            ,\
            (\
            select id, min(line) line\
            from\
            (\
            select clus as id, row_number() over (ORDER BY clus) as line from foursquare.poifcluster_1p_200m_" + city + "\
            order by clus) a\
            group by id\
            ) b, \
            ( \
                select  clus, string_agg(replace(replace(name, ';', ''), ',', ''), ';') labels, \
                        string_agg(replace(replace(category, ';', ''), ',', ''), ';') categories \
                from foursquare.poifcluster_1p_200m_" + city + " f, foursquare.poi_" + city + "_f p \
                where f.object = p.object \
                group by clus \
                order by clus \
            ) c \
            where \
                a.line = b.line \
                and a.id = c.clus \
                and a.id::text in (SELECT DISTINCT POIID::text FROM   " + city + ".traj_fs_poiclusterf_" + dow + "_" + str(hours) + "h_1p_200m_1200s_150m) \
            order by a.id"
    curs = conn.cursor()
    curs.execute(q)
    res = curs.fetchall()
    # r = np.array([]).view(dtype=[("id", int), ("lat", float), ("lng", float), ("labels", np.object), ("categories", np.object)], type=np.recarray).copy()
    r = []

    count = 1

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


def get_number_of_users(city, dow, hours):
    query = "SELECT COUNT(*) FROM " \
            "(SELECT DISTINCT USERID " \
            " FROM  " + city + ".traj_fs_poiclusterf_" + dow + "_" + str(hours) + "h_1p_200m_1200s_150m" \
                                                                                  ") a"

    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    curs.execute(query)
    res = curs.fetchone()

    return int(res[0])


def get_number_of_trajectories(city, dow, hours):
    query = "SELECT COUNT(*) FROM " \
            "(SELECT DISTINCT TRAJID " \
            " FROM  " + city + ".traj_fs_poiclusterf_" + dow + "_" + str(hours) + "h_1p_200m_1200s_150m" \
                                                                                  ") a"

    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    curs.execute(query)
    res = curs.fetchone()

    return int(res[0])


def load_trajectories_by_query( query ):
    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    curs.execute(query)
    res = curs.fetchall()
    # r = np.array([]).view(dtype=[("user_id", basestring), ("traj_id", basestring), ("poi_id", basestring), ("start_time", np.basestring)], type=np.recarray).copy()
    r = dict()
    count = 1

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
            idx = len(traj)-1
            # mesmo tempo anterior
            if last_time == current_time:
                traj[idx][0].append(current_poi)
            else:
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

def load_trajectories(city, dow, hours):

    query = "SELECT * " \
            "FROM " + city + ".traj_fs_poiclusterf_" + dow + "_" + str(hours) + "h_1p_200m_1200s_150m " \
                                                                                "order by userid, start_time"

    return load_trajectories_by_query( query )




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
            print "Storing Traj %s %s" % (traj_id, utils.compute_trajectory_extent(trajectory))
            for position in trajectory:

                place_list = position[0]
                start_time = position[1]
                end_time = position[2]

                for place in place_list:
                    # insert the data into the database TODO
                    curs.execute(query, (str(userid),
                                         str(traj_id),
                                         str(place[0]),
                                         start_time.strftime(DATE_FORMAT),
                                         end_time.strftime(DATE_FORMAT)))
                conn.commit()

            traj_count += 1


