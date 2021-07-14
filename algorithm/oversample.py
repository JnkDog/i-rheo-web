import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
from scipy.interpolate import interp1d
import pandas as pd
import math
from scipy import interpolate
import plotly.express as px
import base64
import io

class Oversampling:
    def __init__(self, data):
        self.data = data
    #available after design g_0,g_dot_inf input label

    '''       
        def __init__(self,g0,ginf,InterpFunc):    
            self.g0= g0
            self.ginf= ginf
            self.InterpFunc= InterpFunc
    ''' 

    def OverSample(self):
        #,t,g,g0,ginf,InterpFunc):
        df_news = pd.read_table(self.data, header = None)
        t = df_news[0]
        g = df_news[1]
        t0 = 0   

        g0 = 1     #delet after design input label
        ginf = 0   #delet after design input label
        InterpFunc = "slinear"  #delet after design input label

        freqpoints = 200
        DIP = math.log10(len(t))/math.log10(t[-1]/t[0]);
        if DIP < 0.6:
            OverSample = int(10^(math.log10(t[-1]/t[0])))
            t_I = np.linspace(0,t[-1],OverSample)
            t1 = np.hstack((0,t))
            g1 = np.hstack((g0,g))
            f = interpolate.interp1d(t1, g1, InterpFunc)
            Gint_I = f(t_I)
        else:
            OverSample = int(len(t)*1e1)
            t_I = np.linspace(0,t[-1],OverSample)
            t1 = np.hstack((0,t))
            g1 = np.hstack((g0,g))
            f = interpolate.interp1d(t1, g1, "slinear")
            Gint_I = f(t_I)
        plt.plot(t_I, Gint_I, '-o', lw=3, color='royalblue', label='$G^{II}$')
        plt.xscale('log')
        plt.xlabel('Time (s)')
        plt.ylabel('G(t) (Pa)')
        plt.show()
    
    # @staticmethod
    def oversamping_process(self, t, g, points_number, option):
        DIP = math.log10(len(t))/math.log10(t[len(t)-1]/t[1])
        g0 = 1
        InterpFunc = option

        if DIP < 0.6:
            OverSample = int(10 ^ (math.log10(t[len(t) - 1] / t[1])))
            t_I = np.linspace(0, t[len(t)-1], OverSample)
            t1 = np.hstack((0, t))
            g1 = np.hstack((g0, g))
            f = interpolate.interp1d(t1, g1, InterpFunc)
            Gint_I = f(t_I)
        else:
            OverSample = int(len(t) * 1e1)
            t_I = np.linspace(0, t[len(t)-1], OverSample)
            t1 = np.hstack((0, t))
            g1 = np.hstack((g0, g))
            f = interpolate.interp1d(t1, g1, "slinear")
            Gint_I = f(t_I)
        
        return t_I, Gint_I

    # @classmethod
    def oversamping_render(self, content, points_number, option):
        fig = px.scatter()
    
        if content is not None:
            points_number = math.floor(points_number)
            contents = content.split(",")[-1]
            decoded = base64.b64decode(contents)
            df = pd.read_table(io.StringIO(decoded.decode("utf-8")))
            df.columns = ["Time (s)", "G(t) (Pa)"]
            t_I, Gint_I = self.oversamping_process(df["Time (s)"], df["G(t) (Pa)"], points_number, option)

            # need modify later
            t_I = pd.Series(t_I.tolist())
            Gint_I = pd.Series(Gint_I.tolist())
            df = DataFrame(dict(t_I = t_I, Gint_I = Gint_I))
            df.columns = ["Time (s)", "G(t) (Pa)"]
            
            fig = px.line(data_frame=df, x="Time (s)", y="G(t) (Pa)", log_x=True, range_y=[0, 1])

        return fig
        
##zyy=oversampling("SingExp6_5.txt")
#zyy.OverSample()

          