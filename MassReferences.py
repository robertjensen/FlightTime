import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import tof_model as tm
import tof_helpers
matplotlib.rc('text',usetex=True) # Magic fix for the font warnings

def MassReferences():
    #Spectrum: 245
    masses = {}
    masses['_28_']  = [69            ,24.859 ,15.0]
    masses['_27_']  = [68            ,24.665 ,15.0]
    masses['_26_']  = [67            ,24.491 ,15.0]
    masses['_25_']  = [64            ,23.925  ,5.0]
    masses['_24_']  = [60            ,23.181 ,10.0]
    masses['_23_']  = [58            ,22.8   ,10.0]
    masses['_22_']  = [57            ,22.606 ,10.0]
    masses['_21_']  = [56            ,22.407 ,10.0]
    masses['_20_']  = [55            ,22.203 ,10.0]
    masses['_19_']  = [54            ,22.0   ,15.0]
    masses['_18_']  = [48            ,20.744  ,6.0]
    masses['_17_']  = [46            ,20.317  ,3.0]
    masses['_16_']  = [45            ,20.095  ,2.0]
    masses['_15_']  = [44            ,19.871  ,0.5]
    masses['_14_']  = [43            ,19.6495 ,1.0]
    masses['_13_']  = [42            ,19.4305 ,3.0]
    masses['_12_']  = [42            ,19.422  ,3.0]
    masses['_11_']  = [41            ,19.198  ,3.0]
    masses['_10_']  = [40            ,18.96   ,4.0]
    masses['_9_']   = [40            ,18.947  ,2.0]
    masses['_8_']   = [39            ,18.725  ,3.0]
    masses['_7_']   = [36            ,17.986  ,4.0]
    masses['_6_']   = [32            ,16.9805 ,2.0] #Double peak?
    masses['O2']    = [31.9898292    ,16.9705 ,0.5]
    masses['_5_']   = [31            ,16.713  ,2.0] 
    masses['_4_']   = [30            ,16.4395 ,1.0] 
    masses['_3_']   = [29            ,16.166  ,1.0] 
    masses['N2']    = [28            ,15.889  ,0.5] 
    masses['_2_']   = [27            ,15.6075 ,0.5] 
    masses['_1_']   = [26            ,15.3195 ,0.5] 
    masses['H2018'] = [20            ,13.458  ,0.5] #Not 100% sure....
    masses['HD0']   = [19            ,13.123  ,0.5] #Not 100% sure....
    masses['H2O']   = [18.0105647    ,12.7775 ,0.5]
    masses['NH3']   = [17.0265491    ,12.426  ,0.5]
    masses['OH']    = [17.0027397    ,12.4175 ,0.5]
    masses['NH2']   = [16.0187241    ,12.058  ,0.5]
    masses['O']     = [15.9949146    ,12.049  ,0.5]
    masses['NH']    = [15.010899     ,11.6818 ,1.0] #Not 100% sure....
    masses['N']     = [14.003074     ,11.287  ,2.5] #Not 100% sure....
    masses['C']     = [12.0          ,10.4585 ,1.5] #Not 100% sure....
    masses['H2']    = [2.01565006    ,4.386   ,0.5]
    masses['H']     = [1.00782503207 ,3.149   ,0.5]

    mass_ref = np.zeros((len(masses),3))
    i = 0
    for key in masses:
        mass_ref[i,0] = masses[key][0]
        mass_ref[i,1] = masses[key][1]
        mass_ref[i,2] = masses[key][2]
        i = i+1

    return mass_ref

#When run as a stand-alone program, the reference file will try to compare
#itself against the model
if __name__ == '__main__':
    mass_ref = MassReferences()

    #These values are corresponding to the reference set conditions
    tm.Voltages['pulse'] = 800
    tm.Voltages['liner'] = -2321.62
    tm.Voltages['R1'] = -702.699
    tm.Voltages['R2'] = 1119.72

    #Offset calculated for hydrogen
    p1 = tof_helpers.extrapolate()
    modelfunc = lambda p, x: p[0]*x**p[1]
    offset_error = 3.149 - modelfunc(p1,1.00782503207)

    modelfunc = lambda p, x: p[0]*x**p[1] + offset_error
    mass_modelfunc = lambda p,x: ((x-offset_error)/p[0])**(1.0/p[1])
    
    xvalues = np.arange(0,80,0.1)
    #yvalues = p1[0]*xvalues**p1[1]
    yvalues = modelfunc(p1,xvalues)
    
    fig = plt.figure()
    fig.subplots_adjust(hspace=0.05)
    ratio = 1
    fig_width = 10
    fig_width = fig_width /2.54     # width in cm converted to inches
    fig_height = fig_width*ratio
    fig.set_size_inches(fig_width,fig_height)
    gs = gridspec.GridSpec(4, 1)

    axis = plt.subplot(gs[0:2, 0])
    #axis = fig.add_subplot(2,1,1)
    axis.plot(xvalues, yvalues,'r-')
    axis.plot(mass_ref[:,0], mass_ref[:,1],'bo',markersize=2)
    axis.set_ylabel('Flight Time / $\mu$s', fontsize=8)
    #axis.set_xlabel('Mass / amu', fontsize=8)
    axis.set_xlabel('')
    axis.set_xticklabels([])
    axis.set_xlim(0,75)
    axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)
    
    #axis = fig.add_subplot(2,1,2)
    axis = plt.subplot(gs[2, 0])
    #axis.plot(mass_ref[:,0], (mass_ref[:,1]-modelfunc(p1,mass_ref[:,0]))*1000,'ro',markersize=1.5)
    axis.errorbar(mass_ref[:,0], (mass_ref[:,1]-modelfunc(p1,mass_ref[:,0]))*1000, yerr=mass_ref[:,2],fmt='o',markersize=2)
    axis.set_xlim(0,75)
    #axis.set_ylim(-20,20)
    axis.set_xlabel('Mass / amu', fontsize=8)
    axis.set_ylabel('Error / ns', fontsize=8)
    axis.set_yticks([-10,0,10,20,30])
    axis.set_xlabel('')
    axis.set_xticklabels([])
    axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)
    
    axis = plt.subplot(gs[3, 0])
    #axis.plot(mass_ref[:,0], (mass_ref[:,1]-modelfunc(p1,mass_ref[:,0]))*1000,'ro',markersize=1.5)
    axis.errorbar(mass_ref[:,0], 1000*abs((mass_ref[:,0]-mass_modelfunc(p1,mass_ref[:,1]))), yerr=1000*abs(mass_modelfunc(p1,mass_ref[:,1])-mass_modelfunc(p1,mass_ref[:,1]-mass_ref[:,2]/1000)),fmt='o',markersize=2)

    axis.set_xlim(0,75)
    #axis.set_ylim(-199,199)
    axis.set_xlabel('Mass / amu', fontsize=8)
    axis.set_ylabel('Error / milliamu', fontsize=8)
    axis.set_yticks([-50,0,50,100,150])
    axis.tick_params(direction='in', length=2, width=1, colors='k',labelsize=8,axis='both',pad=3)

    
    plt.savefig('reference_plot.png',dpi=300)
    #plt.show()
