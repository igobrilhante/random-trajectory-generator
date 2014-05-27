from utils import db_utils

__author__ = 'igobrilhante'

import matplotlib.pyplot as plt
import numpy as np
from mpltools import style
from igraph import *
import brewer2mpl
import utils
from mpltools import layout

style.use('ggplot')

figsize = layout.figaspect(scale=1.0)
fig, axes = plt.subplots(figsize=figsize)

axes.xaxis.label.set_color('#000000')
axes.yaxis.label.set_size(18)
axes.xaxis.label.set_size(18)
axes.yaxis.label.set_color('#000000')
axes.xaxis.major.formatter._useMathText = True
axes.yaxis.major.formatter._useMathText = True

axes.set_yscale('log')
axes.set_xscale('log')

for spine in axes.spines:
    axes.spines[spine].set_color('#aeaeae')
axes.set_axis_bgcolor('white')

markers = ['s', '^', 'v', 'D', 'o', "p", '8', '*']
marker_size = 18
line_width = 0.5
alpha = 0.95
markeredgewidth = 0.0

colors = brewer2mpl.get_map('PuBuGn', 'Sequential', 9).mpl_colors

city = "firenze"
hours = "6"
dow = "we"

# Parametros Random Graph
# PISA
# n = 633
# m = 9310
# n = 576
# m = 3555

# MILAN
# n = 1690
# m = 33876
# n = 1575
# m = 10291

# FIRENZE
# n = 1837
# m = 65201
n = 1734
m = 21198

i = 1

########################## K Rand Traj ##########################
# i = 2
# ks = np.arange(0.25, 1.25, 0.25)
#
# for k in ks:
#
#     table = "network.krandomtraj_" + city+"_"+dow+"_"+str(hours)+"h_"+str(k).replace(".", "_")+"_node$"
#     agg = utils.agg_degree(db_utils.load_degree(table))
#
#     plt.plot(agg.degree, agg.total/float(np.sum(agg.total)), color=colors[i], label=str(int(k*100))+"%-RT", marker=markers[i], markersize=marker_size, linewidth=line_width, markeredgewidth=markeredgewidth, alpha=alpha)
#     i += 1


########################## Full Rand Traj ##########################

table = "network.fullrandtraj_" + city+"_"+dow+"_"+str(hours)+"h_node$"
agg = utils.agg_degree(db_utils.load_degree(table))

plt.plot(agg.degree, agg.total/float(np.sum(agg.total)), color=colors[i], label="FRT", marker=markers[i], markersize=marker_size, linewidth=line_width, markeredgewidth=markeredgewidth, alpha=alpha)

i += 2

# ############################### Rand Traj ##########################
#
# table = "network.randomtraj_" + city+"_"+dow+"_"+str(hours)+"h_node$"
# agg = utils.agg_degree(db_utils.load_degree(table))
#
# plt.plot(agg.degree, agg.total/float(np.sum(agg.total)), color=colors[i], label="DRT", marker=markers[i], markersize=marker_size, linewidth=line_width, markeredgewidth=markeredgewidth, alpha=alpha)
#
# i += 2

############################ Random Graph ##########################

graph = Graph.Erdos_Renyi(n=n, m=m, directed=False, loops=False)
agg = utils.agg_degree(np.array(graph.indegree()).view(dtype=[("degree", int)], type=np.recarray).copy())
plt.plot(agg.degree, agg.total/float(np.sum(agg.total)), color=colors[i], label="RG", marker=markers[i], markersize=marker_size+3, linewidth=line_width, markeredgewidth=markeredgewidth, alpha=alpha)

i += 1
####################################################################

table = "network."+city+"_fs_poiclusterf_traj_"+dow+"_"+hours+"h_trajs_node$"
agg = utils.agg_degree(db_utils.load_degree(table))
plt.plot(agg.degree, agg.total/float(np.sum(agg.total)), color=colors[6], label="PoI Network", marker=markers[6], markersize=marker_size, linewidth=line_width, markeredgewidth=markeredgewidth, alpha=alpha)


plt.tick_params(axis='both', which='major', labelsize=16, colors="#000000")
# plt.xlim([0, 1000])
# plt.ylim([-100, 100])


plt.xlabel('Degree')
plt.ylabel('Probability')

fig.tight_layout()
#
leg = plt.legend(loc=1, prop={'size': 18})
leg.get_frame().set_facecolor("white")
plt.show()