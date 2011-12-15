import scipy as sp
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

import tof_model as tm

def draw_trajectory(mass):
    """
    Create a graph for expected flighttimes
    
    Args:
        mass: The mass to be calculated
    
    Returns:
    
    Raises:
    """
    res =  tm.flight_time(mass,0)
    res_slow =  tm.flight_time(mass,SLOW_POS)
    res_fast =  tm.flight_time(mass,FAST_POS)
    fig = plt.figure()
    ax11 = fig.add_subplot(111)
    #ax11.plot(res[3],res[2],res_slow[3],res_slow[2],res_fast[3],res_fast[2],'r-','b-','g-')
    ax11.plot(res[3],res[2],'r-')
    ax11.set_xlabel('Position / cm')
    ax11.set_ylabel('Time / micro seconds')
    plt.savefig('Trajectory.png')





def print_flighttimes(html, print_values,export_figure):
    """
    Print flight times of various masse
    Args:
        html: If true, the output will be formatted for a web-browser
        print_values...
        export_figure...
        
    Returns:
    
    Raises:
    """
    flight_times = []
    masses = []
    for mass in range(1,50): 
        res = tm.flight_time(mass)
        if print_values:
            #print "Flight time of {}: {:.3f} microsceonds".format(mass,res[0]*1e6)
            print "{} {:.3f}".format(mass,res[0]*1e6)
            if html:
                print "<br>"
        masses.append(mass)
        flight_times.append(res[0]*1e6)
    if export_figure:
        fig = plt.figure()
        ax11 = fig.add_subplot(111)
        ax11.plot(masses,flight_times,'r-')
        ax11.set_xlabel('Mass / AMU')
        ax11.set_ylabel('Flight Time / micro seconds')
        plt.savefig('Masses.png')



