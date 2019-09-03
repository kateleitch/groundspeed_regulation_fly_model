from __future__ import print_function
import numpy as np
import os, sys
import matplotlib
import matplotlib.pyplot as plt

trap_number = 10
trap_angle_list = np.linspace(0,np.pi*2, trap_number, endpoint=False)
trap_names = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
trap_dictionary = {}
for i in range (trap_number):
    trap_dictionary[str(trap_angle_list[i])] = {'headings_of_trapped_flies':[]}

assumed_effective_trap_width = 1 # in meters
assumed_distance_to_trap = 1000 # in meters
trap_angular_width = assumed_effective_trap_width/(2*np.pi*assumed_distance_to_trap) #a width for each trap so they can actually collect some nonzero number of flies.
# fraction_of_trap_circumference_to_sample = 0.001
# trap_angular_width = fraction_of_trap_circumference_to_sample/trap_number*(np.pi/180) #
fly_number = 40000

forward_airspeed_limit = 2.0 #meters per second.
reverse_airspeed_limit = -0.5 #meters per second.
preferred_groundspeed_along_body_axis = 1.5 #meters per second.

wind_direction_list = [0.05, 1.05*np.pi/2., 3.05*np.pi/2.] #in radians, the direction TO WHICH the wind is blowing. NOTE THAT THIS IS pi OFF MY TYPICAL CONVENTION
wind_speed_list = [0.52, 1.02, 1.52, 2.02, 2.52, 3.02] #in meters per second
fly_headings = np.linspace(0, np.pi*2, fly_number)
#fly_headings = [0.000000000001] # a single test fly, heading almost perfectly straight east

fig = plt.figure(figsize=(8,8))
ax = plt.subplot(1,1,1)
for wind_dir in wind_direction_list:
    for wind_speed in wind_speed_list:
        parallel_component_list = [np.cos(wind_dir - heading)*wind_speed for heading in fly_headings] # magnitude of wind in direction parallel to heading
        perp_component_list     = [np.abs(np.sin(wind_dir - heading))*wind_speed for heading in fly_headings] # magnitude of wind in direction perpendicular to heading
        fly_regulated_parallel_component_list = np.zeros(len(parallel_component_list))
        for index, par in enumerate(parallel_component_list):
            #print ('parallel component: ' +str(par))
            if par + reverse_airspeed_limit >= preferred_groundspeed_along_body_axis: # fly cannot "brake" enough to achieve preferred groundspeed
                fly_regulated_parallel_component_list[index] = par + reverse_airspeed_limit # fly brakes as much as it can
            elif par + forward_airspeed_limit < preferred_groundspeed_along_body_axis: # fly cannot thrust enough to achieve preferred groundspeed
                fly_regulated_parallel_component_list[index] = par + forward_airspeed_limit # fly thrusts as much as it can
            else:
                fly_regulated_parallel_component_list[index] = preferred_groundspeed_along_body_axis

            reg_par = fly_regulated_parallel_component_list[index]
            #print ('regulated parallel component: ' +str(reg_par))
            #print ('perpendicular component: ' + str(perp_component_list[index]))
            y_component_of_track = reg_par*np.sin(fly_headings[index]) + perp_component_list[index]*np.abs(np.sin(fly_headings[index]+np.pi/2.))  #in cartesian coordinates
            #print ('y component of track: ' +str(y_component_of_track))
            x_component_of_track = reg_par*np.cos(fly_headings[index]) + perp_component_list[index]*np.abs(np.cos(fly_headings[index]+np.pi/2.))  #in cartesian coordinates
            #print ('x component of track: ' +str(x_component_of_track))
            track_angle = np.arctan2(y_component_of_track,x_component_of_track)
            track_angle = (track_angle+2*np.pi)%(2*np.pi)
            for angle_to_trap in trap_angle_list:
                if (angle_to_trap -trap_angular_width/2.) <= track_angle <= (angle_to_trap + trap_angular_width/2.):
                    trap_dictionary[str(angle_to_trap)]['headings_of_trapped_flies'].append(fly_headings[index])
                    ax.scatter(   np.cos(np.abs(wind_dir - track_angle))*wind_speed   ,    np.sqrt(y_component_of_track**2 + x_component_of_track**2), color = [0,0,0,0.2])
#print (trap_dictionary)
ax.set_ylabel('groundspeed along trajectory, m/s')
ax.set_xlabel('windspeed along trajectory, m/s')
plt.show()

### I have the strong sense of having a sign error somewhere up there!! need to walk through code with someone else ideally
