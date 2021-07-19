from matplotlib import pyplot as plt
import pandas as pd
import plotly.express as px
import base64
import io

class Sigma:
    def __init__(self, data):
        self.data = data

    def sigma_print(self):
        df_news = pd.read_table(self.data, header = None)
        plt.plot(df_news[0], df_news[1], '-o', lw=3, color='royalblue', label='$G^{II}$')
        plt.xscale('log')
        plt.xlabel('Time (s)')
        plt.ylabel('G(t) (Pa)')
        plt.show()
    
    @staticmethod
    def sigma_render(content):
        fig = px.scatter()

        if content is not None:
            contents = content.split(",")[-1]
            decoded = base64.b64decode(contents)
            df = pd.read_table(io.StringIO(decoded.decode("utf-8")))
            df.columns = ["Time (s)", "G(t) (Pa)"]
            
            fig = px.line(data_frame=df, x="Time (s)", y="G(t) (Pa)", log_x=True, range_y=[0, 1])
            # print(df)    
            
        return fig

