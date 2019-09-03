from __future__ import print_function
import numpy as np
import os, sys
import matplotlib
import matplotlib.pyplot as plt
import random

trap_number = 10
trap_angle_list = np.linspace(0,np.pi*2, trap_number, endpoint=False)
trap_names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

assumed_effective_trap_width = 0.1 # in meters
assumed_distance_to_trap = 1000 # in meters
trap_angular_width = assumed_effective_trap_width/(2*np.pi*assumed_distance_to_trap)*  (2*np.pi) #a width for each trap so they can actually collect some nonzero number of flies.
print ('trap angular width assumed to be: ' +str(trap_angular_width*180/np.pi)+' degrees')
# fraction_of_trap_circumference_to_sample = 0.001
# trap_angular_width = fraction_of_trap_circumference_to_sample/trap_number*(np.pi/180) #
fly_number = 80000

preferred_groundspeed_along_body_axis = 1.5 #meters per second.
forward_airspeed_limit = preferred_groundspeed_along_body_axis + 0.3 #2.0 #meters per second.
reverse_airspeed_limit = -0.2 #meters per second.

wind_direction_list = np.linspace(0,2*np.pi,17)#in radians, the direction TO WHICH the wind is blowing. NOTE THAT THIS IS pi OFF MY TYPICAL CONVENTION
wind_speed_list = [0.51, 0.79, 1.01, 1.52, 1.64, 2.4, 3.11] #in meters per second
weight_of_perpendicular_slip = 0.1
fly_headings = list(np.linspace(0, np.pi*2, fly_number))
#fly_headings = [0] # a single test fly, heading straight east

fig = plt.figure(figsize=(8,8))
ax = plt.subplot(1,1,1)
# ax2 = plt.subplot(2,1,2)
for wind_dir in wind_direction_list:
    for wind_speed in wind_speed_list:
        trap_dictionary = {}
        for i in range (trap_number):
            trap_dictionary[str(trap_angle_list[i])] = {'headings_of_trapped_flies':[], 'groundspeed_along_trajectory':[], 'windspeed_along_trajectory':[]}

        parallel_component_list = [np.cos(wind_dir - heading)*wind_speed for heading in fly_headings] # magnitude of wind in direction parallel to heading [-wind_speed,wind_speed]
        perp_component_list     = [np.abs(np.sin(wind_dir - heading))*wind_speed*weight_of_perpendicular_slip for heading in fly_headings] # magnitude of wind in direction perpendicular to heading; [0,wind_speed]
        fly_regulated_parallel_component_list = np.zeros(len(parallel_component_list))
        for index, par in enumerate(parallel_component_list):
            #print ('parallel component: ' +str(par))
            if par + forward_airspeed_limit < 0:
                #print ('maintaining this heading is not possible in this wind')
                parallel_component_list.pop(index)
                perp_component_list.pop(index)
                fly_headings.pop(index)
                continue

            if par + reverse_airspeed_limit >= preferred_groundspeed_along_body_axis: # fly cannot "brake" enough to achieve preferred groundspeed
                fly_regulated_parallel_component_list[index] = par + reverse_airspeed_limit # fly brakes as much as it can
            elif (par + forward_airspeed_limit) < preferred_groundspeed_along_body_axis: # fly cannot thrust enough to achieve preferred groundspeed
                fly_regulated_parallel_component_list[index] = par + forward_airspeed_limit # fly thrusts as much as it can
            else:
                fly_regulated_parallel_component_list[index] = preferred_groundspeed_along_body_axis

            reg_par = fly_regulated_parallel_component_list[index]

            compass_y_of_parallel_component = reg_par*np.sin(fly_headings[index])
            compass_x_of_parallel_component = reg_par*np.cos(fly_headings[index])

            if (wind_dir - fly_headings[index] +2*np.pi)%(2*np.pi) <= np.pi:
                angle_of_perpendicular_component = fly_headings[index] + np.pi/2.
            else:
                angle_of_perpendicular_component = fly_headings[index] - np.pi/2.
            compass_y_of_perpendicular_component = perp_component_list[index]*(np.sin(angle_of_perpendicular_component))
            compass_x_of_perpendicular_component = perp_component_list[index]*(np.cos(angle_of_perpendicular_component))
            y_component_of_track =  compass_y_of_parallel_component +  compass_y_of_perpendicular_component #in cartesian coordinates
            x_component_of_track =  compass_x_of_parallel_component +  compass_x_of_perpendicular_component #in cartesian coordinates
            track_angle = np.arctan2(y_component_of_track,x_component_of_track)
            track_angle = (track_angle+2*np.pi)%(2*np.pi)
            for angle_to_trap in trap_angle_list:
                if (angle_to_trap -trap_angular_width/2.) <= track_angle <= (angle_to_trap + trap_angular_width/2.):
                    trap_dictionary[str(angle_to_trap)]['headings_of_trapped_flies'].append(fly_headings[index])
                    trap_dictionary[str(angle_to_trap)]['groundspeed_along_trajectory'].append(np.sqrt(y_component_of_track**2 + x_component_of_track**2))
                    trap_dictionary[str(angle_to_trap)]['windspeed_along_trajectory'].append(np.cos(np.abs(wind_dir - track_angle))*wind_speed)
                    #ax.scatter(np.cos(np.abs(wind_dir - track_angle))*wind_speed,    np.sqrt(y_component_of_track**2 + x_component_of_track**2), color = [0,0,0,0.1])
        for key in trap_dictionary:
            if len(trap_dictionary[key]['groundspeed_along_trajectory'])>2:
                mean_groundspeed_along_trajectory =  np.mean(trap_dictionary[key]['groundspeed_along_trajectory'])
                err_groundspeed_along_trajectory  =  np.std (trap_dictionary[key]['groundspeed_along_trajectory'])#/len(trap_dictionary[key]['groundspeed_along_trajectory'])
                mean_windspeed_along_trajectory   =  np.mean(trap_dictionary[key]['windspeed_along_trajectory'])
                err_windspeed_along_trajectory    =  np.std (trap_dictionary[key]['windspeed_along_trajectory'])#/len(trap_dictionary[key]['groundspeed_along_trajectory'])
                #print (mean_groundspeed_along_trajectory)
                ax.errorbar(mean_windspeed_along_trajectory, mean_groundspeed_along_trajectory, xerr=err_windspeed_along_trajectory, yerr = err_groundspeed_along_trajectory, fmt='o', color = 'black') #, label = key)
ax.set_ylabel('groundspeed along trajectory, m/s')
ax.set_xlabel('windspeed along trajectory, m/s')
ax.set_ylim(0, 4)
ax.axis('equal')
plt.axhline(preferred_groundspeed_along_body_axis, color = 'k', linestyle = '--')
domain = np.linspace(-1,4,500)
#[x+1 if x >= 45 else x+5 for x in l]
ax.plot(domain, domain, '--k')


plt.show()
