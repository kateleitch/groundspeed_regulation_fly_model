from __future__ import print_function
import numpy as np
import os, sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random
import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import cv2

#******* some figure defaults *******
plt.rcParams['xtick.labelsize']=14
plt.rcParams['ytick.labelsize']=14
#************************************


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

def ask_if_point_is_within_model_patch(point_to_check, patch_contour_vertices):
    #polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
    polygon = Polygon(patch_contour_vertices)
    point = Point(point_to_check)
    return polygon.contains(point)

with open('./second_fly_arrival_groundspeeds_vs_windspeeds.json') as f:
    dictionary = json.load(f)
with open('./patch_contour_vertices.json') as f:
    vertices = json.load(f)['list of vertices']

vertices_as_tuples = [(x[0],x[1])for x in vertices]

groundspeeds = dictionary['groundspeeds']
windspeeds = dictionary['windspeeds']

fractions_inside_patch=[]
shuffling_iteration_number = 20000
for i in range (shuffling_iteration_number):
    resampled_windspeeds = np.random.choice(windspeeds, len(windspeeds), replace=False)
    resampled_groundspeeds = np.random.choice(groundspeeds, len(groundspeeds), replace=False)
    in_patch_count=0.
    total_count = 0.
    for index, resampled_groundspeed in enumerate(resampled_groundspeeds):
        bootstrapped_point = (resampled_windspeeds[index],resampled_groundspeed)
        total_count +=1.
        if ask_if_point_is_within_model_patch(bootstrapped_point, vertices_as_tuples): #if true,
            in_patch_count +=1.
    fractions_inside_patch.append(in_patch_count/float(total_count))

in_patch_count = 0
for index, groundspeed in enumerate(groundspeeds):
    data_point = (windspeeds[index],groundspeed)
    total_count +=1.
    if ask_if_point_is_within_model_patch(data_point, vertices_as_tuples): #if true,
        in_patch_count +=1.
fraction_of_field_data_inside_patch = in_patch_count/float(len(windspeeds))

# bootstrapped_bools = []
# for fraction in fractions_inside_patch:
#     if fraction >= fraction_of_field_data_inside_patch:
#         bootstrapped_bools.append(1)
#     else:
#         bootstrapped_bools.append(0)
# summary_statistic = np.sum(bootstrapped_bools)#/float(len(bootstrapped_bools))
# print ('Over 10,000 iterations, on %d iterations bootstrapped datasets contain a larger fraction of in-model-patch points than does the original model.' %(summary_statistic))

bootstrapped_fractions_inside_patch=[]
bootstrapping_iteration_number = 20000
for i in range (bootstrapping_iteration_number):
    points = [(windspeeds[x], groundspeeds[x]) for x in range(len(windspeeds))]
    resampled_indices = np.random.choice(range(len(points)), len(points), replace=True)
    resampled_points = np.array(points)[resampled_indices]
    in_patch_count=0.
    total_count = 0.
    for resampled_point in resampled_points:
        total_count +=1.
        if ask_if_point_is_within_model_patch(resampled_point, vertices_as_tuples): #if true,
            in_patch_count +=1.
    bootstrapped_fractions_inside_patch.append(in_patch_count/float(total_count))


fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(1,1,1)
ax.set_ylabel('count', fontsize = 14)
ax.set_xlim([0,1.0])
ax.set_ylim([0,8000])
ax.set_xlabel('fraction of points falling within model boundaries', fontsize = 16)
ax.hist(bootstrapped_fractions_inside_patch, color ='black', ec='white', label = 'bootstrapped data points, 20k iterations', zorder = 1)
ax.hist(fractions_inside_patch, color = [0,0,0,0.2], ec="black", label = 'shuffled without replacement, 20k iterations', zorder = 100)
# for tick in ax.xaxis.get_major_ticks():
#     tick.label.set_fontsize(14)
# for tick in ax.yaxis.get_major_ticks():
#     tick.label.set_fontsize(14)

legend = ax.legend(loc='upper left', shadow=False)
# ax.axvline(fraction_of_field_data_inside_patch, linewidth = 2, color = 'k')
# plt.title(('Over 10,000 iterations, on %d iterations bootstrapped datasets \n contain a larger fraction of in-model-patch points than does the original model.') %(summary_statistic), fontsize = 9)
adjust_spines(ax, spines = ['left','bottom'])
plt.savefig('./bootstrapped_20000.svg', transparent = True)
plt.show()
