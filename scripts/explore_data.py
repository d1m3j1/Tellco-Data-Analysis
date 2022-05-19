import numpy as np 
import pandas as pd 
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import IPython
from plotly.offline import init_notebook_mode

def enable_plotly_in_cell():
  display(IPython.core.display.HTML('''<script src="/static/components/requirejs/require.js"></script>'''))
  init_notebook_mode(connected=False)

class ExploreTelcomData:

    def __init__(self, df):
        self.df = df

    
################################################################################################################
# Visualizaion Graph
################################################################################################################

    def ourllier_1(self,x, y):
        enable_plotly_in_cell()
        

