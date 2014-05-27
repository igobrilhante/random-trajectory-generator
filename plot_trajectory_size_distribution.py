__author__ = 'igobrilhante'

import db_utils
import queries
import distribution_utils as dist
import matplotlib.pyplot as plt
from mpltools import style
from mpltools import layout

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
dow = "we"
hours = 6
# method = "krandomtraj"
# method = "fullrandtraj"
method = "randomtraj"

query_tsd = queries.create_tsd_from_table("(select * from "+method+"."+city+"_"+str(hours)+"h_"+dow+" ) a")
query_tsd_original = queries.create_tsd(city, dow, hours)

dist_tsd = dist.compute_probability_distribution(db_utils.query(query_tsd), is_cum_sum=False)
dist_tsd_original = dist.compute_probability_distribution(db_utils.query(query_tsd_original), is_cum_sum=False)

print "TSD ",dist_tsd[0], dist_tsd[1]
print "TSD ORIGINAL", dist_tsd_original[0], dist_tsd_original[1]


plt.plot(dist_tsd[0], dist_tsd[1], label="Random", marker='s', markersize=5, alpha=alpha)
plt.plot(dist_tsd_original[0], dist_tsd_original[1], marker='3', markersize=5, label="Original", alpha=alpha)

plt.tick_params(axis='both', which='major', labelsize=24, colors="#000000")
plt.xlabel('x')
plt.ylabel('P')
leg = plt.legend(loc=1, prop={'size': 18})
leg.get_frame().set_facecolor("white")
#
fig.tight_layout()
#
plt.show()



