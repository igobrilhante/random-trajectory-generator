__author__ = 'igobrilhante'


import db_utils

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from mpltools import style
from igraph import *
import brewer2mpl
import utils
from mpltools import layout

style.use('ggplot')

figsize = layout.figaspect(scale=0.8)
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

markers = ['o', '^', 's', 'D', 'o', "p", '8', '*']
marker_size = 12
line_width = 0.5
alpha = 0.8

city = "pisa"
hours = 6

colors = brewer2mpl.get_map('YlGnBu', 'sequential', 9).mpl_colors
colors = [colors[5], colors[8]]
i = 0

dows = ["wd", "we"]
labels = ["WD", "WE"]

stats = (
    ('node_count', len, 'total'),
)

for dow in dows:

    table = "/Users/igobrilhante/Documents/workspace/research/ComeTogether/experiments/network."+city+"_fs_poiclusterf_traj_"+dow+"_"+str(hours)+"h_trajs_communities.csv"
    data = mlab.csv2rec(table)
    agg = mlab.rec_groupby(data, ('node_count',), stats)
    print agg
    plt.plot(agg.node_count, agg.total, color=colors[i], label=labels[i], marker=markers[i], markersize=marker_size, linewidth=line_width, markeredgewidth=0.0, alpha=alpha)
    i += 1


plt.tick_params(axis='both', which='major', labelsize=16, colors="#000000")
# plt.xlim([-100, 1000])
# plt.ylim([-0.1, 1.1])


plt.xlabel('Number of nodes')
plt.ylabel('Number of communities')

fig.tight_layout()
#
leg = plt.legend(loc=1, prop={'size': 16})
leg.get_frame().set_facecolor("white")
plt.show()

# fig.savefig("/Users/igobrilhante/Dropbox/UFC/Ph.D. Report/Papers/MDM-JOURNALVERSION/tistJournal/figures/"+city+"-community-compactness.pdf")
