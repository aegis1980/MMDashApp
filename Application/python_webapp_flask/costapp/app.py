
import pandas as pd
import plotly.graph_objs as go
import numpy as np
import math
import json

from python_webapp_flask.Cost import CostTool

zone_names = ['Lower perimeter','Lower inner','Bleachers perimeter','Bleachers inner','Upper perimeter','Upper inner','Lower foyer perimeter','Lower foyer inner']
glasses = ['BECA SU', 'BECA IGU','MM SU', 'MM IGU' ]
filename = 'data\data_file.xlsx'

my_cost_tool = CostTool('python_webapp_flask\data\cost_data.csv')

DEFAULT_NZ_COMMERCIAL_ERATE = 16.88 #est c/kWhr for NZ MBIE for 2019 commercial

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

