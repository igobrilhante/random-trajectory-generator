__author__ = 'igobrilhante'

from igraph import *
import numpy as np

n = 633
m = 9310

graph = Graph.Erdos_Renyi(n=n, m=m, directed=False, loops=False)


print graph.average_path_length()
print graph.transitivity_avglocal_undirected()


