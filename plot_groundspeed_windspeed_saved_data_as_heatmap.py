from __future__ import print_function
import numpy as np
import os, sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random
import json
import seaborn as sns
import cv2
from matplotlib.path import Path
import matplotlib.patches as patches


def adjust_spines(ax_handle, spines):
    for loc, spine in ax_handle.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))  # outward by 10 points
            #spine.set_smart_bounds(True)
        else:
            spine.set_color('none')  # don't draw spine
    # turn off ticks where there is no spine
    if 'left' in spines:
        ax_handle.yaxis.set_ticks_position('left')
    else:
        # no yaxis ticks
        ax_handle.yaxis.set_ticks([])
    if 'bottom' in spines:
        ax_handle.xaxis.set_ticks_position('bottom')
    else:
        # no xaxis ticks
        ax_handle.xaxis.set_ticks([])

with open('./simulated_groundspeeds_vs_windspeeds_along_trajectories.json') as f:
    dictionary = json.load(f)


all_windspeeds_along_trajectories=[]
all_groundspeeds_along_trajectories=[]
randomly_labeled_point_count = 0
for windspeed in dictionary:
    for wind_dir in dictionary[windspeed]:
        try:
            all_windspeeds_along_trajectories.append(dictionary[windspeed][wind_dir]['windspeeds along trajectories'][0])
            all_groundspeeds_along_trajectories.append(dictionary[windspeed][wind_dir]['groundspeeds along trajectories'][0])
        except:
            continue



f, ax = plt.subplots(figsize=(10,10))
ax.set_ylim(-0, 5)
ax.set_xlim(-2, 3)
sns.set_style("white")
#sns.kdeplot(all_windspeeds_along_trajectories, all_groundspeeds_along_trajectories, shade = True, shade_lowest = False, n_levels = 300,bw=0.035)
sns.kdeplot(all_windspeeds_along_trajectories, all_groundspeeds_along_trajectories, shade = False, shade_lowest = False)
ax.scatter(0,1)
adjust_spines(ax, spines=['bottom','left'])
ax.set_ylabel('groundspeed along trajectory, m/s')
ax.set_xlabel('windspeed along trajectory, m/s')
#plt.savefig('./modeled_groundspeed_vs_windspeed_kde_plot_300levels_.035bandwidth.svg', transparent = True)
#plt.show()

# for item in ax.collections:
#     print ('')
#     print ('New item')
#     for path in item.get_paths():
#         print (path)
#     # list_of_vertices = path.vertices
#     # print ('number of vertices: '+str(len(list_of_vertices)))
#     # print (list_of_vertices[5])
# plt.show()

item = ax.collections[0]
for path in item.get_paths():
    verts = path.vertices
    codes = [0]+[Path.LINETO]*(len(verts)-2)+[0]
    codes[-1]=(Path.CLOSEPOLY)
    codes[0] =(Path.MOVETO)
    path = Path(verts, codes)
    patch = patches.PathPatch(path, facecolor='orange', lw=2)
    ax.add_patch(patch)
    list_of_vertices = verts.tolist()
    with open('./patch_contour_vertices.json', mode = 'w') as f:
        json.dump({'list of vertices':list_of_vertices},f, indent = 1)
plt.show()
