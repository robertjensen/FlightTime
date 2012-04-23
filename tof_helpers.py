import scipy as sp
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
from scipy import optimize
from scipy import interpolate
import tof_model as tm

mpl.rc('text',usetex=True) # Magic fix for the font warnings

def powerFit(x,y,FitExponent=True):
    """
    Fits the x and y data to an expression of the form
    y = a*x^b
    
    Args:
        x: The x-data points
        y: The y-data points
        FitExponent: If False, b wil be fixed to b=0.5
    Return:
        Two-element array with the values of a and b
    Raises:
        ...
    """
    
    if FitExponent:
        fitfunc = lambda p, x: p[0]*x**p[1] # Target function
        p0 = [1, 0.5] # The initial guess for the parameters
    else:
        fitfunc = lambda p, x: p[0]*x**0.5
        p0 = [1] 
    errfunc = lambda p, x, y: fitfunc(p, x) - y # Distance to the target function
    
    p1, success = optimize.leastsq(errfunc, p0[:], args=(masses, times))
    return p1


def extrapolate(start=1,end=100,step=10,plot=False):
    """
    Uses the physical model on a few (currently 10) masses
    to create a fitting-expression for the flight-time as
    a function of mass.
    Args:
        start: First mass in the fit. Default=5
        end:   Last mass in the fit. Default = 100
        step:  Stepsize. Default = 10
        plot:  If true, a plot showing the fit will be produces. Default=False
    Returns:
        The two coefficients for the extrapolation
    Raises:
        ValueError: Raised on non-legal input parameters
    """
    
    if (start<1) or (end<start):
        raise ValueError

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
    fig.subplots_adjust(bottom=0.15) # Make room for x-label
    ratio = 0.6
    fig_width = 8.5
    fig_width = fig_width /2.54     # width in cm converted to inches
    fig_height = fig_width*ratio
    fig.set_size_inches(fig_width,fig_height)    
    
    ax11 = fig.add_subplot(111)
    ax11.plot(res['time'],res['pos'],'r-', linewidth=0.7)
    ax11.plot(res_slow['time'],res_slow['pos'],'g-', linewidth=0.7)
    ax11.plot(res_fast['time'],res_fast['pos'],'b-', linewidth=0.7)
    ax11.set_xlabel('Time / $\mu$s', fontsize=8)
    ax11.set_ylabel('Position / cm', fontsize=8)
    ax11.set_xlim(0,22)
    ax11.set_ylim(-2,120) 
    ax11.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)
    
    ins_plt = plt.axes([0.4,0.23,0.4,0.175])
    #plt.setp(ins_plt)

    slow_interp = interpolate.interp1d(res_slow['time'],res_slow['pos'], bounds_error=False)
    fast_interp = interpolate.interp1d(res_fast['time'],res_fast['pos'], bounds_error=False)
    zero = [0]*len(res['time'])
    
    ins_plt.plot(res['time'],slow_interp(res['time'])-res['pos'],'g-', linewidth=0.7)
    ins_plt.plot(res['time'],fast_interp(res['time'])-res['pos'],'b-', linewidth=0.7)
    ins_plt.plot(res['time'],zero,'r-', linewidth=0.5)
    ins_plt.set_ylabel('$\Delta$pos / cm', fontsize=7)
    ins_plt.set_yticks([])
    ins_plt.tick_params(direction='in', length=2, width=1, colors='k',labelsize=7,axis='both',pad=3)
    ins_plt.set_xlim(0,22)

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


