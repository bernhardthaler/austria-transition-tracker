# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 17:11:04 2024

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
    
    ### Emissions total 
    data_total = filter_uba_emissions()
    emissions = filter_uba_sectoral_emisssions()
    
    emissions["data"]["Total"] = data_total["data"]["GHG emissions total"]
    
    plot_single_go(title = "<b>Austrian GHG emissions</b> by sectors",
                  filename = "AT_timeseries_co2_emissions_sectors",
                  unit = "Emissions (Mt<sub>CO2e</sub>)", 
                  data_plot = emissions,
                  time_res = "yearly",
                  show_plot = False,
                  source_text = "Umweltbundesamt (Klimadashboard)",
                  plot_type = "area",
                  plotmax_fac = 1.1)


    ### Emissions sectors 
    sectors = {"Buildings": {"file": "buildings"},
                "Energy & Industry": {"file": "energy_industry"},
                "Agriculture":  {"file": "agriculture"},
                "Waste":  {"file": "waste"},
                "Transport":  {"file": "transport"}, 
                "Fluorinated Gases": {"file": "fluorinated_gases"}, 
                }
    
    
    
    for sector in sectors: 
        ### emissions with sub-sectors 
        data_emissions = filter_national_inventory.filt(sector =  sector)
        
        plot_single_go(title = "<b>%s GHG emissions</b> by sub-sectors" %(sector),
                      filename = "AT_timeseries_"+sectors[sector]["file"]+"_emissions_sectors",
                      unit = "Emissions (Mt<sub>CO2e</sub>)", 
                      data_plot = data_emissions,
                      time_res = "yearly",
                      show_plot = False,
                      legend_inside = False,
                      source_text = "Austria NIR 2023, UBA (Klimadashboard), sectoral data 2022 extrapolated",
                      info_text = "<Other> data scaled to match total emissions from UBA dashboard",
                      plot_type = "area",
                      plotmax_fac = 1.1)
        
        
        
        
    ### Energies 
    sectors = {"Buildings": {"file": "buildings",
                              "en_bal": {"Households": "Final consumption - other sectors - households - energy use",
                                        "Commercial": "Final consumption - other sectors - commercial and public services - energy use"}},
                "Industry": {"file": "industry",
                            "en_bal": {"Iron & Steel": "Final consumption - industry sector - iron and steel - energy use",
                                        "Chemicals": "Final consumption - industry sector - chemical and petrochemical - energy use",
                                        "Pulp & Paper": "Final consumption - industry sector - paper, pulp and printing - energy use",
                                        "Non-metallic minerals": "Final consumption - industry sector - non-metallic minerals - energy use",
                                        "Non-ferrous metals": "Final consumption - industry sector - non-ferrous metals - energy use",
                                        "Transport equipment": "Final consumption - industry sector - transport equipment - energy use",
                                        "Machinery": "Final consumption - industry sector - machinery - energy use",
                                        "Mining": "Final consumption - industry sector - mining and quarrying - energy use",
                                        "Food industry": "Final consumption - industry sector - food, beverages and tobacco - energy use",
                                        "Wood industry": "Final consumption - industry sector - wood and wood products - energy use",
                                        "Construction": "Final consumption - industry sector - construction - energy use",
                                        "Textile": "Final consumption - industry sector - textile and leather - energy use",
                                        "Other": "Final consumption - industry sector - not elsewhere specified - energy use"
                                        }},
                "Agriculture":  {"file": "agriculture",
                                "en_bal": {"Total": "Final consumption - other sectors - agriculture and forestry - energy use"}},
                "Transport":  {"file": "transport",
                              "en_bal": {"Rail": "Final consumption - transport sector - rail - energy use",
                                          "Road": "Final consumption - transport sector - road - energy use",
                                          "Domestic aviation": "Final consumption - transport sector - domestic aviation - energy use",
                                          "Domestic shipping": "Final consumption - transport sector - domestic navigation - energy use",
                                          "Pipelines": "Final consumption - transport sector - pipeline transport - energy use",
                                          "Other": "Final consumption - transport sector - not elsewhere specified - energy use"}
                              }
                }

    
    siecs = {"Natural gas": "Natural gas",
              "Oil": "Oil and petroleum products (excluding biofuel portion)",
              "Coal": "Solid fossil fuels",
              "Biomass": "Bioenergy",
              "Electricity": "Electricity"}
    
    set2 = px.colors.qualitative.Dark2
    colors_siecs ={"Natural gas": set2[5],
                    "Oil": set2[6],
                    "Coal": set2[7],
                    "Biomass": set2[4],
                    "Electricity": set2[2]}    
    
    for sector in sectors: 
        data_all_abs = {}
        
        for bal in sectors[sector]["en_bal"]:
            data_all_abs[bal] = filter_eurostat_energy_balance(bals = [sectors[sector]["en_bal"][bal]],
                                                          siecs = siecs)
        
        data_all_abs_plot = {"Total": {"data": {}}}
        
        for siec in siecs: 
            total_sector = np.zeros(len(data_all_abs[bal]["data"]["Oil"]["x"]))
            for bal in sectors[sector]["en_bal"]:
                total_sector += data_all_abs[bal]["data"][siec]["y"]
            data_all_abs_plot["Total"]["data"][siec] =  {"x":  data_all_abs[bal]["data"][siec]["x"],
                                                          "y": total_sector}
        for bal in data_all_abs: 
            data_all_abs_plot[bal] = data_all_abs[bal]
            
            
        data_all_rel_plot = {}
        for bal in data_all_abs_plot:
            data_all_rel_plot[bal] = {"data": {}}
            
            data_total = np.zeros(len(data_all_abs_plot[bal]["data"]["Oil"]["x"]))
            for siec in siecs: 
                data_total += np.array(data_all_abs_plot[bal]["data"][siec]["y"])
    
            for siec in siecs: 
                data_all_rel_plot[bal]["data"][siec] = {"x": data_all_abs_plot[bal]["data"][siec]["x"],
                                  "y": data_all_abs_plot[bal]["data"][siec]["y"]/data_total}    
                
                
        plot_single_go(title = "<b>%s</b>: final energy use - shares" %(sector),
                      filename = "AT_timeseries_%s_final_energy_use_share" %(sectors[sector]["file"]),
                      unit = "Share [%]", 
                      data_plot = data_all_rel_plot,
                      time_res = "yearly",
                      show_plot = False,
                      colors = list([colors_siecs[label] for label in colors_siecs]),
                      source_text = "eurostat energy balances (nrg_bal_c)",
                      plot_type = "area_button",
                      plotmax_fac = 1)
            
        plot_single_go(title = "<b>%s</b>: final energy use" %(sector),
                      filename = "AT_timeseries_%s_final_energy_use" %(sectors[sector]["file"]),
                      unit = "Energy (TWh)", 
                      data_plot = data_all_abs_plot,
                      time_res = "yearly",
                      show_plot = False,
                      colors = list([colors_siecs[label] for label in colors_siecs]),
                      source_text = "eurostat energy balances (nrg_bal_c)",
                      plot_type = "area_button")

        
    return data_all_abs_plot
    
if __name__ == "__main__": 
    data = plot()