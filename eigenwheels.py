
# basic animated mod 39 wheel in python
from __future__ import division 
import glob
from PIL import Image
import re
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np 
import random

allow_plot = 1
allow_scatter = 1
allow_text = 1
allow_gif = 0

To          = 39 
k_o         = 1/3
sessions    = 10 

r_o=(1/4)
t_o=To*k_o
                              
batch_size  = sessions*To

#change this to the int vector representing input signal
#symbol = some_stochastic_vector
symbol      = np.zeros(batch_size,dtype=int) 

if allow_plot == 1 :
    #Init plot settings
    plt.close()
    plt.rcParams.update({
        "lines.color": "black",
        "patch.edgecolor": "black",
        "text.color": "black",
        "axes.facecolor": "black",
        "axes.edgecolor": "black",
        "axes.labelcolor": "black",
        "xtick.color": "black",
        "ytick.color": "black",
        "grid.color": "black",
        "figure.facecolor": "black",
        "figure.edgecolor": "black",
        "savefig.facecolor": "black",
        "savefig.edgecolor": "black"})
    #plt.xlabel('real alpha')
    #plt.ylabel('imaginary beta')
    #plt.title('events constellation')
    #plt.xlim(-2, 2)
    #plt.ylim(-2, 2)
    #plt.gca().set_aspect('equal', adjustable='box')
    
    #Create base colormapplt.close() wheel
    hsvwheel = cm.get_cmap('hsv', To)

#Main constants
wzero = 2 * np.pi * (1/To) #Base


#Initial conditions natural information field carrier
half=1/2
root_phase=np.sqrt(5)
root_norm=np.sqrt(3)

r_phase=half*(1+root_phase)
r_norm=half*(1+1j*root_norm)



#Plot constants
base_symbol_size=0
base_text_size=6
symbol_size =base_symbol_size*np.ones(batch_size,dtype=int)
text_size =base_text_size*np.ones(batch_size,dtype=int)
dots_per_inch=300
event_marker="o"

#Variables preallocation
xphitime    = np.zeros(batch_size,dtype=float)
yphitime    = np.zeros(batch_size,dtype=float)
phitime     = np.zeros(batch_size,dtype=complex)
phisymbol   = np.zeros(batch_size,dtype=complex)
xphisymbol  = np.zeros(batch_size,dtype=float)
yphisymbol  = np.zeros(batch_size,dtype=float)
z_time_phase = np.zeros(batch_size,dtype=complex)
z_time_norm  = np.zeros(batch_size,dtype=complex)
z_time=np.zeros(batch_size,dtype=complex)
z_carrier_alpha=np.zeros(batch_size,dtype=float)
z_carrier_beta=np.zeros(batch_size,dtype=float)
z_carrier=np.zeros(batch_size,dtype=complex)

events_index   = np.arange(batch_size,dtype=int)
nmod = events_index%To


for n in events_index:
    
    # Index parametrization
    
    phitime[n]      = np.exp(1j * wzero * nmod[n] )
    xphitime[n]     = phitime[n].real 
    yphitime[n]     = phitime[n].imag 
    z_time_phase[n] = ((n+1)/r_o) * np.exp(1j * ((r_o)/r_phase) * (n+1) )
    z_time_norm[n]  = (n+1) * r_norm
    z_time[n]=z_time_norm[n]/z_time_phase[n]
    z_carrier_alpha[n]=(r_o+t_o-(half/r_o)*n)*z_time[n].real
    z_carrier_beta[n]=(r_o+t_o-(half*root_norm)*n)*z_time[n].imag
    z_carrier[n]=z_carrier_alpha[n]+1j*z_carrier_beta[n]
    
    # Symbol parametrization
    
    symbol[n]      = nmod[n] # symbols follow events index
    #symbol[n]     = input_symbols[n]    
    #symbol[n]     = random.randint(1, To) # symbols from RNG
    phisymbol[n]   = np.exp(1j * wzero * symbol[n])
    xphisymbol[n]  = phisymbol[n].real
    yphisymbol[n]  = phisymbol[n].imag

 
    if allow_plot == 1 :
        #plot current event hsvwheel phase color in index space
    
         
        if allow_scatter==1 :
            plt.scatter(z_carrier_alpha[n], z_carrier_beta[n] , marker=event_marker, color=hsvwheel(symbol[n-7]), s=symbol_size[n])
            plt.scatter(z_carrier_alpha[n], (-1)*z_carrier_beta[n] , marker=event_marker, color=hsvwheel(symbol[n-6]), s=symbol_size[n])
            plt.scatter((-1)*z_carrier_alpha[n], z_carrier_beta[n] , marker=event_marker, color=hsvwheel(symbol[n-5]), s=symbol_size[n])
            plt.scatter((-1)*z_carrier_alpha[n], (-1)*z_carrier_beta[n] , marker=event_marker, color=hsvwheel(symbol[n-4]), s=symbol_size[n])
            plt.scatter(z_carrier_beta[n], z_carrier_alpha[n] , marker=event_marker, color=hsvwheel(symbol[n-3]), s=symbol_size[n])
            plt.scatter(z_carrier_beta[n], (-1)*z_carrier_alpha[n] , marker=event_marker, color=hsvwheel(symbol[n-2]), s=symbol_size[n])
            plt.scatter((-1)*z_carrier_beta[n], z_carrier_alpha[n] , marker=event_marker, color=hsvwheel(symbol[n-1]), s=symbol_size[n])
            plt.scatter((-1)*z_carrier_beta[n], (-1)*z_carrier_alpha[n] , marker=event_marker, color=hsvwheel(symbol[n]), s=symbol_size[n])
        if allow_text==1 :
            plt.text(z_carrier_alpha[n], z_carrier_beta[n],str(symbol[n]), color=hsvwheel(symbol[n-7]), size=text_size[n])
            plt.text(z_carrier_alpha[n], (-1)*z_carrier_beta[n],str(symbol[n]), color=hsvwheel(symbol[n-6]), size=text_size[n])         
            plt.text((-1)*z_carrier_alpha[n], z_carrier_beta[n],str(symbol[n]), color=hsvwheel(symbol[n-5]), size=text_size[n])
            plt.text((-1)*z_carrier_alpha[n], (-1)*z_carrier_beta[n],str(symbol[n]), color=hsvwheel(symbol[n-4]), size=text_size[n])      
            plt.text(z_carrier_beta[n], z_carrier_alpha[n] ,str(symbol[n]), color=hsvwheel(symbol[n-3]), size=text_size[n])
            plt.text(z_carrier_beta[n], (-1)*z_carrier_alpha[n] ,str(symbol[n]), color=hsvwheel(symbol[n-2]), size=text_size[n])
            plt.text((-1)*z_carrier_beta[n], z_carrier_alpha[n] ,str(symbol[n]), color=hsvwheel(symbol[n-1]), size=text_size[n])
            plt.text((-1)*z_carrier_beta[n],(-1)*z_carrier_alpha[n] ,str(symbol[n]), color=hsvwheel(symbol[n]), size=text_size[n])
        
        # Save a png with current state
        plt.savefig(f'img{n}.png',dpi=dots_per_inch)
    
        
