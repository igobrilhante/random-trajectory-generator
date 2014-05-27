from utils import db_utils

__author__ = 'igobrilhante'

import matplotlib.pyplot as plt
import numpy as np
from mpltools import style
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
marker_size = 10
line_width = 0.0
alpha = 0.8


hours = ["5", "6", "6"]
dow = "wd"

colors = brewer2mpl.get_map('YlGnBu', 'sequential', 9).mpl_colors
colors = [colors[3], colors[5], colors[8]]
i = 0

cities = ["Pisa", "Firenze", "Milan"]
labels = ["Pisa", "Florence", "Milan"]

for city in cities:

    table = "network."+city+"_fs_poiclusterf_traj_" + dow + "_" + hours[i] + "h_trajs_node$"
    agg = utils.agg_degree(db_utils.load_degree(table))

    plt.plot(agg.degree, agg.total/float(np.sum(agg.total)), color=colors[i], label=labels[i], marker=markers[i], markersize=marker_size, linewidth=line_width, markeredgewidth=0.0, alpha=alpha)
    i += 1


plt.tick_params(axis='both', which='major', labelsize=16, colors="#000000")
# plt.xlim([0, 1000])
# plt.ylim([-100, 100])


plt.xlabel('Degree')
plt.ylabel('Probability')

fig.tight_layout()
#
leg = plt.legend(loc=1, prop={'size': 16})
leg.get_frame().set_facecolor("white")
plt.show()