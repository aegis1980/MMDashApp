# library
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from IES import IesDataTool 
import numpy as np

def filterFunction(x):
    if x>0.5:
        return x
    else:
        return 0.5


def main():
    zone_names = ['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8']
    glasses = ['BECA SU', 'BECA IGU','MM IGU', 'MM SG' ]
    filename = 'data/data_file.xlsx'

    my_ies_tool = IesDataTool(zone_names,glasses)   
    my_ies_tool.load_data([filename],load_from_pickle = True, save_to_pickle = True)

    df = my_ies_tool.fullDataframe
    #n = df.iloc[:,'date']

    ### THIS WORKS.
    z1 = df.iloc[:, df.columns.get_level_values(1)=='Zone 1'].transpose().to_numpy()
    bins = [0, 0.5, 0.75, 1, 1.25,2, np.inf]
    names = ['<2', '2-18', '18-35', '35-65', '65+']
   

    # creating a list of dataframe columns 
    columns = list(df) 


    binned_df = pd.DataFrame()
    for c in columns:
        col_data = df[c].transpose().to_numpy()
        binned_df[c] = pd.cut(col_data, bins = bins).value_counts()        


    #print (binned_df.head())

    ###TO HERE


    #df['pmv-ranges'] = df.apply(pd.cut(z1[0], bins = bins,).value_counts()

    #new = pd.cut(z1.values[0], bins = bins).value_counts()



   # a = z1.gt(limits).sum()
   # print(a)
    scenario_col = 'BECA IGU'
    tup = ('BECA IGU','Zone 1')

   # print(df[tup1].max(axis=1).unstack())
    heatmap_scenario_df = df[scenario_col].max(axis=1).unstack().transpose().iloc[::-1]
    #
    pmv = 0.5
    print(heatmap_scenario_df.applymap(lambda x : max(x,pmv)).head())
    #df =  my_ies_tool.generateMatrices()
    
    #tup = ('BECA IGU')
    #print(df.max(level='BECA IGU'))

    #months = [x.to_pydatetime().strftime("%b") for x in df.columns]
    #print(months)
    #plot using a color palette
    hm_ax = sns.heatmap(heatmap_scenario_df, square = True,cmap="coolwarm", center=0, vmin=-2, vmax=2)


   
    
    sns.set(style = "white")

    #add this after your favorite color to show the plot
    plt.show()



#if __name__ == "__main__":
main()