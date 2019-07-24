import pandas as pd
import _pickle as pickle
from pathlib import Path
from python_webapp_flask import ASSETS_PATH
import os

class IesDataTool:

    """ file where data imported from pmv_scv saved """
    PICKLE_FILENAME = ASSETS_PATH + 'data\myfile.pkl'

    # Default sheet name from IES
    # Do not change unless you changed sheet names in IES    
    SUMMER_CLO_PMV = 'Summer CLO'
    WINTER__CLO_PMV = 'Winter CLO'
    INTERNAL_TEMP = 'Internal Temperature'
    RADIANT_TEMP = 'Mean Radiant Temperature'
    OUTDOOR_TEMP = 'Outdoor DB Temperature'


    DEFAULT_SHEETS = [
        SUMMER_CLO_PMV, 
        WINTER__CLO_PMV, 
        INTERNAL_TEMP, 
        RADIANT_TEMP, 
        OUTDOOR_TEMP
     ]

    """ Dict name for generated combined file """
    COMBINED_PMV= 'Combined PMV'


    @staticmethod
    def isNaN(num):
        """Used to get rid of NaN cells in imported data"""
        return num != num

    @staticmethod
    def combine_summer_winter_fn(x1, x2):
        """On the logic that person can put on clothes/ take them off to become more comfortable"""
        x3 = []

        for i in range(len(x1)):
            if (abs(x1[i]) < abs(x2[i])): #x1 more comfortable (closer to zero)
                x3.append(x1[i])
            else:
                x3.append(x2[i])

        return x3


    def __init__(self, zone_names, scenarios):
        """ Constructor """
        self.zone_names = zone_names    
        self.scenarios = scenarios
        self._full_df = {} #dict of dataframes. 



    def load_pmv_data(self, filenames = None, load_from_pickle = True, save_to_pickle = True):
              
        if load_from_pickle :
            my_file = Path(IesDataTool.PICKLE_FILENAME)
            if my_file.is_file():
                print('Loading from existing data from pickle file')
                self._full_df = pd.read_pickle(IesDataTool.PICKLE_FILENAME)
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
            self._full_df.to_pickle(IesDataTool.PICKLE_FILENAME)
            print ('...Done. ')
 

    def load_data(self, filename = None, load_from_pickle = True, save_to_pickle = True):

        if load_from_pickle :
            if self.load_data_from_pickle(): 
                return #if we got here then we successfully loaded a file. no need to proceed. 

        #importing excel file
        print('Importing data from excel file')
        
        # returns dict of sheets.
        imported_df = pd.read_excel(filename, sheet_name=None, skiprows=1)

        #for idx,val in enumerate(imported_df.keys()):
        #    if val.strip() is not IesDataTool.DEFAULT_SHEETS[idx].strip():
        #        raise Exception('Imported file needs to have sheets labelled')

            
        # START OF EXCEL PARSE      

        # strips out times and cleans them up. This could be slicker.
        time_df = self.create_clunky_time_df(imported_df)


        for k in IesDataTool.DEFAULT_SHEETS[:-1]: # external temp not quite the same format as all others.
            self.combine_time_df_and_data(time_df,imported_df,k)

        # END OF EXCEL PARSE

        # Create new df with key 'COMBINED_PMV with combines summer and winter clothing pmvs.
        self._full_df.update( 
            {IesDataTool.COMBINED_PMV : self._full_df['Summer CLO'].combine(self._full_df['Winter CLO'],IesDataTool.combine_summer_winter_fn)} )

        if save_to_pickle:
            print ('Saving as pickle, for next time...')

            pickle_out = open(IesDataTool.PICKLE_FILENAME, 'wb')
            pickle.dump(self._full_df, pickle_out)
            pickle_out.close()
            #self._full_df.to_pickle(IesDataTool.PICKLE_FILENAME)
            print ('...Done. ')



    def get_heatmap_array_df(self, dataset = COMBINED_PMV, zones = None, scenario = None, time_range = None, data_mode= None, n_days = None):
        pmv_df = self._full_df[dataset]
        df = pmv_df[[(scenario, i) for i in zones]].max(axis=1).unstack().transpose().iloc[::-1]

        # will shown all times.
        if time_range is not None:
            df = df.loc[time_range[1]:time_range[0]]

        df = df[::-1] # reverse rows so early in day is on bottom of hmap

        if data_mode != 'Y': # if datamode is 'Y' (year) then return whole year's data
            if isinstance(n_days, int): 
                # taking 'hottest'(NH) or coldest as largest/smallest summed pmv. over allotted time period.
                sum = df.sum().sort_values(ascending = (data_mode == 'NC'))
                sum = sum[:-(len(sum)-n_days)]
                df = df[sum.index]

        return df


    def create_clunky_time_df(self, imported_df):
        full_df = imported_df['Summer CLO']
        #import and concat times as df_t
        time_df = full_df.iloc[:,0:2].copy()
        time_df.columns = ['date','time']
        time_df = time_df.iloc[1:].reset_index(drop=True)

        #Replace nans with dates. Mmmm. love na(a)ns.
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
        #time_df['time'] = time_df.apply(lambda r : pd.datetime.strptime(r['time'],'%H:%M').time(),1)
        #time_df['time'] = time_df.apply(lambda r : r['time'].time(),1)
        return time_df


    def combine_time_df_and_data(self,time_df, imported_df, key):
        r = 2
        zones = len(self.zone_names)
        temp_df  = {}
        for scen in self.scenarios:
            temp_df[scen] =imported_df[key].iloc[:,r:r+zones]
            temp_df[scen] = temp_df[scen].iloc[1:].reset_index(drop=True)
            temp_df[scen].columns = self.zone_names
            temp_df[scen] =  pd.concat([time_df,temp_df[scen]], axis =1)
            temp_df[scen]=  temp_df[scen].set_index(['date','time'])
            r = r + zones

        #package all cleaned data up back into single dataframe
        self._full_df.update( {key : pd.concat(temp_df, axis=1)} )
        self._full_df[key] = self._full_df[key].applymap(lambda x : pd.to_numeric(x, errors='coerce'))


    def load_data_from_pickle(self):
        my_file = Path(IesDataTool.PICKLE_FILENAME)
        if my_file.is_file():
            print('Loading from existing data from pickle file')
            #self._full_df = pd.read_pickle(IesDataTool.PMV_PICKLE_FILENAME)

            pickle_in = open(IesDataTool.PICKLE_FILENAME,"rb")
            self._full_df = pickle.load(pickle_in)

            print('Done')
            return True
        else:
            print('No existing pickle file found.')
            if (filename == None):
                raise Exception('You need to define an excel data file')
                return
            return False

    @property
    def fullDataframe(self):
        return self._full_df

    @property
    def combined_pmv(self):
        return self._full_df[IesDataTool.COMBINED_PMV]

    @property
    def internal_temp(self):
        return self._full_df[IesDataTool.INTERNAL_TEMP]



        


