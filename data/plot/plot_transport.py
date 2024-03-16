# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:00:34 2024

@author: Bernhard
"""

import plotly.io as pio
pio.renderers.default = 'browser'
import plotly.express as px

from plot_single import plot_single_go
from utils.filter import filter_eurostat_monthly
from utils.filter import filter_car_registrations
from utils.filter import filter_eurostat_cars
from utils import filter_national_inventory

set2 = px.colors.qualitative.Dark2
colors_cars = {"Electric": set2[0],
          "Hybrid plugin": set2[1],
          "Hybrid": set2[2],
          "Diesel": set2[6],
          "Gasoline": set2[7],
          "Other": set2[5]}


def get_car_vectors(data): 
    data_rel = {"data": {}}
    data_abs = {"data": {}}

    for cat in ["Electric", "Hybrid plugin", "Hybrid", "Diesel", "Gasoline", "Other"]: 
        if cat != "Total": 
            data_rel["data"][cat] = {"x": list(data[cat].keys()),
                             "y": list(data[cat][time]*100/data["Total"][time] for time in data[cat])}
            data_abs["data"][cat] = {"x": list(data[cat].keys()),
                             "y": list(data[cat][time] for time in data[cat])}
            
    return data_rel, data_abs 
    


def plot():

    ### Road petroleum products 
    data_gasoline = filter_eurostat_monthly(name = "oil",
                                      code = "NRG_CB_OILM",
                                  start_year = 2010,
                              options = {"unit": "THS_T",
                                        "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                        "siec": "Motor gasoline [O4652]"},
                              unit = "THS_T", movmean = 12) 
    
    data_diesel = filter_eurostat_monthly(name = "oil",
                                    code = "NRG_CB_OILM",
                                  start_year = 2010,
                              options = {"unit": "THS_T",
                                        "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                        "siec": "Road diesel [O46711]"},
                              unit = "THS_T", movmean = 12)    

    data_plot = {"data": {"Diesel monthly": data_diesel["data"]["Monthly"],
                          "Diesel 12-Month average": data_diesel["data"]["12-Month average"],
                          "Gasoline monthly": data_gasoline["data"]["Monthly"],
                          "Gasoline 12-Month average": data_gasoline["data"]["12-Month average"]
                        },
                  "meta": {"code": "%s | %s" %(data_gasoline["meta"]["code"],
                                              data_diesel["meta"]["code"])
                          }
                  }
    plot_single_go(title = "<b>Road fuels</b>: monthly consumption (incl. biofuels)", 
                    filename = "AT_timeseries_road_fuels_consumption",
                    unit = "Fuel (thousand tons)", 
                    data_plot=data_plot,
                    legend_inside = False)    


    ### Road bio-petroleum products 
    data_gasoline = filter_eurostat_monthly(name = "oil",
                                  start_year = 2010,
                                  code = "NRG_CB_OILM",
                              options = {"unit": "THS_T",
                                        "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                        "siec": "Blended biogasoline [R5210B]"},
                              unit = "THS_T", movmean = 12) 
    
    data_diesel = filter_eurostat_monthly(name = "oil",
                                  start_year = 2010,
                                  code = "NRG_CB_OILM",
                              options = {"unit": "THS_T",
                                        "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                        "siec": "Blended biodiesels [R5220B]"},
                              unit = "THS_T", movmean = 12)    
    
    data_plot = {"data": {"Blended biodiesel monthly": data_diesel["data"]["Monthly"],
                          "Blended biodiesel 12-Month average": data_diesel["data"]["12-Month average"],
                          "Blended biogasoline monthly": data_gasoline["data"]["Monthly"],
                          "Blended biogasoline 12-Month average": data_gasoline["data"]["12-Month average"]
                          },
                "meta": {"code": "%s | %s" %(data_gasoline["meta"]["code"],
                                              data_diesel["meta"]["code"])
                          }
                }
            
    plot_single_go(title = "<b>Road biofuels</b>: monthly consumption (incl. biofuels)", 
                    filename = "AT_timeseries_road_biofuels_consumption",
                    unit = "Fuel (thousand tons)", 
                    data_plot=data_plot,
                    legend_inside = False)   
    
    ### Aviation fuel 
    data_oil = filter_eurostat_monthly(name = "oil",
                                  code = "NRG_CB_OILM",
                                  start_year = 2010,
                              options = {"unit": "THS_T",
                                        "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                        "siec": "Kerosene-type jet fuel [O4661]"},
                              unit = "THS_T", movmean = 12)

    plot_single_go(title = "<b>Kerosene / Aviation fuel</b>: monthly consumption Austria (incl. biofuels)", 
                    filename = "AT_timeseries_kerosene_consumption",
                    unit = "Fuel (thousand tons)", 
                    data_plot=data_oil)    


    
    ### Car registrations data 
    data = filter_car_registrations()
    data_rel, data_abs = get_car_vectors(data) 
    
    
    plot_single_go(title = "<b>Fuel type share</b>: new car registrations",
                  filename = "AT_timeseries_share_fuel_new_cars",
                  unit = "Share [%]", 
                  data_plot = data_rel,
                  show_plot = False,
                  colors = list([colors_cars[label] for label in colors_cars]),
                  source_text = "eurostat (road_eqr_carpda) & Statistik Austria",
                  plot_type = "area",
                  plotmax_fac = 1)
    
    plot_single_go(title = "<b>Fuel type absolute number</b>: new car registrations",
                  filename = "AT_timeseries_number_fuel_new_cars",
                  unit = "Number", 
                  data_plot = data_abs,
                  show_plot = False,
                  colors = list([colors_cars[label] for label in colors_cars]),
                  source_text = "eurostat (road_eqr_carpda) & Statistik Austria",
                  plot_type = "area")
    
    
    # ### Car stock data 
    data = filter_eurostat_cars(file = "AT_cars_road_eqs_carpda")
    data_rel, data_abs = get_car_vectors(data) 
    
    plot_single_go(title = "<b>Fuel type share</b>: registered cars",
                  filename = "AT_timeseries_share_fuel_stock_cars",
                  unit = "Share [%]", 
                  data_plot = data_rel,
                  time_res = "yearly",
                  show_plot = False,
                  colors = list([colors_cars[label] for label in colors_cars]),
                  source_text = "eurostat (road_eqs_carpda)",
                  plot_type = "area",
                  plotmax_fac = 1)
        
    plot_single_go(title = "<b>Fuel type absolute number</b>: registered cars",
                  filename = "AT_timeseries_number_fuel_stock_cars",
                  unit = "Number", 
                  data_plot = data_abs,
                  time_res = "yearly",
                  show_plot = False,
                  colors = list([colors_cars[label] for label in colors_cars]),
                  source_text = "eurostat (road_eqs_carpda)",
                  plot_type = "area")
    
    
    ### Lorries registrations data 
    data = filter_eurostat_cars(file = "AT_lorries_road_eqr_lormot",
                                options = {"vehicle": "VG_LE3P5"})
    data_rel, data_abs = get_car_vectors(data) 
    
    plot_single_go(title = "<b>Fuel type share</b>: new lorry (≤3.5t) registrations",
              filename = "AT_timeseries_share_fuel_new_lorries_le3p5",
              unit = "Share [%]", 
              data_plot = data_rel,
              time_res = "yearly",
              show_plot = False,
              colors = list([colors_cars[label] for label in colors_cars]),
              source_text = "eurostat (road_eqr_lormot)",
              plot_type = "area",
              plotmax_fac = 1)
    
    plot_single_go(title = "<b>Fuel type absolute number</b>: new lorry (≤3.5t) registrations",
              filename = "AT_timeseries_number_fuel_new_lorries_le3p5",
              unit = "Number", 
              data_plot = data_abs,
              time_res = "yearly",
              show_plot = False,
              colors = list([colors_cars[label] for label in colors_cars]),
              source_text = "eurostat (road_eqr_lormot)",
              plot_type = "area")   
    

    data = filter_eurostat_cars(file = "AT_lorries_road_eqr_lormot",
                                options = {"vehicle": "VG_GT3P5"})
    data_rel, data_abs = get_car_vectors(data) 
    
    plot_single_go(title = "<b>Fuel type share</b>: new lorry (>3.5t) registrations",
              filename = "AT_timeseries_share_fuel_new_lorries_gt3p5",
              unit = "Share [%]", 
              data_plot = data_rel,
              time_res = "yearly",
              show_plot = False,
              colors = list([colors_cars[label] for label in colors_cars]),
              source_text = "eurostat (road_eqr_lormot)",
              plot_type = "area",
              plotmax_fac = 1)
    
    plot_single_go(title = "<b>Fuel type absolute number</b>: new lorry (>3.5t) registrations",
              filename = "AT_timeseries_number_fuel_new_lorries_gt3p5",
              unit = "Number", 
              data_plot = data_abs,
              time_res = "yearly",
              show_plot = False,
              colors = list([colors_cars[label] for label in colors_cars]),
              source_text = "eurostat (road_eqr_lormot)",
              plot_type = "area")   
    

    
if __name__ == "__main__": 
    print("Plotting ...")
    plot()
    