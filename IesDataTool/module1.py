# library
import seaborn as sns
import matplotlib.pyplot as plt
import IES

zone_names = ['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8']
glasses = ['BECA IGU', 'BECA SG','MM IGU', 'MM SG' ]
filename = 'C:/data/full_pmv_summer_clo.csv'
ies = IES.IesImport(filename,zone_names,glasses)
ies.run()
df =  ies.get2DTimeMatrix()