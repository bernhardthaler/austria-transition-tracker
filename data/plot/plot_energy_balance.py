# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 10:32:07 2024

@author: Bernhard
"""

import plotly.express as px
from plot_single import plot_single_go
import numpy as np 

from utils.filter import filter_eurostat_energy_balance



def plot(show_plot = False): 
    
    
    ### TOTAL FINAL AND PRIMARY ENERGY 
    siecs_gross_energy = {"Natural gas": ["Natural gas"],
              "Oil": ["Oil and petroleum products (excluding biofuel portion)"],
              "Coal": ["Solid fossil fuels"],
              "Biomass": ["Primary solid biofuels", "Charcoal", "Pure biogasoline",
                          "Blended biogasoline", "Pure biodiesels", "Blended biodiesels",
                          "Pure bio jet kerosene", "Blended bio jet kerosene", "Other liquid biofuels",
                          "Biogases"],
              "Renewable electricity": ["Hydro","Wind","Solar photovoltaic","Tide, wave, ocean"],
              "Ambient heat": ["Geothermal", "Solar thermal", "Ambient heat (heat pumps)"],
              "Other": ["Manufactured gases", "Industrial waste (non-renewable)", 
                        "Non-renewable municipal waste",
                        "Renewable municipal waste", "Heat", "Electricity"]}
    
    set2 = px.colors.qualitative.Dark2
    colors_siecs_gross_energy ={"Natural gas": set2[5],
                    "Oil": set2[6],
                    "Coal": set2[7],
                    "Biomass": set2[4],
                    "Renewable electricity": set2[2],
                    "Ambient heat": set2[3],
                    "Other": set2[1]}    
    
    data_all_abs = filter_eurostat_energy_balance(bals = ["Gross inland consumption"],
                                                  siecs = siecs_gross_energy)
    data_all_abs_plot = {"data": {}}
    
    for siec in siecs_gross_energy: 
        data_all_abs_plot["data"][siec] = data_all_abs["data"][siec]
        
    data_all_rel_plot = {"data": {}}
    
    data_total = np.zeros(len(data_all_abs_plot["data"]["Oil"]["x"]))
    for siec in colors_siecs_gross_energy: 
        data_total += np.array(data_all_abs_plot["data"][siec]["y"])

    for siec in colors_siecs_gross_energy: 
        data_all_rel_plot["data"][siec] = {"x": data_all_abs_plot["data"][siec]["x"],
                          "y": data_all_abs_plot["data"][siec]["y"]*100/data_total}    
            

    plot_single_go(title = "<b>AT gross inland consumption</b>: shares",
                  filename = "AT_timeseries_gross_inland_consumption_share",
                  unit = "Share [%]", 
                  data_plot = data_all_rel_plot,
                  time_res = "yearly",
                  show_plot = show_plot,
                  colors = list([colors_siecs_gross_energy[label] for label in colors_siecs_gross_energy]),
                  source_text = "eurostat energy balances (nrg_bal_c)",
                  plot_type = "area",
                  plotmax_fac = 1)
        
    plot_single_go(title = "<b>AT gross inland consumption</b>: absolute",
                  filename = "AT_timeseries_gross_inland_consumption_absolute",
                  unit = "Energy (TWh)", 
                  data_plot = data_all_abs_plot,
                  time_res = "yearly",
                  show_plot = show_plot,
                  colors = list([colors_siecs_gross_energy[label] for label in colors_siecs_gross_energy]),
                  source_text = "eurostat energy balances (nrg_bal_c)",
                  plot_type = "area")
    
    
    ### SECTORIAL FINAL ENERGY 
    siecs_final_energy = {"Natural gas": ["Natural gas"],
              "Oil": ["Oil and petroleum products (excluding biofuel portion)"],
              "Coal": ["Solid fossil fuels"],
              "Biomass": ["Primary solid biofuels", "Charcoal", "Pure biogasoline",
                          "Blended biogasoline", "Pure biodiesels", "Blended biodiesels",
                          "Pure bio jet kerosene", "Blended bio jet kerosene", "Other liquid biofuels",
                          "Biogases"],
              "Electricity": ["Electricity"],
              "District Heat": ["Heat"],
              "Other": ["Manufactured gases", "Industrial waste (non-renewable)", 
                        "Geothermal", "Solar thermal", "Ambient heat (heat pumps)",
                        ]}
    
    set2 = px.colors.qualitative.Dark2
    colors_siecs_final_energy ={"Natural gas": set2[5],
                    "Oil": set2[6],
                    "Coal": set2[7],
                    "Biomass": set2[4],
                    "Electricity": set2[2],
                    "District Heat": set2[3],
                    "Other": set2[1]}    
    
    
    ### SECTORS 
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
                              },
                "AT-total": {"file": "total",
                          "en_bal": {"Total": "Available for final consumption"}}
                }

    
    
    
    for sector in sectors: 
        data_all_abs = {}
        
        for bal in sectors[sector]["en_bal"]:
            data_all_abs[bal] = filter_eurostat_energy_balance(bals = [sectors[sector]["en_bal"][bal]],
                                                                siecs = siecs_final_energy)
        
        data_all_abs_plot = {"Total": {"data": {}}}
        
        for bal in data_all_abs: 
            data_all_abs_plot[bal] = {"data": {}}
            for siec in siecs_final_energy: 
                data_all_abs_plot[bal]["data"][siec] = data_all_abs[bal]["data"][siec]

        ### Total of sector               
        if "Total" not in data_all_abs: 
            for siec in data_all_abs_plot[bal]["data"]: 
                total_sector = np.zeros(len(data_all_abs[bal]["data"]["Oil"]["x"]))
                for bal in data_all_abs_plot:
                    if bal not in ["Total"]: 
                        total_sector += data_all_abs_plot[bal]["data"][siec]["y"]
                data_all_abs_plot["Total"]["data"][siec] =  {"x": data_all_abs_plot[bal]["data"][siec]["x"],
                                                              "y": total_sector}
                   
                    
        data_all_rel_plot = {}
        for bal in data_all_abs_plot:
            data_all_rel_plot[bal] = {"data": {}}
            
            data_total = np.zeros(len(data_all_abs_plot[bal]["data"]["Oil"]["x"]))
            for siec in colors_siecs_final_energy: 
                data_total += np.array(data_all_abs_plot[bal]["data"][siec]["y"])
    
            for siec in colors_siecs_final_energy: 
                data_all_rel_plot[bal]["data"][siec] = {"x": data_all_abs_plot[bal]["data"][siec]["x"],
                                  "y": data_all_abs_plot[bal]["data"][siec]["y"]*100/data_total}    
                
                
        plot_single_go(title = "<b>%s</b>: final energy use - shares" %(sector),
                      filename = "AT_timeseries_%s_final_energy_use_share" %(sectors[sector]["file"]),
                      unit = "Share [%]", 
                      data_plot = data_all_rel_plot,
                      time_res = "yearly",
                      show_plot = show_plot,
                      colors = list([colors_siecs_final_energy[label] for label in colors_siecs_final_energy]),
                      source_text = "eurostat energy balances (nrg_bal_c)",
                      plot_type = "area_button",
                      plotmax_fac = 1)
            
        plot_single_go(title = "<b>%s</b>: final energy use" %(sector),
                      filename = "AT_timeseries_%s_final_energy_use" %(sectors[sector]["file"]),
                      unit = "Energy (TWh)", 
                      data_plot = data_all_abs_plot,
                      time_res = "yearly",
                      show_plot = show_plot,
                      colors = list([colors_siecs_final_energy[label] for label in data_all_abs_plot[bal]["data"]]),
                      source_text = "eurostat energy balances (nrg_bal_c)",
                      plot_type = "area_button")

        


if __name__ == "__main__": 
    print("Plotting ...")
    plot()
    
    data = filter_eurostat_energy_balance(bals = ["Gross inland consumption"],
                                                  siecs = {"Total": ["Total"]})
