# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 19:04:15 2024

@author: Bernhard
"""

from datetime import datetime, timedelta  
import pandas as pd 
import numpy as np 
import plotly.express as px
import matplotlib.pyplot as plt 
import os 

from plot_single import plot_single_go
from utils.filter import filter_eurostat_monthly
from utils import filter_fossil_extrapolation
from utils.filter import filter_uba_sectoral_emisssions


### natural gas must be converted from TJ_GCV to TJ_NCV 
TJ_GCV_to_1000m3 = 0.03914 #TJ_GCV / 1000m3 
TJ_NCV_to_1000m3 = 0.03723 #TJ_NCV / 1000M3 


fossils = {"Natural gas": {"file": "gas",
                           "save_name": "natural_gas",
                           "code": "NRG_CB_GASM",
                           "options":  {"unit": "TJ_GCV",
                                        "nrg_bal": "Inland consumption - calculated as defined in MOS GAS [IC_CAL_MG]"},
                           "NCV": TJ_NCV_to_1000m3/TJ_GCV_to_1000m3/1000,   #TJ_NCV / (1000*TJ_GCV) 
                           "em_fac": 55.4},  #t_CO2 / TJ 
           "Gasoline": {"file": "oil",
                        "save_name": "gasoline",
                        "code": "NRG_CB_OILM",
                        "options":  {"unit": "THS_T",
                                     "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                     "siec": "Motor gasoline [O4652]"},
                        "NCV": 0.0418,
                        "em_fac": 71.3},
            "Diesel": {"file": "oil",
                         "save_name": "diesel",
                         "code": "NRG_CB_OILM",
                         "options":  {"unit": "THS_T",
                                      "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                      "siec": "Road diesel [O46711]"},
                         "NCV": 0.0424,
                         "em_fac": 71.3},
            "Heating gas oil": {"file": "oil",
                         "save_name": "heating_oil",
                         "code": "NRG_CB_OILM",
                         "options":  {"unit": "THS_T",
                                      "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                      "siec": "Heating and other gasoil [O46712]"},
                         "NCV": 0.0428,
                         "em_fac": 75},
            "Refinery gas": {"file": "oil",
                         "save_name": "refinery_gas",
                         "code": "NRG_CB_OILM",
                         "options":  {"unit": "THS_T",
                                      "nrg_bal": "Refinery fuel [RF]",
                                      "siec": "Refinery gas [O4610]"},
                         "NCV": 0.0306,
                         "em_fac": 64},
            "Hard coal - electricity sector": {"file": "coal",
                         "save_name": "hard_coal_electricity",
                         "code": "NRG_CB_SFFM",
                         "options":  {"unit": "THS_T",
                                      "nrg_bal": "Transformation input - electricity and heat generation - main activity producers [TI_EHG_MAP]",
                                      "siec": "Hard coal [C0100]"},
                         "NCV": 0.0299,
                         "em_fac": 95},
            "Hard coal - industry sector": {"file": "coal",
                         "save_name": "hard_coal_industry",
                         "code": "NRG_CB_SFFM",
                         "options":  {"unit": "THS_T",
                                      "nrg_bal": "Final consumption - industry sector [FC_IND]",
                                      "siec": "Hard coal [C0100]"},
                         "NCV": 0.0299,
                         "em_fac": 84},
            "Hard coal - coke ovens": {"file": "coal",
                         "save_name": "hard_coal_coke_ovens",
                         "code": "NRG_CB_SFFM",
                         "options":  {"unit": "THS_T",
                                      "nrg_bal": "Transformation input - coke ovens [TI_CO]",
                                      "siec": "Hard coal [C0100]"},
                         "NCV": 0.0299,
                         "em_fac": 84},
            "Coke oven coke": {"file": "coal",
                         "save_name": "coke_oven_coke",
                         "code": "NRG_CB_SFFM",
                         "options":  {"unit": "THS_T",
                                      "nrg_bal": "Gross inland deliveries - calculated [GID_CAL]",
                                      "siec": "Coke oven coke [C0311]"},
                         "NCV": 0.0282,
                         "em_fac": 94.6},
            }


# fossils = {"Natural gas": {"file": "gas",
#                             "save_name": "natural_gas",
#                             "code": "NRG_CB_GASM",
#                             "options":  {"unit": "TJ_GCV",
#                                         "nrg_bal": "Inland consumption - calculated as defined in MOS GAS [IC_CAL_MG]"},
#                             "NCV": TJ_NCV_to_1000m3/TJ_GCV_to_1000m3/1000,   #TJ_NCV / (1000*TJ_GCV) 
#                             "em_fac": 55.4}}  #t_CO2 / TJ 


dark2 = px.colors.qualitative.Dark2
set2 = px.colors.qualitative.Set2
colors  = {"yearly_to": dark2[0],
            "yearly_from": set2[0],
            "extrapolated": set2[1]}


def separate_bios(data_monthly, f): 
    """ based on diesel and gasoline data, load also biofuel data and subtract them from 
    to be plotted data """ 
    
    if f == "Diesel": siec = "Blended biodiesels [R5220B]"
    if f == "Gasoline": siec = "Blended biogasoline [R5210B]"
    data_monthly_bio = filter_eurostat_monthly(name = "oil",
                                           code = "NRG_CB_OILM",
                                           options = {"unit": "THS_T",
                                                      "nrg_bal": "Gross inland deliveries - observed [GID_OBS]",
                                                      "siec": siec},
                                           unit = "THS_T",
                                           movmean = 12)
    movmean = 12 
    times_plot = data_monthly_bio["data"]["Monthly"]["x"]
    times_plot_mean = data_monthly_bio["data"]["%i-Month average" %(movmean)]["x"]
    values = np.array(data_monthly["data"]["Monthly"]["y"])
    values_mean = np.array(data_monthly["data"]["%i-Month average" %(movmean)]["y"])
    values_bio = np.array(data_monthly_bio["data"]["Monthly"]["y"])
    values_bio_mean = np.array(data_monthly_bio["data"]["%i-Month average" %(movmean)]["y"])
    
    data_monthly = {"data": {"%s Monthly" %(f): {"x": times_plot,
                                                 "y": values-values_bio},
                             "%s %i-Month average" %(f, movmean): {"x": times_plot_mean,
                                                                           "y": values_mean-values_bio_mean},
                             "Bio-%s Monthly " %(f): {"x": times_plot,
                                                     "y": values_bio},
                             "Bio-%s %i-Month average" %(f, movmean): {"x": times_plot_mean,
                                                                               "y": values_bio_mean},                                     
                             },
                    "meta": {"code": "NRG_CB_OILM"}
                    }
    return data_monthly 


def extrapolate_fossil_fuels(plot = True):
    """ extrapolate the consumption data of fossil fuels to the end of year based on historic factors """
    
    consumption = {}
    
    for f in fossils: 
        ### MONTHLY 
        data_monthly = filter_eurostat_monthly(name = fossils[f]["file"],
                                               code = fossils[f]["code"],
                                               options = fossils[f]["options"],
                                               unit = fossils[f]["options"]["unit"],
                                               movmean = 12)
        legend_inside = True 
        if f in ["Diesel", "Gasoline"]: 
            legend_inside = False 
            data_monthly  = separate_bios(data_monthly, f) 

        if plot: 
            plot_single_go(title = "<b>%s</b>: monthly consumption" %(f), 
                            filename = "AT_timeseries_consumption_%s_monthly" %(fossils[f]["save_name"]),
                            unit =  "Consumption (%s)" %(fossils[f]["options"]["unit"]),
                            data_plot=data_monthly, 
                            unit_fac = 1,
                            legend_inside = legend_inside)
        
        ### rename bio values so that they can be processed 
        if f in ["Diesel", "Gasoline"]: 
            data_monthly["data"]["Monthly"] = data_monthly["data"]["%s Monthly" %(f)]
        
        
        ### YEARLY AND EXTRAPOLATION 
        data_raw = filter_fossil_extrapolation.cut_data_fossil(data_monthly)
        data_extrapolated = filter_fossil_extrapolation.extrapolate_data_fossil(data_raw)
        
        years = [year for year in data_raw["values_year_to_last_month"]]
        times_years = pd.date_range(start = datetime(year = years[0], month = 1, day =1),
                              end = datetime(year = years[-1], month = 1, day = 1),
                              freq="YS")
        
        ### values up to latest month 
        values_year_to_last_month = [data_raw["values_year_to_last_month"][year] for year in data_raw["values_year_to_last_month"]]
        last_month = datetime.strptime(str(data_raw["meta"]["last_month"]), "%m")
        data = {"data": {"Observed: Jan - %s" %(last_month.strftime("%b")):
                         {"x": times_years,
                          "y": np.array(values_year_to_last_month)},
                         }}
        colors_plot = [colors["yearly_to"]] 
            
        if last_month.month != 12: 
            ### values from latest month on 
            values_year_from_last_month = [data_raw['values_year_from_last_month'][year] for year in data_raw['values_year_from_last_month']]
            last_month_plus = datetime.strptime(str(data_raw["meta"]["last_month"]+1), "%m")
            data["data"]["Observed: %s - Dec" %(last_month_plus.strftime("%b"))] =  {
                "x": times_years,
                "y": np.array(values_year_from_last_month)}
            colors_plot.append(colors["yearly_from"])
            
            ### extrapolation data from latest month on 
            values_extrapolated = np.zeros(len(times_years))
            values_extrapolated[-1] = data_extrapolated["extrapolated_year"]-data_extrapolated["consumption_to_month"]
            data["data"]["Extrapolated: %s - Dec" %(last_month_plus.strftime("%b"))] =  {
                "x": times_years,
                "y": np.array(values_extrapolated)}
            colors_plot.append(colors["extrapolated"])
            
        ### sum up consumption data for emission estimation 
        yearly_consumptions = (np.array(values_year_to_last_month)+
                               np.array(values_year_from_last_month) + 
                               np.array(values_extrapolated)) 
        
        data["data"]["Total"] = {"x": times_years,
                                 "y": yearly_consumptions}
        
        if plot: 
            plot_single_go(title = "<b>%s</b>: yearly consumption" %(f),
                          filename = "AT_timeseries_consumption_%s_yearly" %(fossils[f]["save_name"]),
                          unit = "Conumption (%s)" %(fossils[f]["options"]["unit"]),
                          data_plot = data,
                          time_res = "yearly",
                          colors = colors_plot,
                          show_plot = False,
                          unit_fac= 1, 
                          source_text = "eurostat (%s)" %(fossils[f]["code"]),
                          info_text = "Extrapolations based on monthly available data scaled with past trends",
                          plot_type = "bar")
    
        consumption[f] = {"data": {times_years[t]: yearly_consumptions[t] for t in range(len(times_years))},
                          "fac_mean": data_extrapolated["fac_mean"],
                          "std_energy": data_extrapolated["std_energy"]}
        
        
    return consumption 
    
    
 

def extrapolate_emissions_by_cons(consumption, 
                          year_extrapolate = 2023, 
                          train_start = 2008,
                          train_end = 2022,
                          plot = False): 

    times_train = pd.date_range(start = datetime(year = train_start, month = 1, day =1),
                          end = datetime(year = train_end, month = 1, day = 1),
                          freq="YS")
    
    emissions_fuels = {}
    for f in consumption: 
        emissions_fuels[f] = []
        for t in times_train:
            emissions_fuels[f].append(consumption[f]["data"][t]*fossils[f]["NCV"]*fossils[f]["em_fac"]/1000)


    emissions_train = np.zeros(len(times_train))
    for f in fossils: 
        emissions_train = emissions_train + np.array(emissions_fuels[f])
                               
    emissions_real = filter_uba_sectoral_emisssions()
    emissions_energy_years = []
    for time in times_train: 
        ind = emissions_real["data"]["Transport"]["x"].index(time)
        emissions_energy_years.append(emissions_real["data"]["Transport"]["y"][ind]+
                                     emissions_real["data"]["Buildings"]["y"][ind]+
                                     emissions_real["data"]["Energy & Industry"]["y"][ind])
        
    facs = []
    for t in range(len(times_train)):
        e_real = emissions_energy_years[t]
        e_train = emissions_train[t]
        facs.append(e_real/e_train)
    
    fac_mean = np.mean(np.array(facs))
    std_estimator = np.sqrt(np.var(facs)*len(facs)/(len(facs)-1.5))
    
    ### ESTIMATE EMISSIONS AND EXTRAPOLATE 
    emissions_energy_model = 0
    time_project = datetime(year = year_extrapolate, month= 1, day=1)
    for f in fossils: 
        emissions_energy_model += consumption[f]["data"][time_project]*fossils[f]["NCV"]*fossils[f]["em_fac"]/1000
    emissions_energy_projected = emissions_energy_model*fac_mean
    
    ### ESTIMATE STD (BOTH CONTRIBUTIONS)
    std_emisssion_projected =  emissions_energy_projected*std_estimator
    
    std_consumption_projected = 0
    for f in consumption: 
        ### in case no projection was made to projection year, set error to zero (full data available)
        time_project_plus_one = datetime(year = year_extrapolate+1, month= 1, day=1)
        if time_project_plus_one in consumption[f]["data"]:
            pass 
        else:
            std_consumption_projected += (consumption[f]["std_energy"]*fossils[f]["NCV"]*fossils[f]["em_fac"]/1000 
                                     * fac_mean)
            
    total_std = std_emisssion_projected + std_consumption_projected 
    
    ### for agriculture, fluorinated gases and waste, extrapolate current emission trends 
    emissions_rest_years = (np.array(emissions_real["data"]["Agriculture"]["y"]) + 
                            np.array(emissions_real["data"]["Waste"]["y"]) + 
                            np.array(emissions_real["data"]["Fluorinated Gases"]["y"])) 
    
    emissions_energy_years = (np.array(emissions_real["data"]["Transport"]["y"]) + 
                            np.array(emissions_real["data"]["Buildings"]["y"]) + 
                            np.array(emissions_real["data"]["Energy & Industry"]["y"]))     
    
    times_historic = emissions_real["data"]["Agriculture"]["x"]
    emissions_historic = emissions_energy_years+emissions_rest_years
    ind_last = times_historic.index(times_train[-1])
    
    emission_rest_trend_year = (emissions_rest_years[ind_last]-emissions_rest_years[ind_last-3])/3    
    emissions_rest_projected = emissions_rest_years[ind_last] + emission_rest_trend_year

    projected_emissions = [emissions_historic[ind], emissions_energy_projected+emissions_rest_projected]
    times_projected = [times_historic[ind],time_project]

    times_total = times_historic + [time_project]
    emissions_energy_sectors = list(emissions_energy_years) + [emissions_energy_projected]
    emissions_rest_sectors = list(emissions_rest_years) + [emissions_rest_projected]
    
    data_plot = {"data": {"Energy sectors": {"x": times_total,
                                              "y": emissions_energy_sectors},
                          "Other sectors": {"x": times_total,
                                            "y": emissions_rest_sectors},
                          "Projeted emissions": {"x": times_projected,
                                                 "y": projected_emissions},
                          "Historic emissions": {"x": times_historic,
                                                 "y": emissions_historic}
                          }}
    
    data_plot["meta"] = {"uncertainty": {"Projeted emissions": [0, total_std]},
                         "areas": ["Energy sectors", "Other sectors"]}
    
    if plot:
        plot_single_go(title = "<b>Austrian GHG emissions</b>: projection",
                      filename = "AT_timeseries_emissions_projection_yearly",
                      unit = "Emissions (CO2e)",
                      data_plot = data_plot,
                      time_res = "yearly",
                      show_plot = False,
                      unit_fac= 1, 
                      source_text = "Umweltbundesamt, eurostat & own projection",
                      plot_type = "line")
    
    data_out = {"emissions_energy_projected": emissions_energy_projected,
                "std_emission_projected": std_emisssion_projected,
                "std_consumption_projected": std_consumption_projected,
                "emissions_rest_projected": emissions_rest_projected}
    
    
    return data_out
    


def extrapolate_emissions(plot = True): 
    consumption = extrapolate_fossil_fuels(plot = False)
    extrapolate_emissions_by_cons(consumption, plot = plot) 
    

def plot_extrapolation_demo(): 
    """ plot a simple demo to show how the extrapolation of fossil fuel consumption works """ 
    year_plot = 2022
    
    ### commodity extrapolation demo 
    demos = ["Natural gas", "Diesel", "Coke oven coke"]
    data_plot = {}
    
    for f in demos: 
        data_monthly = filter_eurostat_monthly(name = fossils[f]["file"],
                                                code = fossils[f]["code"],
                                                options = fossils[f]["options"],
                                                unit = fossils[f]["options"]["unit"],
                                                movmean = 12)
        data_raw = filter_fossil_extrapolation.cut_data_fossil(data_monthly)
                
        data_plot[f] = {}
        last_months = np.arange(1,13)
        data_plot[f] = {"last_months": last_months,
                        "extrapolated_data": [],
                        "std_data": [],
                        "actual_consumption_year": [data_raw["values_year"][year_plot] for i in range(12)],
                        "actual_consumption_to_month": [],
                        "facs_mean": []}
        
        for last_month in last_months: 
            data = filter_fossil_extrapolation.extrapolate_data_fossil(data_raw, 
                                            last_year_raw = year_plot, 
                                            last_month_raw = last_month)
            
            data_plot[f]["extrapolated_data"].append(data["extrapolated_year"])
            data_plot[f]["std_data"].append(data["std_energy"])
            data_plot[f]["actual_consumption_to_month"].append(data["consumption_to_month"])
            data_plot[f]["facs_mean"].append(data["fac_mean"])
        data_plot[f]["unit"] = fossils[f]["options"]["unit"]
    
    filter_fossil_extrapolation.plot_data_fossils(data_plot, 
                                                  year_plot = year_plot)
    
    ### emissions estimations demo 
    data_out = {}
    last_months = np.arange(1,13)
    for last_month in last_months: 
        print("Projecting from month %i/12" %(last_month))
        consumption = {}
        for f in fossils: 
            data_monthly = filter_eurostat_monthly(name = fossils[f]["file"],
                                                    code = fossils[f]["code"],
                                                    options = fossils[f]["options"],
                                                    unit = fossils[f]["options"]["unit"],
                                                    movmean = 12)
            if f in ["Diesel", "Gasoline"]: 
                data_monthly  = separate_bios(data_monthly, f) 
                data_monthly["data"]["Monthly"] = data_monthly["data"]["%s Monthly" %(f)]
        
            data_raw = filter_fossil_extrapolation.cut_data_fossil(data_monthly)
            data_extrapolated = filter_fossil_extrapolation.extrapolate_data_fossil(data_raw, 
                                            last_year_raw = year_plot, 
                                            last_month_raw = last_month)
            times_years = pd.date_range(start = datetime(year = 2008, month = 1, day =1),
                                  end = datetime(year = year_plot, month = 1, day = 1),
                                  freq="YS")
            
            values_year_to_last_month = [data_raw["values_year_to_last_month"][time.year] for time in times_years]
            values_year_from_last_month = [data_raw['values_year_from_last_month'][time.year] for time in times_years]
            yearly_consumptions = (np.array(values_year_to_last_month)+
                                    np.array(values_year_from_last_month))
            yearly_consumptions[-1] = data_extrapolated["extrapolated_year"] 

            consumption[f] =  {"data": {times_years[t]: yearly_consumptions[t] for t in range(len(times_years))},
                              "fac_mean": data_extrapolated["fac_mean"],
                              "std_energy": data_extrapolated["std_energy"]}
            
        data = extrapolate_emissions_by_cons(consumption, 
                                      year_extrapolate = year_plot,
                                      train_start = 2008,
                                      train_end = year_plot-1,
                                      plot = False)    
            
        data_out[last_month] = {"emissions_model": data["emissions_rest_projected"]+data["emissions_energy_projected"],
                        "std_emission_projected":  data["std_emission_projected"],
                        "std_consumption_projected": data["std_consumption_projected"]}

    
    emissions_real = filter_uba_sectoral_emisssions()
    emissions_year = 0
    time_projected = times_years[-1]
    ind = emissions_real["data"]["Transport"]["x"].index(time_projected)
    for sector in  ["Transport", "Energy & Industry", "Agriculture", "Buildings", "Waste", "Fluorinated Gases"]:
        emissions_year += emissions_real["data"][sector]["y"][ind]

    projected_emissions = np.array([data_out[month]["emissions_model"] for month in last_months])
    error_emission_projection = np.array([data_out[month]["std_emission_projected"] for month in last_months])
    error_consumption_projection = np.array([data_out[month]["std_consumption_projected"] for month in last_months])
    emission_errors = error_emission_projection + error_consumption_projection

    fig,ax = plt.subplots(2,1)
    fig.set_size_inches(7,2*3)
    ax[0].plot(last_months, np.ones(len(last_months))*emissions_year, label = "Actual emissions") 
    ax[0].plot(last_months, projected_emissions, label = "Projected emissions") 

    ax[0].fill_between(last_months, 
                        projected_emissions-emission_errors/2,
                        projected_emissions+emission_errors/2,
                        alpha = 0.3,
                        label = "Estimated standard deviation")
    
    ax[0].set_title("CO2 emission extrapolatoin of 2022 using monthly data") 
    ax[0].set_ylim([0, emissions_year*1.2])
    ax[0].legend() 
    ax[0].set_ylabel("CO2 emissions (Mt_CO2e)")
    ax[0].grid() 


    ax[1].plot(last_months, error_consumption_projection, label = "Uncertainty fossil fuel consumtion extrapolation") 
    ax[1].plot(last_months, error_emission_projection, label = "Uncertainty emission scaling") 
    ax[1].set_ylim([0, max([max(error_consumption_projection),
                            max(error_emission_projection)])*1.1])
    ax[1].legend() 
    ax[1].set_ylabel("CO2 emissions (Mt_CO2e)")
    ax[1].set_xlabel("Month")
    ax[1].grid() 
    
    plt.tight_layout() 
    plt.savefig(os.path.join(os.path.dirname(__file__), 
                             "../../docs/assets/images/emissions_projection_2022.png"), dpi = 400)
    

    return data_out 
    

def plot_emission_estimate_demo(): 
    emissions = {}
    end_year = 2022 
    start_year = 2008
    times = pd.date_range(start = datetime(year = start_year, month = 1, day =1),
                          end = datetime(year = end_year, month = 1, day = 1),
                          freq="YS")
                              
    for f in fossils: 
        ### MONTHLY 
        data_monthly = filter_eurostat_monthly(name = fossils[f]["file"],
                                               code = fossils[f]["code"],
                                               options = fossils[f]["options"],
                                               unit = fossils[f]["options"]["unit"],
                                               movmean = 12)
        if f in ["Diesel", "Gasoline"]: 
            data_monthly = separate_bios(data_monthly, f)
            data_monthly["data"]["Monthly"] = data_monthly["data"]["%s Monthly" %(f)]

        
        ### YEARLY AND EXTRAPOLATION 
        data_raw = filter_fossil_extrapolation.cut_data_fossil(data_monthly)
        
        emissions_years = []
        for time in times: 
            emissions_years.append(data_raw["values_year"][time.year])
        emissions[f] = np.array(emissions_years)*fossils[f]["NCV"]*fossils[f]["em_fac"]/1000
        

    total_emissions = np.zeros(len(times))
    for f in fossils: 
        total_emissions = total_emissions +  emissions[f]
        
    emissions_real = filter_uba_sectoral_emisssions()
    emissions_energy_years = []
    for time in times: 
        ind = emissions_real["data"]["Transport"]["x"].index(time)
        emissions_energy_years.append(emissions_real["data"]["Transport"]["y"][ind]+
                                     emissions_real["data"]["Buildings"]["y"][ind]+
                                     emissions_real["data"]["Energy & Industry"]["y"][ind])



    facs = []
    for t in range(len(times)):
        actual_emissions = emissions_energy_years[t]
        calculated_emissions = total_emissions[t]
        facs.append(actual_emissions/calculated_emissions)
    
    fac_mean = np.mean(np.array(facs))
    std_estimator = np.sqrt(np.var(facs)*len(facs)/(len(facs)-1.5))
    
    emissions_extrapolated = np.zeros(len(times))
    emission_errors = np.zeros(len(times))
    for t in range(len(times)):
        emissions_extrapolated[t] = total_emissions[t]*fac_mean
        emission_errors[t] = total_emissions[t]*std_estimator
        
    fig,ax = plt.subplots(2,1)
    fig.set_size_inches(7,2*3)

    ax[0].plot(times, total_emissions, label = "Estimated emissions") 
    ax[0].plot(times, emissions_energy_years, label = "Actual emissions Energy-sectors") 
    ax[0].legend() 
    ax[0].set_ylim([0, max(emissions_energy_years)*1.1])
    ax[0].set_ylabel("CO2 emissions (Mt)")
    ax[0].grid() 
    
    
    ax[1].plot(times, emissions_extrapolated, label = "Scaled emissions") 
    ax[1].plot(times, emissions_energy_years, label = "Actual emissions Energy-sectors") 

    ax[1].fill_between(times, 
                          emissions_extrapolated-emission_errors,
                          emissions_extrapolated+emission_errors,
                          alpha = 0.3,
                          label = "Scaling standard deviation")
    ax[1].set_ylim([0, max(emissions_energy_years)*1.1])
    ax[1].legend() 
    ax[1].set_ylabel("CO2 emissions (Mt)")
    ax[1].set_xlabel("Year")
    ax[1].grid() 
    
    plt.tight_layout() 
    plt.savefig(os.path.join(os.path.dirname(__file__), 
                             "../../docs/assets/images/emissions_estimation.png"), dpi = 400)
    
    return emissions    


    
if __name__ == "__main__":
    extrapolate_fossil_fuels()
    data = extrapolate_emissions(plot = True)
    
    # data = plot_extrapolation_demo()
    # plot_emission_estimate_demo()
