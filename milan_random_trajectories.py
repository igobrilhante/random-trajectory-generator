__author__ = 'igobrilhante'

import trajectory_generator_count as t

if __name__ == '__main__':

    city = 'milan'
    dows = ['wd', 'we']
    hours = 6

    for dow in dows:
        t.generate_random_trajectories(city, dow, hours)
