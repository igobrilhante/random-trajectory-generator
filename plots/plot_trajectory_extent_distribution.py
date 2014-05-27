from utils import db_utils

__author__ = 'igobrilhante'

import matplotlib.pyplot as plt
from mpltools import style
from mpltools import layout


print plt.get_backend()

style.use('ggplot')

alpha = 0.7

figsize = layout.figaspect(scale=1.2)
fig, axes = plt.subplots(figsize=figsize)
axes.xaxis.label.set_color('#000000')
axes.yaxis.label.set_color('#000000')
#
for spine in axes.spines:
    axes.spines[spine].set_color('#aeaeae')
axes.set_axis_bgcolor('white')
#
axes.yaxis.label.set_size(22)
axes.xaxis.label.set_size(22)

city = "milan"
dow = "wd"
hours = 5
# method = "krandomtraj"
# method = "fullrandtraj"
method = "randomtraj."

traj_query = "select * from %s order by userid, start_time" % ( method + city+"_"+str(hours)+"h_"+dow )


dist_ted = dist.compute_probability_density_function(db_utils.query_trajectory_extent_by_query( traj_query, city, dow, hours ))

dist_ted_original = dist.compute_probability_density_function(db_utils.query_trajectory_extent( city, dow, hours ))

print "TED", dist_ted[0], dist_ted[1]

print "TED ORIGINAL", dist_ted_original[0], dist_ted_original[1]


plt.plot(dist_ted_original[0][1:len(dist_ted_original[0])], dist_ted_original[1], marker='3', markersize=5, label="Original", alpha=alpha)
plt.plot(dist_ted[0][1:len(dist_ted[0])], dist_ted[1], label="Random", marker='s', markersize=5, alpha=alpha)

plt.tick_params(axis='both', which='major', labelsize=24, colors="#000000")
plt.xlabel('x')
plt.ylabel('Probability')
leg = plt.legend(loc=1, prop={'size': 18})
leg.get_frame().set_facecolor("white")
#
fig.tight_layout()
#
plt.show()



