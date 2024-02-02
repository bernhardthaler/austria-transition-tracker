# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 17:10:55 2024

@author: Bernhard
"""

import eurostat 
import pandas as pd 

def download_and_save(name = "",
                      code = "",
                      start_period = 2010, 
                      options = [],
                      geo = ["AT"]):
    print("Downloading data %s ..." %(name))
    
    my_filter_pars = {'startPeriod': start_period, 
                      'geo': geo}
    
    options_dict = {}
    for option in options: 
        specs = eurostat.get_par_values(code, option)
        names = eurostat.get_dic(code, option, frmt = "dict")
        options_dict[option] = {"specs": specs, "names": names}
        
        my_filter_pars[option] = specs 
        
    data = eurostat.get_data_df(code, filter_pars=my_filter_pars)
    
    for option in options_dict: 
        for spec in options_dict[option]["specs"]:
            data = data.replace(spec, options_dict[option]["names"][spec] + " ["+spec+"]")
    
    df = pd.DataFrame(data)
    df.to_excel("../data/%s_%s.xlsx" %(geo[0], name))  
    
    
if __name__ == "__main__": 
    
    ### meat production 
    download_and_save(name = "meat", 
                      code = "apro_mt_pheadm", 
                      options = ["meat", "meatitem"])
    
    ### gas consumption 
    download_and_save(name = "gas", 
                      code = "NRG_CB_GASM", 
                      options = ['siec', 'nrg_bal'])

    ### coal consumption 
    download_and_save(name = "coal", 
                      code = "NRG_CB_SFFM", 
                      options = ['siec', 'nrg_bal'])    
    
    ### oil consumption 
    download_and_save(name = "oil", 
                      code = "NRG_CB_OILM", 
                      options = ['siec', 'nrg_bal'])    
    
    
    
