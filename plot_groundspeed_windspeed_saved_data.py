from __future__ import print_function
import numpy as np
import os, sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import random
import json
import seaborn as sns

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

def draw_wind_and_traject_vectors(ax_handle, wind_vector,perp_vector, par_vector,heading_unit_vector, trajectory_vector, draw_legend, graph_number):
    l = 100
    if draw_legend:
        l = 0
    ax_handle.plot(np.linspace(0,wind_vector[0],l),np.linspace(0,wind_vector[1],l), 'deepskyblue', linewidth = 2, label = 'wind')
    ax_handle.scatter(wind_vector[0], wind_vector[1], s = 15, color = 'deepskyblue')
    ax_handle.plot(np.linspace(0,perp_vector[0],l),np.linspace(0,perp_vector[1],l), 'darkturquoise', linewidth = 2,label = 'wind perp')
    ax_handle.scatter(perp_vector[0], perp_vector[1], s = 15, color = 'darkturquoise')
    ax_handle.plot(np.linspace(0,par_vector[0],l),np.linspace(0,par_vector[1],l), 'cadetblue',linewidth = 2,label = 'wind par')
    ax_handle.scatter(par_vector[0], par_vector[1], s = 15, color = 'cadetblue')

    ax_handle.plot(np.linspace(0,trajectory_vector[0],l),np.linspace(0,trajectory_vector[1],l), 'k', linewidth =2,label = 'trajectory')
    ax_handle.scatter(trajectory_vector[0], trajectory_vector[1], s = 15, color = 'k')
    ax_handle.plot(np.linspace(0,3*heading_unit_vector[0],l),np.linspace(0,3*heading_unit_vector[1],l), '--k',label = 'heading')
    if draw_legend:
        ax_handle.legend(fontsize = 10, loc =2)
    else:
        y_position = -1* np.sign(trajectory_vector[1])
        ax_handle.text(-1,y_position,('%.2f m/s') %(np.dot(par_vector,heading_unit_vector)/np.linalg.norm(heading_unit_vector)),color = 'cadetblue')
        ax_handle.text(-1.9,1.6,str(graph_number))
    ax_handle.set_ylim(-2.5,2.5)
    ax_handle.set_xlim(-2.5,2.5)

with open('./simulated_groundspeeds_vs_windspeeds_along_trajectories.json') as f:
    dictionary = json.load(f)
gs = gridspec.GridSpec(nrows=4, ncols=5)

fig = plt.figure(figsize=(10,8))
ax = fig.add_subplot(gs[0:4, 0:4])
ax.set_ylabel('groundspeed along trajectory, m/s')
ax.set_xlabel('windspeed along trajectory, m/s')
adjust_spines(ax, spines = ['left','bottom'])
ax.set_ylim(-0, 5)
ax.set_xlim(-2, 3)
cmap = plt.cm.viridis_r
norm = matplotlib.colors.Normalize(vmin=0 ,vmax=2.75)
#norm = matplotlib.colors.Normalize(vmin=0 ,vmax=2*np.pi)
dotcolors = plt.cm.ScalarMappable(norm, cmap)

all_windspeeds_along_trajectories=[]
all_groundspeeds_along_trajectories=[]
randomly_labeled_point_count = 0
windspeeds_to_plot = np.linspace(0.2, 2.8, 14, endpoint = True)
for windspeed in dictionary:
    for wind_dir in dictionary[windspeed]:
        try:
            all_windspeeds_along_trajectories.append(dictionary[windspeed][wind_dir]['windspeeds along trajectories'][0])
            all_groundspeeds_along_trajectories.append(dictionary[windspeed][wind_dir]['groundspeeds along trajectories'][0])
        except:
            continue
        if float(windspeed) in windspeeds_to_plot:
            trajectories = dictionary[windspeed][wind_dir]['trajectories']
            windspeeds_along_trajectories= dictionary[windspeed][wind_dir]['windspeeds along trajectories']
            groundspeeds_along_trajectories=dictionary[windspeed][wind_dir]['groundspeeds along trajectories']
            size = 15
            # if randomly_labeled_point_count < 8:
            #     if random.random() < 0.02:
            #         print ('wind blowing to '+str(float(wind_dir)/np.pi)+' pi at '+str(windspeed)+' m/s')
            #         print ('fly trajectory to: ' + str(trajectories[0]))
            #         print ('')
            #         size = 100
            #         col_num = randomly_labeled_point_count - divmod(randomly_labeled_point_count,4)[1]*divmod(randomly_labeled_point_count,4)[0]
            #         row_num = randomly_labeled_point_count - col_num
            #         print ([row_num,col_num])
            #         vector_axis = fig.add_subplot(gs[row_num,col_num])
            #         #vector_axis = fig.add_subplot(gs[randomly_labeled_point_count,4])
            #         should_we_draw_legend = False
            #         draw_wind_and_traject_vectors(ax_handle = vector_axis,
            #                                         wind_vector = dictionary[windspeed][wind_dir]['wind vectors'][0],
            #                                         perp_vector = dictionary[windspeed][wind_dir]['perp_vectors'][0],
            #                                         par_vector = dictionary[windspeed][wind_dir]['par_vectors'][0],
            #                                         heading_unit_vector =dictionary[windspeed][wind_dir]['heading_unit_vectors'][0],
            #                                         trajectory_vector =dictionary[windspeed][wind_dir]['trajectory_vectors'][0],
            #                                         draw_legend = should_we_draw_legend,
            #                                         graph_number = randomly_labeled_point_count+1)
            #         adjust_spines(vector_axis, spines = [])
            #         randomly_labeled_point_count+=1
            #         ax.annotate(str(randomly_labeled_point_count),
            #         xy=(windspeeds_along_trajectories[0],groundspeeds_along_trajectories[0]), xycoords='data',
            #         xytext=(windspeeds_along_trajectories[0]-0.5,groundspeeds_along_trajectories[0]+1), textcoords='data',
            #         arrowprops=dict(arrowstyle="->",
            #                     connectionstyle="arc3"))
            ax.scatter(windspeeds_along_trajectories,groundspeeds_along_trajectories, color = dotcolors.to_rgba(float(windspeed)), alpha = 0.2, s = 15,zorder=100 )
        # trajectory_minus_wind_angle = [(x - float(wind_dir)+2*np.pi)%2*np.pi for x in trajectories]
        # ax.scatter(windspeeds_along_trajectories,groundspeeds_along_trajectories, color = dotcolors.to_rgba(trajectory_minus_wind_angle), alpha = 1, s = size )
plt.sca(ax)
sns.set_style("white")
sns.kdeplot(all_windspeeds_along_trajectories, all_groundspeeds_along_trajectories, shade = True, shade_lowest = False, n_levels = 300,bw=0.035, zorder = 1)
#sns.kdeplot(all_windspeeds_along_trajectories, all_groundspeeds_along_trajectories, shade = False, shade_lowest = False, n_levels = 10,zorder = 1)

legend_axis = fig.add_subplot(gs[1,0])
draw_wind_and_traject_vectors(ax_handle = legend_axis,
                                wind_vector = [0,0],
                                perp_vector = [0,0],
                                par_vector = [0,0],
                                heading_unit_vector =[0,0],
                                trajectory_vector =[0,0],
                                draw_legend = True,
                                graph_number = 0)
adjust_spines(legend_axis, spines = [])
plt.savefig('./modeled_groundspeed_vs_windspeed_field_patch_fullest_extent.svg', transparent = True)
# plt.savefig('./modeled_groundspeed_vs_windspeed_field_.png', transparent = True)
plt.show()
