import matplotlib
import matplotlib.pyplot as plt
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
    masses['_6_']   = [32            ,16.95   ,2.0] #Double peak?
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

    #Offset calculated for water
    p1 = tof_helpers.extrapolate()
    modelfunc = lambda p, x: p[0]*x**p[1]
    offset_error = 12.7775 - modelfunc(p1,18.0105647)
    modelfunc = lambda p, x: p[0]*x**p[1] + offset_error

    xvalues = np.arange(0,80,0.1)
    #yvalues = p1[0]*xvalues**p1[1]
    yvalues = modelfunc(p1,xvalues)
    
    fig = plt.figure()
    axis = fig.add_subplot(2,1,1)
    axis.plot(mass_ref[:,0], mass_ref[:,1],'ro')
    axis.plot(xvalues, yvalues,'b-')

    axis.set_ylabel('Flight Time / $\mu$s')
    axis.set_xlabel('Molecular mass / amu')

    axis = fig.add_subplot(2,1,2)
    axis.plot(mass_ref[:,0], (mass_ref[:,1]-modelfunc(p1,mass_ref[:,0]))*1000,'ro')
    axis.errorbar(mass_ref[:,0], (mass_ref[:,1]-modelfunc(p1,mass_ref[:,0]))*1000, yerr=mass_ref[:,2]*2,fmt='o')
    axis.set_xlim(0,80)
    axis.set_xlabel('Molecular mass / amu')
    axis.set_ylabel('Model error / ns')
    plt.show()
