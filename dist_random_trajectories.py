import dist_randtraj.dist_trajectory_generator as t

__author__ = 'igobrilhante'

if __name__ == '__main__':

    city = 'firenze'
    dows = ['wd', 'we']
    hours = 5

    for dow in dows:
        t.generate_random_trajectories(city, dow, hours)
