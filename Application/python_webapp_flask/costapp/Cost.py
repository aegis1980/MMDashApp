import pandas as pd
import dash_table as table
import math
from operator import add

class CostTool():
    """Lifecycle $/carbon costing tool for facade"""

    RATE = 'rate ($/m2)'

    ENERGY_COOL = 'annual cooling (kWh pa)'
    ENERGY_HEAT = 'annual heating (kWh pa)'
    LIFE = 'expected life (yr)'

    def __init__(self, file):
        """ Constructor """ 
        self._dfin =  pd.read_csv(file)
        # to do 
        self._dfout = pd.DataFrame()
        self.params = None
        self.recalc_dfout()
        


    def columnsin(self):
        return self._dfin.columns

    def columnsout(self):
        return self._dfout.columns

    def datain(self):  
        return self._dfin.to_dict('records')
    
    def dataout(self):  
        return self._dfout.to_dict('records')

    def datain_change_from_ui(self, rows, columns,params):
        self._dfin = pd.DataFrame(rows, columns=[c['name'] for c in columns])
        self.params = params
        self.recalc_dfout()
        return self.dataout()

    def recalc_dfout(self):
        p = self.params
        rate = self._dfin[CostTool.RATE].astype('float32')
        service_life = self._dfin[CostTool.LIFE].astype('float32')
        energy_cool = self._dfin[CostTool.ENERGY_COOL].astype('float32')
        energy_heat = self._dfin[CostTool.ENERGY_HEAT].astype('float32')
    
 
        if (p is not None):
            init_cost = rate * p['area']

            # cost of replacement after service life, inc inflation
            rep_n = list(map (lambda x  : max(0,math.floor((p['design_life']-1)/x)) , service_life.values)) #no of replacements during life
            replacement_cost = [0.0] * len(rep_n)
            for i in range(len(rep_n)):    
                for j in range(rep_n[i]):
                    replacement_cost[i] = replacement_cost[i] + CostTool.compound_interest(init_cost[i], p['inflation'], service_life[i]*(j+1))


            for i in range(len(replacement_cost)):
                replacement_cost[i] =  replacement_cost[i] * p['rep_factor']


            #cost of energy
            #first year
            e_year1_heat = energy_heat * p['e_cost']
            e_year1_cool = energy_cool * p['e_cost']
            e_year1 = e_year1_heat + e_year1_cool
            # building life
            e_life_heat = list(map(lambda e : CostTool.cumulative_compound_interest(e,p['e_inflation'], p['design_life']), e_year1_heat))
            e_life_cool = list(map(lambda e : CostTool.cumulative_compound_interest(e,p['e_inflation'], p['design_life']), e_year1_cool))
            
            e_life = list(map(add, e_life_heat,e_life_cool))
            life_cost = init_cost + replacement_cost + e_life


            
            self._dfout['initial cost'] = list(map (CostTool.format_money, init_cost))
            self._dfout['replacement cost'] =  list(map (CostTool.format_money, replacement_cost)) 
 
            self._dfout['Energy cost (y1)'] = list(map (CostTool.format_money, e_year1))
            self._dfout['Energy cost lifetime'] = list(map (CostTool.format_money, e_life))

            self._dfout['lifetime cost'] = list(map (CostTool.format_money, life_cost))
        else:
            self._dfout['initial cost'] = rate * 1
            self._dfout['replacement cost'] = rate * 1
            self._dfout['Energy cost (y1)'] = 'na'
            self._dfout['Energy cost lifetime'] = 'na'
            self._dfout['lifetime cost'] = 'na'        


    def total_cost_breakdown(self, scenario):
        df = self._dfout
        return ()



# static helper methods

    def compound_interest(principle, irate, time): 
        """ Calculates compound interest. irate in pp, not %! """ 
        return principle * (pow((1 + irate), time)) 

    def cumulative_compound_interest(principle, irate, time):
        tot =0
        for t in range(time):
            tot = tot + CostTool.compound_interest(principle, irate, t)
        
        return tot
        #return sum(map (lambda t : CostTool.compound_interest(principle, irate, t),range(time)))


    def format_money(x):
        return "${:,.0f}".format(x)
         