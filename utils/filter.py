# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 17:23:46 2024

@author: Bernhard
"""

import pandas as pd 
from datetime import datetime 
import numpy as np 
import os 

def get_filtered_data(name = "meat",
                   geo = "AT",
                   start_year = 2010,
                   end_year = 2023,
                   options = {},
                   unit = "",
                   movmean = 4): 
    
    data = pd.read_excel(os.path.join(os.path.dirname(__file__), 
                              "../data/%s_%s.xlsx" %(geo, name)))
    data = data.fillna(0)
    
    ### filter dataframe for desired options 
    data_trim = data[(data["unit"] == unit)]
    for option in options: 
        data_trim = data_trim[data_trim[option] == options[option]]

    times = pd.date_range(start = datetime(year = start_year, month = 1, day =1),
                          end = datetime(year = end_year+1, month = 1, day = 1),
                          freq="M")
    
    ### find last key with columns 
    for month in range(1, 13):
        if "%i-%02i" %(end_year, month) in data: 
            if sum(data["%i-%02i" %(end_year, month)] > 0):
                last_month = month 

    out = {"data_monthly": {},
           "data_yearly": {},
           "data_yearly_cut": {}}

    times_months = []
    for time in times: 
        if time.year == end_year and time.month > last_month: 
            pass 
        else: 
            times_months.append(time)
            time_key = "%i-%02i" %(time.year, time.month)
            
            if time_key not in data.keys(): value = 0 
            else: value = float(data_trim[time_key])
    
            yeartime = datetime(year = time.year, month = 1, day = 1)
            if yeartime not in out["data_yearly"]: 
                out["data_yearly"][yeartime] = value
                
                if time.month <= last_month:
                    out["data_yearly_cut"][yeartime] = value
                    
            else: 
                out["data_yearly"][yeartime] += value
                
                if time.month <= last_month:
                    out["data_yearly_cut"][yeartime] += value                
                
            out["data_monthly"][time]= value 
            
    
    months = list(out["data_monthly"].keys())
    values = list(out["data_monthly"][key] for key in out["data_monthly"])
    out["data_monthly_mean"] = {}
    for t in range(len(months)-movmean):
        out["data_monthly_mean"][months[t+movmean]] = np.mean(
            values[t:t+movmean])
    
    out["meta"] = {"movmean": movmean}
    
    return out 



if __name__ == "__main__": 
    
    out = get_filtered_data(name = "meat",
                             options = {"meat": "Pigmeat [B3100]",
                                        "meatitem": "Slaughterings [SL]"},
                             unit = "THS_T")
    
    # import matplotlib.pyplot as plt 
    # plt.plot(out["data_monthly"].keys(), 
    #          [out["data_monthly"][key] for key in out["data_monthly"]])
    # plt.plot(out["data_monthly_mean"].keys(), 
    #          [out["data_monthly_mean"][key] for key in out["data_monthly_mean"]])