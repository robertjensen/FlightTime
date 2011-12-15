import sys
#import argparse
import optparse
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



#mass = 40
#mass = float(sys.argv[1])


parser = optparse.OptionParser('Calculates expected flighttime in the TOF')
parser.add_option('--html', action="store_true", default=False, help='Adds html line breaks to the text output')
parser.add_option('--liner', '-L', action="store", default=-2000, type=int, help='Liner Voltage')
parser.add_option('--pulse', '-P', action="store", default=400, type=int, help='Pulse Voltage')
parser.add_option('--R1', action="store", default=-432, type=int, help='Voltage at R1')
parser.add_option('--R2', action="store", default=1791, type=int, help='Voltage at R2')
(options, args) = parser.parse_args()

SLOW_POS =  0.62
FAST_POS = -0.62

tm.Voltages = {} # Contains all electrical values of the maching
tm.Voltages['pulse'] = options.pulse
tm.Voltages['liner'] = options.liner
tm.Voltages['R1'] = options.R1
tm.Voltages['R2'] = options.R2

if tm.Voltages['R2'] <= 0: # Liniar mode
    tm.Voltages['R1'] = Voltages['R1'] = Voltages['liner']



""" Under here starts random experimentation that needs to be cleaned up """


print_flighttimes(False,True,False)

#R1_Voltage = 0
#R2_Voltage = 0


"""
flight_times = []
positions = []
mass = 28
for pos in range(int(FAST_POS*1000),int(SLOW_POS*1000)):
    res = flight_time(mass,pos/1000.0)
    positions.append(pos/1000.0)
    flight_times.append(res[0]*1e6)

fig = plt.figure()
ax11 = fig.add_subplot(111)
ax11.plot(positions,flight_times,'r-')
ax11.set_xlabel('Start position')
ax11.set_ylabel('Flight Time / micro seconds')
plt.savefig('Peak-width.png')
"""


#draw_trajectory(28.006)

#print_flighttimes(options.html,True,True)
#print_flighttimes(options.html,False,False)

#### Implement peak-width analysis!!!
# Should be easy...


#mass = 27.995
#res = flight_time(mass)
#print "Center ions {0}: {1:.3f} microsceonds".format(mass,res[0]*1e6)

#mass = 28.006
#res2 = flight_time(mass)
#print "Center ions {0}: {1:.3f} microsceonds".format(mass,res2[0]*1e6)

#print "Difference: {0}: ".format((res2[0]-res[0])*1e9)


#res = flight_time(mass,0.63)
#print "Slowest ions {0}: {1:.3f} microsceonds".format(mass,res[0]*1e6)
#res = flight_time(mass,-0.63)
#print "Fastest ions {0}: {1:.3f} microsceonds".format(mass,res[0]*1e6)

#R1_Voltage = 0
#R2_Voltage = 0
#res = flight_time(mass)
#print "Center ions {0}: {1:.3f} microsceonds".format(mass,res[0]*1e6)
#res = flight_time(mass,0.63)
#print "Slowest ions {0}: {1:.3f} microsceonds".format(mass,res[0]*1e6)
#res = flight_time(mass,-0.63)
#print "Fastest ions {0}: {1:.3f} microsceonds".format(mass,res[0]*1e6)

