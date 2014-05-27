__author__ = 'igobrilhante'

import matplotlib.mlab as mlab
import numpy as np
import random
import utils


def read_distribution(f):
    print f


# Compute probability distribution
# return an array of cumulative probability
def compute_probability_distribution(arr, is_cum_sum=True):
    # stats used - count

    agg_data = utils.array2recarray( arr )
    stats = (
        ("key", len, 'total'),
    )

    res = mlab.rec_groupby(agg_data, ('key',), stats)
    if is_cum_sum:
        cumsum = np.cumsum(res.total/float(len(arr)))
    else:
        cumsum = res.total/float(len(arr))
    # return array with the keys and the cummulative distribution
    return np.array([res.key, cumsum])



# Compute probability density function
# Return array of probability of k <= x
def compute_probability_density_function(data, is_cum_sum=True):

    # keys to be used on axis x
    # m = np.max(data)
    # s = np.arange(1000, m+5001, m/10)

    freq, bins = np.histogram(data)

    s = np.sum(freq)
    if is_cum_sum:
        cumsum = np.cumsum(freq/float(s))
    else:
        cumsum = freq/float(s)

    # return array with the keys and the cummulative distribution
    return np.array([bins, cumsum])


# Generate random value based on the given distribution
def random_from_probability(distribution):
    # res corresponds to the keys
    res = distribution[0]
    # cumulative distribution
    cumsum = distribution[1]

    # Flip the coin
    flip = random.uniform(0, 1)
    # Initialize the element
    elem = -1


    # get the element if its probability if greater than the flip value
    for i in range(0, len(cumsum)):
        if flip <= cumsum[i]:
            elem = res[i]
            break

    return elem

# Generate random value based on the given distribution
def random_from_probability_2(distribution_1, distribution_2):
    # res corresponds to the keys
    res_1 = distribution_1[0]
    # cumulative distribution
    cumsum_1 = distribution_1[1]

        # res corresponds to the keys
    res_2 = distribution_2[0]
    # cumulative distribution
    cumsum_2 = distribution_2[1]

    # Flip the coin
    flip = random.uniform(0, 1)
    # Initialize the element
    elem_1 = -1

    # get the element if its probability if greater than the flip value
    for i in range(0, len(cumsum_1)):
        if flip <= cumsum_1[i]:
            elem_1 = res_1[i]
            break

    elem_2 = -1

    # get the element if its probability if greater than the flip value
    for i in range(0, len(cumsum_2)):
        if flip <= cumsum_2[i]:
            elem_2 = res_2[i]
            break

    return elem_1, elem_2


# pdf = compute_probability_density_function("/tmp/teste_pdf.txt")
#
# prob = compute_probability_distribution("/tmp/teste.txt")
#
# print random_from_probability(prob)
# print random_from_probability(pdf)


