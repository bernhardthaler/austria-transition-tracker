# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:05:47 2024

@author: Bernhard
"""

import matplotlib.pyplot as plt 
import matplotlib.dates as mdates

def plot_single(name = "",
                unit = "",
                data = {}): 
    
    fig, ax = plt.subplots(1,2, squeeze = False)
    fig.set_size_inches(12,5)

    times_years = list(data["data_yearly"].keys())
    times_months = list(data["data_monthly"].keys())
    times_months_mean = list(data["data_monthly_mean"].keys())

    ax[0,0].plot(times_years, 
                 [data["data_yearly"][time] for time in times_years],
                label = name)
    
    ax[0,1].plot(times_months, 
                 [data["data_monthly"][time] for time in times_months], 
            label = name)
    ax[0,1].plot(times_months_mean, 
                 [data["data_monthly_mean"][time] for time in times_months_mean], 
            label = "%s (%i-month-mean)" %(name, data["meta"]["movmean"]))
    
    ax[0,0].xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax[0,1].xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
    
    for a in [0,1]:
        ax[0,a].set_axisbelow(True)
        ax[0,a].set_ylabel("Value (%s)" %(unit))
        ax[0,a].grid()
        ax[0,a].legend(loc = "lower left")
        ax[0,a].set_ylim(bottom=0)
        
    plt.tight_layout()