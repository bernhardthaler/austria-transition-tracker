# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 09:51:56 2024

@author: Bernhard
"""

import pandas as pd 

data = pd.read_csv("../../data_raw/statistik_austria/meat_consumption_StatCube_table_2024-03-16_09-44-19.csv",
                   skiprows = 6, encoding = "utf-8")