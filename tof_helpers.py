import scipy as sp
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy import optimize

import tof_model as tm



def extrapolate():
    times = []
    masses = []
    for mass in range(1,20):
        times.append(tm.flight_time(mass))
        masses.append(mass)


    # Fit the first set
    fitfunc = lambda p, x: p[0]*x**0.5 + p[1] # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [1, 0,] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(masses, times))

    time = sp.linspace(1, 50, 100)
    plt.plot(masses, times, "ro", time, fitfunc(p1, time), "r-") # Plot of the data and the fit


    # Legend the plot
    plt.title("Oscillations in the compressed trap")
    plt.xlabel("time [ms]")
    plt.ylabel("displacement [um]")
    plt.legend(('x position', 'x fit', 'y position', 'y fit'))

    #ax = axes()

    #text(0.8, 0.07,
    #     'x freq :  %.3f kHz' % (1/p1[1]),
    #     fontsize=16,
    #     horizontalalignment='center',
    #     verticalalignment='center',
    #     transform=ax.transAxes)

    plt.show()


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



