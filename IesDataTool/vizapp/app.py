
import pandas as pd
import plotly.graph_objs as go
from IES import IesDataTool 
import numpy as np
import math


zone_names = ['Lower perimeter','Lower inner','Bleachers perimeter','Bleachers inner','Upper perimeter','Upper inner','Lower foyer perimeter','Lower foyer inner']
glasses = ['BECA SU', 'BECA IGU','MM SU', 'MM IGU' ]
filename = 'data\data_file.xlsx'

my_ies_tool = IesDataTool(zone_names,glasses)   
my_ies_tool.load_data(filename,load_from_pickle = True, save_to_pickle = True)


###################################################################
# helper methods


def format_time_from_slider(slider_time):
    t =  '{}:{}:00'.format(math.floor(slider_time/2),(slider_time % 2)*30)
    return pd.datetime.strptime(t,'%H:%M:%S').time()


def my_filter(x, pmv):
    mid = 0.5*(pmv[0]+pmv[1])
    if x<=pmv[0]:
        return pmv[0]
    elif x>=pmv[1]:
        return pmv[1]
    return mid