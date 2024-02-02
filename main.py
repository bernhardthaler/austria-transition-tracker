# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:10:31 2024

@author: Bernhard
"""

from plot import plot 
from utils.filter import get_filtered_data

data = get_filtered_data(name = "meat",
                         options = {"meat": "Pigmeat [B3100]",
                                    "meatitem": "Slaughterings [SL]"},
                         unit = "THS_T", movmean = 4)

plot.plot_single(name = "Schweinefleisch", unit = "kt", data=data)