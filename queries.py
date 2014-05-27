__author__ = 'igobrilhante'


def create_tsd(city, dow, hours):
    return " select count::int as total \
            from                            \
            (\
                select trajid, count(*)\
                from\
                (\
                    select distinct trajid, start_time\
                    from " + city + ".traj_fs_poiclusterf_" + dow + "_" + str(hours) + "h_1p_200m_1200s_150m\
                    order by trajid, start_time\
                ) a\
            group by trajid\
            ) a"

def create_tsd_from_table(table):
    return " select count::int as total \
            from                            \
            (\
                select trajid, count(*)\
                from\
                (\
                    select distinct trajid, start_time\
                    from " + table + "\
                    order by trajid, start_time\
                ) a\
            group by trajid\
            ) a"


def create_tpu(city, dow, hours):
    return " select count as total \
            from \
            ( \
                select userid, count(*) \
                from \
                ( \
                    select distinct userid,trajid \
                    from " + city + ".traj_fs_poiclusterf_" + dow + "_" + str(hours) + "h_1p_200m_1200s_150m \
                    order by userid \
                ) a \
            group by userid \
            ) a"


def create_tpu_from_table(table):
    return " select count as total \
            from \
            ( \
                select userid, count(*) \
                from \
                ( \
                    select distinct userid,trajid \
                    from " + table + " \
                    order by userid \
                ) a \
            group by userid \
            ) a"


def create_ted(city, dow, hours):
    return " select l::int \
            from \
            ( \
            select trajid, st_length(ST_Transform(st_makeline(object), 26986)) as l \
            from \
            ( \
            select * \
            from foursquare.poifcluster_1p_200m_" + city + " p, \
             " + city + ".traj_fs_poiclusterf_" + dow + "_" + str(hours) + "h_1p_200m_1200s_150m t \
             where t.poiid = p.clus::text \
             order by userid, start_time \
             ) a \
            group by trajid \
            ) a"


def create_ted_from_table(table, city):
    return " select l::int \
            from \
            ( \
            select trajid, st_length(ST_Transform(st_makeline(object), 26986)) as l \
            from \
            ( \
            select * \
            from foursquare.poifcluster_1p_200m_" + city + " p, \
             " + table + " t \
             where t.poiid = p.clus::text \
             order by userid, start_time \
             ) a \
            group by trajid \
            ) a"