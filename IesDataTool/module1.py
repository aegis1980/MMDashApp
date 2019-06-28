# library
import pandas as pd
from IES import IesDataTool 
import numpy as np


zone_names = ['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8']
glasses = ['BECA SU', 'BECA IGU','MM IGU', 'MM SG' ]
filename = 'data\data_file.xlsx'

my_ies_tool = IesDataTool(zone_names,glasses)   
my_ies_tool.load_data(filename,load_from_pickle = True, save_to_pickle = True)

df_dict = my_ies_tool.fullDataframe
