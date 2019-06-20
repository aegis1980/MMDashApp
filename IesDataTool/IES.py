import pandas as pd
from pathlib import Path


class IesDataTool:

    """ file where data imported from pmv_scv saved """
    PMV_PICKLE_FILENAME = 'myfile.pkl'
    
    @staticmethod
    def isNaN(num):
        """Used to get rid of NaN cells in imported data"""
        return num != num


    @staticmethod
    def combine_summer_winter(x1, x2):
        """On the logic that person can put on clothes/ take them off to become more comfortable"""
        if (abs(x1) < abs(x2)): #x1 more comfortable (closer to zero)
            return x1
        else:
            return x2


    def __init__(self, zone_names, scenarios):
        self.zone_names = zone_names    
        self.scenarios = scenarios
        self._full_df = None
        self._imported_df = None #list of dataframes. 


    def load_pmv_data(self, filenames = None, load_from_pickle = True, save_to_pickle = True):
              
        if load_from_pickle :
            my_file = Path(IesDataTool.PMV_PICKLE_FILENAME)
            if my_file.is_file():
                print('Loading from existing data from pickle file')
                self._full_df = pd.read_pickle(IesDataTool.PMV_PICKLE_FILENAME)
                print('Done')
                return 
            else:
                print('No existing pickle file found.')
                if (filenames == None):
                    raise Exception('You need to define at least one (max two) csv data files')
                    return

       

        #importing csv files
        print('Importing data from csvs')
        self._imported_df = [None] * len(filenames)
        
        # START OF CSV IMPORT AND PARSE
        fi = 0
        for filename in filenames:
           
            full_df = pd.read_csv(filename, skiprows=1)
            #import and concat times as df_t
            time_df = full_df.iloc[:,0:2].copy()
            time_df.columns = ['date','time']
            time_df = time_df.iloc[1:].reset_index(drop=True)

            #Replace nans with dates. Mmmm. love nans.
            #No. Sorry, I love Naans.
            for i, row in time_df.iterrows():
                d =row['date']
                if (not IesDataTool.isNaN(d)):
                    currentDate = d
                else:
                    time_df.iat[i,0] = currentDate

            #parse string-date into datetime
            time_df['date'] = time_df.apply(lambda r : pd.datetime.strptime(r['date'],'%a, %d/%b'),1)

            #parse string-time into datetime.time
            time_df['time'] = time_df.apply(lambda r : pd.datetime.strptime(r['time'],'%H:%M').time(),1)
        
            #create new column that combine date and time. 
            #time_df['date-time'] = time_df.apply(lambda r : pd.datetime.combine(r['date'],r['time']),1)


            r = 2
            zones = len(self.zone_names)
            temp_df  = {}
            for scen in self.scenarios:
               temp_df[scen] =full_df.iloc[:,r:r+zones]
               temp_df[scen] = temp_df[scen].iloc[1:].reset_index(drop=True)
               temp_df[scen].columns = self.zone_names
               temp_df[scen] =  pd.concat([time_df,temp_df[scen]], axis =1)
               temp_df[scen]=  temp_df[scen].set_index(['date','time'])
               r = r + zones

            #package all cleaned data up back into single dataframe
            self._imported_df[fi] = pd.concat(temp_df, axis=1)
            self._imported_df[fi] = self._imported_df[fi].applymap(lambda x : pd.to_numeric(x, errors='coerce'))
            fi += 1
    
        # END OF CSV IMPORT AND PARSE

        if len(self._imported_df) == 1: #user only imported single file.
            self._full_df = self._imported_df[0]
        else:
            df1 = self._imported_df[0]
            df2 =  self._imported_df[1]
            self._full_df = df1.DataFrame.combine(df2,self.__combine_summer_winter())
            self._full_df = self._full_df.set_index(['date','time'])
            


        if save_to_pickle:
            print ('Saving as pickle, for next time...')
            self._full_df.to_pickle(IesDataTool.PMV_PICKLE_FILENAME)
            print ('...Done. ')
 

    def get_heatmap_array_df(self, zones = None, scenario = None, 
                             time_range = None, hottest_n = None):

        df = self.fullDataframe[[(scenario, i) for i in zones]].max(axis=1).unstack().transpose().iloc[::-1]

        if time_range is not None:
            df = df.loc[time_range[1]:time_range[0]]

        df = df[::-1] # reverse rows so early is on bottom of hmap

        if isinstance(hottest_n, int): 

            # taking 'hottest' as largest summed pmv. over allotted time period.
            sum = df.sum().sort_values(ascending = False)
            sum = sum[:-(len(sum)-hottest_n)]
            df = df[sum.index]

        return df






    @property
    def fullDataframe(self):
        return self._full_df






        


