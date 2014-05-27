from full_randtraj import full_trajectory_generator as fullrandtraj

__author__ = 'igobrilhante'

if __name__ == '__main__':

    city = 'pisa'
    dows = ['wd', 'we']
    hours = 5

    for dow in dows:
        fullrandtraj.generate_random_trajectories(city, dow, hours)
