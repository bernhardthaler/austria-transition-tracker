# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 23:39:34 2024

@author: Bernhard
"""

import plotly.express as px
from plot_single import plot_single_go
import numpy as np 

from utils import filter_national_inventory
from utils.filter import filter_eurostat_energy_balance
from utils.filter import filter_uba_sectoral_emisssions
from utils.filter import filter_uba_emissions


def plot(): 
    siecs = {"Natural gas": "Natural gas",
             "Oil": "Oil and petroleum products (excluding biofuel portion)",
             "Biomass": "Primary solid biofuels",
              "Coal": "Solid fossil fuels",
             "Waste non-renewable": "Non-renewable waste",
             "Waste renewable": "Renewable municipal waste",
             "Total": "Total"}
    
    dark2 = px.colors.qualitative.Dark2
    colors_siecs ={"Natural gas": dark2[5],
                    "Oil": dark2[6],
                    "Coal": dark2[7],
                    "Biomass": dark2[4],
                    "Waste": dark2[2],
                    "Other": dark2[1]}    
    
    data  = filter_eurostat_energy_balance(bals = ["Gross heat production"],
                                                 siecs = siecs)
    
    data_plot = {"data": {"Natural gas": data["data"]["Natural gas"],
                          "Oil": data["data"]["Oil"],
                          "Coal": data["data"]["Coal"],
                          "Biomass": data["data"]["Biomass"],
                          "Waste": {"x": data["data"]["Waste non-renewable"]["x"],
                                    "y": (np.array(data["data"]["Waste non-renewable"]["y"])+
                                          np.array(data["data"]["Waste renewable"]["y"]))},
                          "Other": {"x":  data["data"]["Waste non-renewable"]["x"],
                                    "y": (np.array(data["data"]["Total"]["y"])-
                                          np.array(data["data"]["Natural gas"]["y"])-
                                          np.array(data["data"]["Oil"]["y"])-
                                          np.array(data["data"]["Coal"]["y"])-
                                          np.array(data["data"]["Biomass"]["y"])-
                                          np.array(data["data"]["Waste non-renewable"]["y"])-
                                          np.array(data["data"]["Waste renewable"]["y"]))}}}
    
    data_rel = {"data": {}}
    
    for siec in data_plot["data"]: 
        data_rel["data"][siec] = {"x": data_plot["data"][siec]["x"],
                                    "y": np.array(data_plot["data"][siec]["y"])/np.array(data["data"]["Total"]["y"])}
    
    plot_single_go(title = "<b>District heat generation (gross)</b>: energy",
                  filename = "AT_timeseries_dh_energy_use",
                  unit = "Energy (TWh)", 
                  data_plot = data_plot,
                  time_res = "yearly",
                  show_plot = False,
                   colors = list([colors_siecs[label] for label in colors_siecs]),
                  source_text = "eurostat energy balances (nrg_bal_c)",
                  plot_type = "area")
    
    
    plot_single_go(title = "<b>District heat generation (gross)</b>: energy shares",
                  filename = "AT_timeseries_dh_energy_use_share",
                  unit = "Share [%]", 
                  data_plot = data_rel,
                  time_res = "yearly",
                  show_plot = False,
                  colors = list([colors_siecs[label] for label in colors_siecs]),
                  source_text = "eurostat energy balances (nrg_bal_c)",
                  plot_type = "area",
                  plotmax_fac = 1)
    
    
    
    
    
    
    siecs = {"Natural gas": "Natural gas",
             "Biomass": "Bioenergy",
              "Coal": "Solid fossil fuels",
             "Waste non-renewable": "Non-renewable waste",
             "Waste renewable": "Renewable municipal waste",
             "PV": "Solar photovoltaic",
             "Wind": "Wind",
             "Hydro": "Hydro",
             "Total": "Total"}
    
    dark2 = px.colors.qualitative.Dark2
    set1 = px.colors.qualitative.Set1
    set2 = px.colors.qualitative.Set2
    set3 = px.colors.qualitative.Set3
    
    colors_siecs ={"PV": set3[5],
                   "Wind": dark2[0],
                   "Hydro": set1[1],
                   "Biomass": dark2[4],
                    "Natural gas": dark2[5],
                    "Coal": dark2[7],
                    "Waste": dark2[2],
                    "Other": dark2[1],
                    }    
    
    data  = filter_eurostat_energy_balance(bals = ["Gross electricity production"],
                                                 siecs = siecs)
    
    data_plot = {"data": {"PV": data["data"]["PV"],
                          "Wind": data["data"]["Wind"],
                          "Hydro": data["data"]["Hydro"],
                          "Biomass": data["data"]["Biomass"],
                          "Natural gas": data["data"]["Natural gas"],
                          "Coal": data["data"]["Coal"],
                          "Waste": {"x": data["data"]["Waste non-renewable"]["x"],
                                    "y": (np.array(data["data"]["Waste non-renewable"]["y"])+
                                          np.array(data["data"]["Waste renewable"]["y"]))},
                          "Other": {"x":  data["data"]["Waste non-renewable"]["x"],
                                    "y": (np.array(data["data"]["Total"]["y"])-
                                          np.array(data["data"]["Natural gas"]["y"])-
                                          np.array(data["data"]["PV"]["y"])-
                                          np.array(data["data"]["Wind"]["y"])-
                                          np.array(data["data"]["Hydro"]["y"])-
                                          np.array(data["data"]["Coal"]["y"])-
                                          np.array(data["data"]["Biomass"]["y"])-
                                          np.array(data["data"]["Waste non-renewable"]["y"])-
                                          np.array(data["data"]["Waste renewable"]["y"]))}}}
    
    data_rel = {"data": {}}
    
    for siec in data_plot["data"]: 
        data_rel["data"][siec] = {"x": data_plot["data"][siec]["x"],
                                    "y": np.array(data_plot["data"][siec]["y"])/np.array(data["data"]["Total"]["y"])}
    
    plot_single_go(title = "<b>Electricity production (gross)</b>: energy ",
                  filename = "AT_timeseries_elec_energy_use",
                  unit = "Energy (TWh)", 
                  data_plot = data_plot,
                  time_res = "yearly",
                  show_plot = False,
                  colors = list([colors_siecs[label] for label in colors_siecs]),
                  source_text = "eurostat energy balances (nrg_bal_c)",
                  plot_type = "area")
    
    
    plot_single_go(title = "<b>Electricity production (gross)</b>: energy shares",
                  filename = "AT_timeseries_elec_energy_use_share",
                  unit = "Share [%]", 
                  data_plot = data_rel,
                  time_res = "yearly",
                  show_plot = False,
                  colors = list([colors_siecs[label] for label in colors_siecs]),
                  source_text = "eurostat energy balances (nrg_bal_c)",
                  plot_type = "area",
                  plotmax_fac = 1)


if __name__ == "__main__": 
    plot()