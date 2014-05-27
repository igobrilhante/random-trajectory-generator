import extent_randtraj.extent_trajectory_generator as t

__author__ = 'igobrilhante'

if __name__ == '__main__':

    city = 'pisa'
    dows = ['wd', 'we']
    hours = 5

    prob_come_back = 0.001
    extent_factor = 1000000000

    for dow in dows:
        t.generate_random_trajectories(city, dow, hours, prob_come_back=prob_come_back, extent_factor=extent_factor)
