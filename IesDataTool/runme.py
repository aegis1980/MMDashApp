# library
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from IES import IesDataTool as IesDataTool

def filterFunction(x):
    if x>0.5:
        return x
    else:
        return 0.5


def main():
    zone_names = ['Zone 1','Zone 2','Zone 3','Zone 4','Zone 5','Zone 6','Zone 7','Zone 8']
    glasses = ['BECA SU', 'BECA IGU','MM IGU', 'MM SG' ]
    filename = 'C:/data/full_pmv_summer_clo.csv'

    my_ies_tool = IesDataTool(zone_names,glasses)   
    my_ies_tool.load_pmv_data([filename],load_from_pickle = True, save_to_pickle = True)

    df = my_ies_tool.fullDataframe

    print(df.iloc[:, df.columns.get_level_values(1)=='Zone 1'])
    scenario_col = 'BECA IGU'
    tup = ('BECA IGU','Zone 1')

   # print(df[tup1].max(axis=1).unstack())

    heatmap_df = df[tup].unstack(level=0)


    #
    heatmap_scenario_df = df[scenario_col].max(axis=1).unstack().transpose()
    #df =  my_ies_tool.generateMatrices()
    
    #tup = ('BECA IGU')
    #print(df.max(level='BECA IGU'))

    #months = [x.to_pydatetime().strftime("%b") for x in df.columns]
    #print(months)
    #plot using a color palette
    hm_ax = sns.heatmap(heatmap_scenario_df, square = True,cmap="Reds")


   
    
    sns.set(style = "white")
    #sns.heatmap(df, cmap="Blues")
    #sns.heatmap(df, cmap="BuPu")
    #sns.heatmap(df, cmap="Greens")
 
    #add this after your favorite color to show the plot
    plt.show()



#if __name__ == "__main__":
main()