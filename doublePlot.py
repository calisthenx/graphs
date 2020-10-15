
import pylab
import lmfit
import pandas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
matplotlib.rcParams['svg.fonttype'] = 'none'

def fitModel(x, a,p_sat):
    p_optical=x
    return a*p_optical/(p_sat+p_optical)   

def fitSaturation(x,y):
    from lmfit import  Model
    # Fit Model    
    fitmodel=Model(fitModel)
    a=np.max(y)
    p_sat = 4.
    pars = fitmodel.make_params()    
    pars['a'].set(value = a,)
    pars['p_sat'].set(value  = p_sat,)
    result = fitmodel.fit(y,pars,x=x) 
    return result  

def linePlotDouble(ax,x,y,y1,fit,label='',left_ticks=False):    
    myfont={'fontname':'Arial'}
    perc= r'$(\percent)$'
    n=1.
    ax.plot(x,y/n, 'o',linewidth=1, markersize=5,markerfacecolor='None',alpha=0.3,label='BG')#lw=1,color='red') 
    ax.plot(x,y1/n,'o',linewidth=1, markersize=5,markerfacecolor='lightblue',markeredgecolor='black',label='Signal')#lw=1,color='red')
    ax.plot(x,fit/n,lw=1,color='red',)
    
    if not left_ticks:
        ax.set_ylabel('Photon Counts (1/s)')
    ax.set_xlabel('Optical Power (mW)')
    ax.set_label(label)
    ax.set_title(label)
    ax.grid(True,color='grey',lw=0.2,dashes=(1,1.5))  
    ax.yaxis.tick_left()
    ax.xaxis.tick_bottom()
    ax.set_axisbelow(True)

    ax2 = ax.twiny()
    new_tick_locations = np.array([0, 5, 10])
    def tick_function(x):
        V = np.pi*0.03**2*x*1000
        return ["%.1f" % z for z in V]
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(new_tick_locations)
    ax2.set_xticklabels(tick_function(new_tick_locations))
    ax2.set_xlabel(r"Optical Power (W/cm"+r'$^2$'+')')

    if left_ticks:
        ax.grid(True)
        ax.set_yticklabels([])
        ax.grid(True)
        for tic in ax.yaxis.get_major_ticks():
            tic.tick1On = tic.tick2On = False
            tic.label1On = tic.label2On = False
    #ax.set_xticks(arange(min(x), max(x)+1, 20))
    ax.set_ylim([-1,45])
    ax.legend(loc='top right')


# files
folder ='/your_folder/'
data = 'doublePlotData.xlsx'
cor= pandas.read_excel(folder+data)

# data assignements
x=np.transpose(cor.values)[0][1:]
y=np.transpose(cor.values)[1][1:]
z=np.transpose(cor.values)[2][1:]
x1=np.transpose(cor.values)[3][1:]
z1=np.transpose(cor.values)[4][1:]
y1=np.transpose(cor.values)[5][1:]

#fits
fit=fitSaturation(x,z)
fit1=fitSaturation(x1,z1)

fig = plt.figure(figsize=(6,6),dpi=150)
gs1 = gridspec.GridSpec(10, 2)#y,x
ax1 = fig.add_subplot(gs1[6:,0:1])#[y1:y2,x1,x2]
ax2 = fig.add_subplot(gs1[6:,1:2])#[y1:y2,x1,x2], sharex=ax



linePlotDouble(ax1,x,y,z,fit.best_fit)
linePlotDouble(ax2,x1,y1,z1,fit1.best_fit,left_ticks=True)
