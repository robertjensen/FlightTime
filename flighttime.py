
#pos=0 is defined to be at the center axis of the incoming ions
def field(pos):
    #dR1ZGap = 80 # Not correct distance

    #Measured from CAD drawing
    #A1-A2: 1.333cm
    #A1-A3: 1.333cm

    Params = []
    #Params.append((-2.5,Pulse_Voltage))    #A1
    #Params.append((2.5,0))                 #A2
    Params.append((-0.635,Pulse_Voltage))   #A1
    Params.append((0.635,0))                #A2
    Params.append((1.9685,Liner_Voltage))   #A3
    Params.append((95.235,Liner_Voltage))   #Liner grid
    Params.append((96.390,R1_Voltage))      #R1
    Params.append((110.81,R2_Voltage))      #R2
    Params.append((10000,R2_Voltage))       #This field extends to infinity

    i = 0
    while Params[i][0] < pos:
        i = i+1
    field = (Params[i][1] - Params[i-1][1]) / (Params[i][0] - Params[i-1][0])

    return (field,Params[i][0],Params[i-1][0]) #Tuple containing field (Volt / cm) and
                                               #distance until it needs to be checked again in either direction

# F = q*E
# A = F / m
def acceleration(field,mass):
    elementary_charge = -1.602e-19 # Unit, columb
    force = field * elementary_charge * 100 # Unit, N, factor of 100 compensating for field unit of V/cm
    acc = force / (mass * 1.6605e-27) #Unit, m/s, mass unit AMU, thus compensating factor
    return acc



def flight_time(mass,pos=0):
    t = 0
    dt = 1e-10
    dT = dt
    v = 1e-10 # Make sure v is positive from the beginning
    i = 0
    valid_until = -100000
    t_values = [] #Aaarrgghhh
    v_values = [] #Aaaaarrgggghhhh
    pos_values = [] #This need to be done as a single list of tuples!!!!
    while (((pos < 110.8) & (v>0)) | ((pos > 37.167) & (v<0))):
        if v>0:
            if pos > valid_until:
                Field = field(pos)
                E = Field[0]
                valid_until = Field[1]
                A = acceleration(E,mass)
                dT = dt
            else:
                if ((pos+500*v*dT) < valid_until) & (E == 0):
                    dT = 50 * dt
        else:
            if pos < valid_until:
                Field = field(pos)
                E = Field[0]
                valid_until = Field[2]
                A = acceleration(E,mass)
                dT = dt
            else:
                if (pos > 29) & (E == 0): # BVAADDRRRR!!!! HACK!!!!
                    dT = 50 * dt

        v = v + A*dT
        pos = pos + (v*dT) * 100 # pos is in cm
        t = t+dT
        i = i+1
        if (i%100 == 0):
            t_values.append(t*1e6)
            pos_values.append(pos)
            v_values.append(v)
            #print pos
            #print E
            #print field(pos)
            #print t
            #print pos
            #print A
            #print v
            #print "--"


    s1 =  "Time {0:.3f} microseconds".format(t*1e6)
    s2 =  "Speed: {0:.2f} km/s".format(v / 1000)
    s3 =  "Distance error: {0}".format(pos-107.5)
    status_text = s1 + "\n" + s2 + "\n" + s3
    return (t,status_text,t_values,pos_values,v_values)


"""Create a graph for expected flighttimes"""
def draw_trajectory(mass):
    res =  flight_time(mass,0)
    res_slow =  flight_time(mass,SLOW_POS)
    res_fast =  flight_time(mass,FAST_POS)
    fig = plt.figure()
    ax11 = fig.add_subplot(111)
    #ax11.plot(res[3],res[2],res_slow[3],res_slow[2],res_fast[3],res_fast[2],'r-','b-','g-')
    ax11.plot(res[3],res[2],'r-')
    ax11.set_xlabel('Position / cm')
    ax11.set_ylabel('Time / micro seconds')
    plt.savefig('Trajectory.png')




"""Print flight times of various masse"""
def print_flighttimes(html, print_values,export_figure):
    flight_times = []
    masses = []
    for mass in range(1,50): 
        res = flight_time(mass)
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

import sys
#import argparse
import optparse
import scipy as sp
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt



parser = optparse.OptionParser('Calculates expected flighttime in the TOF')
parser.add_option('--html', action="store_true", default=False, help='Adds html line breaks to the text output')
parser.add_option('--liner', '-L', action="store", default=-2000, type=int, help='Liner Voltage')
parser.add_option('--pulse', '-P', action="store", default=400, type=int, help='Pulse Voltage')
parser.add_option('--R1', action="store", default=-1, type=int, help='Voltage at R1')
parser.add_option('--R2', action="store", default=-1, type=int, help='Voltage at R2')
(options, args) = parser.parse_args()


#Global variables
SLOW_POS =  0.62
FAST_POS = -0.62

Pulse_Voltage = options.pulse
Liner_Voltage = options.liner
R1_Voltage = options.R1
R2_Voltage = options.R2

R1_Voltage = -432
R2_Voltage = 1791


if R2_Voltage < 0: # Liniar mode
    R1_Voltage = Liner_Voltage
    R2_Voltage = Liner_Voltage



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

