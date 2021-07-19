
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import pandas as pd

class mtfourier:
    def __init__(self,data):
        self.data=data

    #available after design g_0,g_dot_inf input label
    '''       
        def __init__(self,g_0,g_dot_inf):    
            self.g_0= g_0
            self.g_dot_inf= g_dot_inf
    '''    
    #invoking test function to print G' and G"
    def test(self):
        df_news = pd.read_table(self.data,header = None)
        i = complex(0,1)
        time=np.linspace(1e-2,1e2,10000) 
        func = df_news[1]
        omega,res_test = mtfourier.manlio_ft(self,func,time,N_f=100,interpolate=True)
        g_p = np.real(res_test*omega*i)
        g_pp = np.imag(res_test*omega*i)
        fig = plt.figure(figsize=(6,5))
        plt.loglog(omega,g_p, '-o', lw=3, color='red',label='$G^{I}$') 
        plt.loglog(omega,g_pp, '-o', lw=3, color='royalblue',label='$G^{II}$')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Moduli (Pa)')
        plt.legend()
        plt.show()
    
    def manlio_ft(self,g,t,g_0=1,g_dot_inf=0,N_f=100,interpolate=True,oversampling=10):
        """ 
        Calculates the Fourier transform of numeric data.

        Takes any numeric time-dependent function g(t) that vanishes fot t<0,
        sampled at finite points [g_k,t_k] with k=1...N, and returns its 
        Fourier transform g(omega), together with the frequency range omega 
        defined from 1/t_max to 1/t_min. For details on the numerical procedure,
        refer to Tassieri et al., 2016 (https://doi.org/10.1122/1.4953443).

        Parameters
        ---------
        g : array 
            measured time-dependent variable.
        t : array 
            time array. 
        g_0: 
            value of g at time euqal 0. Can be taken as g[0].
        g_dot_inf:
            value of the time derivative of g at time equal infinity. Can be taken as 0.
        N_f: int
            frequency samples.
        interpolate: bool
            if True, data is interpolated with a cubic spline and re-sampled in log-space.
        oversampling: int
            factor by which the length of the time array is increased for oversampling in log-space.
        """
    
        g=np.array(g)
        t=np.array(t)
    
        if interpolate is True:
            gi = interp1d(t,g,kind='cubic',fill_value='extrapolate')
            t_new = np.logspace(min(np.log10(t)),max(np.log10(t)),len(t)*oversampling) #re-sample t in log space
            g = gi(t_new) # get new g(t) taken at log-space sampled t
            t = t_new
        i = complex(0,1)
        min_omega = 1/max(t)
        max_omega = 1/min(t)
        N_t=len(t)
        omega = np.logspace(np.log10(min_omega),np.log10(max_omega),N_f)
        zero=i*omega*g_0 + (1-np.exp(-i*omega*t[1]))*((g[1]-g_0)/t[1])\
                + g_dot_inf*np.exp(-i*omega*t[N_t-1]) 
        res = np.zeros(len(omega),dtype=complex)
        for w_i, w in enumerate(omega):
            after = 0
            for k in range(2,N_t):
                after+=((g[k] - g[k-1]) / (t[k] - t[k-1])) * (np.exp(-i * w *
                t[k-1])-np.exp(-i * w * t[k]))
            res[w_i]=(zero[w_i]+after)
        return omega, ((res)/(i*omega)**2)

