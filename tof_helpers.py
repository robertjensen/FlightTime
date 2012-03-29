import scipy as sp
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy import optimize
import tof_model as tm

mpl.rc('text',usetex=True) # Magic fix for the font warnings


def extrapolate(start=1,end=100,step=10,plot=False):
    """
    Uses the physical model on a few (currently 10) masses
    to create a fitting-expression for the flight-time as
    a function of mass.
    Currently the function takes no arguments, but obviously
    it will be nice to be able to set the range and number
    of masses used in the fit
    Args:
        start: First mass in the fit. Default=5
        end: Last mass in the fit. Default = 100
        step: Stepsize. Default = 10
        plot: If true, a plot showing the fit will be produces. Default=False
    Returns:
        The two coefficients for the extrapolation
    Raises:
    """

    times = []
    masses = []
    for mass in range(start,end,step):
        ft = tm.flight_time(mass)
        times.append(ft[0]*1e6)
        masses.append(mass)

    times = sp.array(times)
    masses = sp.array(masses)

    # Fit the first set
    fitfunc = lambda p, x: p[0]*x**p[1] # Target function
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    p0 = [1, 0.5] # Initial guess for the parameters
    p1, success = optimize.leastsq(errfunc, p0[:], args=(masses, times))

    if plot:
        fig = plt.figure()
        #Plot the fit and the data-points
        axis = fig.add_subplot(2,1,1)

        mass_axis = sp.linspace(0, end, 1000)
        # Plot of the data and the fit
        axis.plot(masses, times, 'ro')
        axis.plot(mass_axis, fitfunc(p1, mass_axis), 'r-')
        axis.set_xlabel("Mass [amu]")
        axis.set_ylabel("Expected flighttime (microseconds)")

        #Plot the error-function
        axis = fig.add_subplot(2,1,2)
        axis.plot(masses, (fitfunc(p1, masses)-times)*1000, 'ro')
        axis.set_xlabel("Mass [amu]")
        axis.set_ylabel("Fitting-error / ns")    
        plt.show()
    
    return p1

def draw_trajectory(mass):
    """
    Create a graph for expected flighttimes
    
    Args:
        mass: The mass to be calculated
    
    Returns:
    
    Raises:
    """
    t,res =  tm.flight_time(mass,0)
    t,res_slow =  tm.flight_time(mass,tm.SLOW_POS)
    t,res_fast =  tm.flight_time(mass,tm.FAST_POS)
    fig = plt.figure()
    ax11 = fig.add_subplot(111)
    ax11.plot(res['time'],res['pos'],'r-')
    ax11.plot(res_slow['time'],res_slow['pos'],'g-')
    ax11.plot(res_fast['time'],res_fast['pos'],'b-')
    ax11.set_xlabel('Time / $\mu$s')
    ax11.set_ylabel('Position / cm')
    plt.savefig('Trajectory.png',dpi=300)





def print_flighttimes(html, print_values,export_figure):
    """
    Print flight times of various masses. This is done by
    calling the extrapolate function and then use the
    returned expression to calculate the values
    Args:
        html: If true, the output will be formatted for a web-browser
        print_values...
        export_figure...
        
    Returns:
    
    Raises:
    """
    flight_times = []
    masses = []
    coeff = extrapolate()
    for mass in range(1,50): 
        res = coeff[0] * (mass ** coeff[1])
        if print_values:
            #print "Flight time of {}: {:.3f} microsceonds".format(mass,res[0]*1e6)
            print "{0} {1:.3f}".format(mass,res)
            if html:
                print "<br>"
        masses.append(mass)
        flight_times.append(res)
    if export_figure:
        fig = plt.figure()
        ax11 = fig.add_subplot(111)
        ax11.plot(masses,flight_times,'r-')
        ax11.set_xlabel('Mass / AMU')
        ax11.set_ylabel('Flight Time / micro seconds')
        plt.savefig('Masses.png')



