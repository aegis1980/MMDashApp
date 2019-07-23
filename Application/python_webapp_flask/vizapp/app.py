
import pandas as pd
import plotly.graph_objs as go
from python_webapp_flask.IES import IesDataTool 
import numpy as np
import math
import json



zone_names = ['Lower perimeter','Lower inner','Bleachers perimeter','Bleachers inner','Upper perimeter','Upper inner','Lower foyer perimeter','Lower foyer inner']
glasses = ['BECA SU', 'BECA IGU','MM SU', 'MM IGU' ]
filename = 'webappdata\data_file.xlsx'

my_ies_tool = IesDataTool(zone_names,glasses)   
my_ies_tool.load_data(filename,load_from_pickle = True, save_to_pickle = True)

# this loads glass info (SC, U etc) from json file. 
with open('python_webapp_flask\data\glass_info.js', 'r') as f:
        glass_info = json.load(f)

# this is a bit of a hack
for glass in glass_info:
    glass_info[glass].update(
        {'markdown': 
            glass_info[glass]['description']+ '<br/>' +
            '<u>**SC:**</u>' + str(glass_info[glass]['sc']) + '<br/>' +
            '<u>**VLT:**</u>' + str(glass_info[glass]['tv']*100) +'%' + '<br/>' +
            '<u>**U:**</u>' + str(glass_info[glass]['u']) +' W/m<sup>2</sup>' + '<br/>' 
         })

###################################################################
# helper methods


def format_time_from_slider(slider_time):
    t =  '{}:{}:00'.format(math.floor(slider_time/2),(slider_time % 2)*30)
    return pd.datetime.strptime(t,'%H:%M:%S').time()



def my_filter(x, pmv, filter_mode):
    
    """ filters pmv data for binary heatmap. filter_mode= True heat, filter_mode= False: cold."""
    if x>=pmv:
        return int(filter_mode)
    else:
        return int(not filter_mode)


def generate_heatmap_figure(zones, scenario, time_range, data_mode, n_days, filter, pmv, filter_mode):
    df = my_ies_tool.get_heatmap_array_df(dataset= IesDataTool.COMBINED_PMV, zones= zones, scenario=scenario, time_range = time_range, data_mode = data_mode, n_days=n_days)
    
    readable_times = [str(x)[:-3] for x in df.index.tolist()] # times for y axes.
    readable_dates = [pd.to_datetime(x).strftime('%d %b') for x in df.columns.values.tolist()]

    # xgap>0 and ygap>0 puts separating lines on heatmap.
    if (data_mode =='Y'): #annual data
        x_gap = 0
        y_gap = 0 
    else: # n-hottest or coldest
        x_gap = 2 
        y_gap = 1


    data_plain = go.Heatmap(
                    z= df,
                    xgap = x_gap,
                    ygap = y_gap,
                    zmid = 0,
                    zmax = df.values.max(),
                    x = readable_dates,
                    y = readable_times)

    if filter:
        filtered_df = df.applymap(lambda x : my_filter(x,pmv, filter_mode))
        data_filtered = go.Heatmap(
                        z= filtered_df,
                        name = 'filtered data',
                        xgap = x_gap,
                        ygap = y_gap,
                        x = readable_dates,
                        y = readable_times,
                        opacity=0.5,
                        colorscale= [
                                [0, 'rgb(255,255,255)'],
                                [1, 'rgb(0,0,0)']
                            ],
                        showscale=False
                    )
        data = [data_plain,data_filtered]
    else:
        data = [data_plain]

    if data_mode != 'Y':
        x_title = ('Coldest' , 'Hottest')[data_mode == 'NH'] + str (n_days) + ' day' + ('' , 's')[n_days>1]
    else:
        x_title = 'Annual data'

    return {'data': data,
            'layout': go.Layout(
                        xaxis ={ 'title': x_title},
                        yaxis ={ 'title': 'Time of day'}
                    ) 
            }
