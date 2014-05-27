from extent_randtraj import trajectory_generator as t

__author__ = 'igobrilhante'

if __name__ == '__main__':

    city = 'firenze'
    dows = ['wd', 'we']
    hours = 6

    prob_come_back = 0.001
    extent_factor = 1000000000

    for dow in dows:
        t.generate_random_trajectories(city, dow, hours, prob_come_back=prob_come_back, extent_factor=extent_factor)
