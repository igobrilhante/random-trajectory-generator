__author__ = 'igobrilhante'

import trajectory_generator as t
import db_utils as db
import distribution_utils as dist
import queries

if __name__ == '__main__':

    city = "pisa"
    dow = "we"
    hours = "5"

    place_table = "( select a.id, a.lat, a.lng, c.labels, c.categories from \
           poi_table ) a"

    traj_table = "( select * from traj_table ) a "
    traj_output_table = "randomtraj.teste"

    place_list = db.query_places(place_table)


        ################################## QUERIES ##################################

    # trajectory size (number of points) distribution
    tsd = queries.create_tsd_from_table(traj_table)

    # trajectory per user distribution
    tpu = queries.create_tpu_from_table(traj_table)

    # trajectory extent distribution
    ted = queries.create_ted(city, dow, hours)

    ################################## END QUERIES ##################################

    # LOAD DATA
    # Compute the distributions
    n_users = db.get_number_of_users(traj_table)

    trajectories_per_user_distribution = dist.compute_probability_distribution(db.query(tpu))
    print "Trajectory Per User ", trajectories_per_user_distribution

    trajectory_size_distribution = dist.compute_probability_distribution(db.query(tsd))
    print "Trajectory Size Distri ", trajectory_size_distribution

    trajectory_extent_distribution = dist.compute_probability_density_function(db.query(ted))
    print "Trajectory Extent Dist ", trajectory_extent_distribution

    print "N of users:", n_users

    generated_trajs = t.generate_random_trajectories(place_list, n_users, trajectories_per_user_distribution, trajectory_size_distribution, trajectory_extent_distribution)


    db.store_trajectories(generated_trajs, "randomtraj.teste")


    '''
        CHECK THE RESULT
    '''

    query_tsd = queries.create_tsd_from_table("(select * from randomtraj.teste ) a")
    query_tsd_original = queries.create_tsd(city, dow, hours)

    dist_tsd = dist.compute_probability_distribution(db.query(query_tsd), is_cum_sum=False)
    dist_tsd_original = dist.compute_probability_distribution(db.query(query_tsd_original), is_cum_sum=False)

    query_ted = queries.create_ted_from_table("(select * from randomtraj.teste ) a", city)
    query_ted_original = queries.create_ted(city, dow, hours)

    dist_ted = dist.compute_probability_density_function(db.query(query_ted))

    dist_ted_original = dist.compute_probability_density_function(db.query(query_ted_original))

    print "TED", dist_ted[0], dist_ted[1]

    print "TED ORIGINAL", dist_ted_original[0], dist_ted_original[1]

    print "TSD ",dist_tsd[0], dist_tsd[1]
    
    print "TSD ORIGINAL", dist_tsd_original[0], dist_tsd_original[1]
