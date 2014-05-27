__author__ = 'igobrilhante'

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from mpltools import style
import brewer2mpl
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

for spine in axes.spines:
    axes.spines[spine].set_color('#aeaeae')
axes.set_axis_bgcolor('white')

markers = ['o', '^', 's', 'D', 'o', "p", '8', '*']
marker_size = 12
line_width = 0.5
alpha = 0.8

city = "firenze"
hours = 6

colors = brewer2mpl.get_map('YlGnBu', 'sequential', 8).mpl_colors
i = 2

dow = "wd"
# label = "WD"



# ############################ Dist Random Trajectories #############################

# i += 1
# table = "/Users/igobrilhante/Documents/workspace/research/ComeTogether/experiments/network.randomtraj_"+city+"_"+dow+"_"+str(hours)+"h_trajs_communities.csv"
# agg = np.histogram(mlab.csv2rec(table).traj_compactness, bins=np.arange(0.0, 1.1, 0.1))
# plt.plot(agg[1][1:len(agg[1])], np.cumsum(agg[0])/float(agg[0].sum()), color=colors[i], label="DRT", marker=markers[i], markersize=marker_size, linewidth=line_width, markeredgewidth=0.0, alpha=alpha)


# ############################ K Random Trajectories #############################
ks = np.arange(0.25, 1.25, 0.25)

for k in ks:

    i += 1
    table = "/Users/igobrilhante/Documents/workspace/research/ComeTogether/experiments/network.krandomtraj_"+city+"_"+dow+"_"+str(hours)+"h_"+str(k).replace(".", "_")+"_trajs_communities.csv"

    agg = np.histogram(mlab.csv2rec(table).traj_compactness, bins=np.arange(0.0, 1.1, 0.1))

    plt.plot(agg[1][1:len(agg[1])], np.cumsum(agg[0])/float(agg[0].sum()), color=colors[i], label=str(k*100)+"-RT", marker=markers[i], markersize=marker_size, linewidth=line_width, markeredgewidth=0.0, alpha=alpha)


# ############################ PoI Network #############################

table = "/Users/igobrilhante/Documents/workspace/research/ComeTogether/experiments/network."+city+"_fs_poiclusterf_traj_"+dow+"_"+str(hours)+"h_trajs_communities.csv"
agg = np.histogram(mlab.csv2rec(table).traj_compactness, bins=np.arange(0.0, 1.1, 0.1))
plt.plot(agg[1][1:len(agg[1])], np.cumsum(agg[0])/float(agg[0].sum()), color=colors[2], label="PoI Network", marker=markers[2], markersize=marker_size, linewidth=line_width, markeredgewidth=0.0, alpha=alpha)




plt.tick_params(axis='both', which='major', labelsize=16, colors="#000000")
plt.xlim([0.0, 1.1])
plt.ylim([-0.1, 1.1])


plt.xlabel('Compactness')
plt.ylabel('P(k <= x)')

fig.tight_layout()
#
leg = plt.legend(loc=2, prop={'size': 16})
leg.get_frame().set_facecolor("white")
plt.show()

fig.savefig("/Users/igobrilhante/Dropbox/UFC/Ph.D. Report/Papers/GraphMobility/journal-version/figures/"+city+"/"+city+"-community-compactness"+dow+".pdf")
