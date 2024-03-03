---
layout: home 
title: Fossil fuel consumption projection and emission extrapolation 
permalink: /consumption-estimation/
---



This page describes a simple, purely data-based method to project fossil fuel consumption and related CO$_2$ emissions within a year with available monthly data from eurostat. The basic idea of the approach is to extrapolate the trend in fuel consumption of past months within a year to fully yearly values.<br> 
<br> 
The first step is to retrieve the available monthly datasets from <a href = "https://ec.europa.eu/eurostat/data/database">Eurostat</a>, using the monthly commodity balances for natural gas, petroleum products and solid fossil fuels: 

|Fossil fuel category   | Database  | Unit   | Update delay  |   
|---|---|---|---|
| Natural gas   | NRG_CB_GASM  | TJ_GCV  | 1 month  |
| Oil  | NRG_CB_OILM    |THS_T   | 2 months |
| Coal  | NRG_CB_SFFM    | THS_T  |2 months  |

In case not all months are available for a year, yearly data are extrapolated based on projection factors that are retrieved from past data. For each fuel $f$, each month $m$ and each past year $y$ (starting 2013), a scaling factor $F_{f,m,y}^{cons}$ is calculated. This scaling factor describes the ratio between the actual final consumption at the end of the year $C_{f,y}$ and the consumption up to the respective month $C_{f,m,y}$: 

$$C_{f,y} = F_{f,m,y}^{cons} \cdot C_{f,m,y}$$ 
 
The monthly scaling factors of all years are assumed to be normally distributed, averaged and the average $\overline{F^{cons}_{m,f}}$ is used to scale the actual data: 

$$\overline{F^{cons}_{f,m}} = \frac{1}{N}\sum_y F_{f,m,y}^{cons}$$ 

For each scaling factor, also a <a href = "https://en.wikipedia.org/wiki/Unbiased_estimation_of_standard_deviation"> standard deviation estimator</a> with  rule-of thumb bias correction is calculated: 

$$\hat{\sigma_{F^{cons}_{f,m}}} = \sqrt{\frac{1}{N-1.5}\sum_y (\overline{F^{cons}_{f,m}} - F^{cons}_{f,y,m})^2}$$

This deviation allows to estimate the uncertainty of the fuel consumption projection. In the figure below, results of the approach to predict data of 2022 can be seen, with scaling factors calculated from the years 2013-2021. Although the prediction is not bad, there is still some systematic error, which cannont be explained by the pure statistical features. Especially the unstable situation of energy markets in the last years adds additional uncertainties. For example, the full year natural gas consumption is overestimated taking data until summer 2022. High prices during the second half of the year probably led to a consumption decrease compared to previous years that could not be projected. Extrapolation results have therefore be taken with great care. Data displayed on the <a href= "/" >tracker start page</a> always use training data up to the last year. 

<img src="/assets/images/fossil_fuel_consumption_estimation.png" alt="">


In order to estimate CO<sub>2</sub> emissions from these data, fuel-specific emissions of the following commodities are calculated using emission factors taken from the <a href = "https://www.umweltbundesamt.at/studien-reports/publikationsdetail?pub_id=2474&cHash=682457cf175c26a3d9639b6ef68c1c3b">National Inventory Report</a> and net calorific values (NCV) taken from <a href = "https://www.statistik.at/statistiken">Statistics Austria Energy Balances</a>: 

|Fossil fuel   | Database  | Entry | NCV  | Emission factor |   
|---|---|---|---|---|
| Natural gas   | NRG_CB_GASM  | Inland consumption (IC_CAL_MG) | 0.0372 TJ/1000m3  | 55.4 t_CO2/TJ  |
| Gasoline  | NRG_CB_OILM    |Gross inland deliveries (GID_OBS)   | 0.0418 TJ/t  |71.3 t_CO2/TJ | 
| Diesel  | NRG_CB_OILM    |Gross inland deliveries (GID_OBS)   |0.0424 TJ/t | 71.3 t_CO2/TJ|
| Heating gas oil  | NRG_CB_OILM    |Gross inland deliveries (GID_OBS)   |0.0428 TJ/t | 75.0 t_CO2/TJ|
| Refinery gas  | NRG_CB_OILM    |Refinery fuel (RF) |0.0306 TJ/t | 64.0 t_CO2/TJ|
| Hard coal - electricity sector  | NRG_CB_SFFM  |Transformation input - electricity and heat generation  (TI_EHG_MAP) |0.0299 TJ/t | 95.0 t_CO2/TJ|
| Hard coal - industry sector  | NRG_CB_SFFM  | Final consumption - industry sector (FC_IND) |0.0299 TJ/t | 95.0 t_CO2/TJ|
| Hard coal - coke ovens  | NRG_CB_SFFM  | Transformation input - coke ovens (TI_CO) |0.0299 TJ/t | 95.0 t_CO2/TJ|
| Coke oven coke  | NRG_CB_SFFM  | Gross inland deliveries - calculated (GID_CAL) |0.0282 TJ/t | 94.6 t_CO2/TJ|

<div class="row">
  <div class="column_left">
  With the yearly consumption data $C_{f,y}$ of fuel $f$, the $NCV_f$ and emission factor $e_f$, an estimate for the actual emissions $E^{estimated}_{y}$ can be calculated: 

  $$E^{estimated}_{y} = \sum_f C_{f,y} \cdot NCV_f \cdot e_f$$

  Note that Biofuel related consumption (Biodiesel and Biogasoline) has to be subtracted from the Diesel and Gasoline consumption data, respectively. <br>
  The figure to the right (upper chart) compares these estimated emissions with the actual emissions from the energy-related sectors (<i>Transport, Energy&Industry</i> and <i>Buildings</i>). It can be seen that there is a systematic gap, caused by several systematic errors: 
<ul>
  <li>The calculated data do not consider process emissions from non fossil-fuel based industry secors (mainly cement and lime production, approximately 2.5 Mt<sub>CO2</sub> in 2021). </li>
  <li>Calculated data focus on CO<sub>2</sub> emissions, and do not consider CH<sub>4</sub> and N<sub>2</sub>O emissions, including fugitive emissions. </li>
  <li>Energy-related emissions from the agriculture sector are included in the calculated emissions, but not in the actual emissions used here. </li>
  <li>Not all fuels are considered, and integrated process routes in the industry sector (especially steel and chemical industry) might be oversimplified. </li>
</ul> 
To account for these systematic effects, an approach similar to the consumption projection above is chosen. For each year's calculated emissions $E^{estimated}_{y}$, a scaling factor $F^{em}_y$ is calculated, leading to an average $\overline{F^{em}_y}$ over all years with standard deviation $\hat{\sigma_{F^{em}_m}}$, that is used to arrive at the total emissions of the energy sector $E^{scaled}_{y}$: 

 $$E^{scaled}_{y} = E^{estimated}_{y} \cdot \overline{F^{em}_y}$$

 In the figure to the right (lower chart), upscaled emissions (using $\overline{F^{em}_y}$) of all years are shown, including the uncertainty. It can be seen that the approach estimates the actual emissions reasonably well.
  </div>

  <div class="spacer"></div>

  <div class="column_right">
  <img src="/assets\images\emissions_estimation.png" alt="">
  </div>

</div> 
<br> 

<div class="row">
  <div class="column_left">
   <img src="/assets\images\emissions_projection_2022.png" alt="">
  </div>

  <div class="spacer"></div>
 
  <div class = "column_right">
Together the fuel consumption extrapolation and the emission estimation allow to estimate CO<sub>2</sub> emissions based on non-fully available yearly data. In the first step, yearly fuel consumption is extrapolated from available monthly data and in the second step, emissions are estimated based on the described scaling:

$$ E^{scaled}_{y} = (\sum_f C_{f,m,y} \cdot \overline{F^{cons}_{f,m}} \cdot  NCV_f \cdot e_f) \cdot \overline{F^{em}_y}$$ 

It is important to note that the statistical uncertainties of both approaches add up (uncertainty propagation): 

$$\sigma^{E,total}_{y} = \sum_f (C_{f,m,y} \cdot  NCV_f \cdot e_f \cdot \overline{F^{em}_y} \cdot \hat{\sigma_{F^{cons}_{f,m}}})  +  (\sum_f C_{f,m,y} \cdot \overline{F^{cons}_{f,m}} \cdot  NCV_f \cdot e_f)  \cdot  \hat{\sigma_{F^{em}_y}}$$

The first term describes the uncertainty from fossil fuel consumption extrapolation and the second term the uncertainty from emission scaling. <br> 

  Finally, the emissions from other sectors (<i>Agriculture, Waste</i> and <i>Fluroinated Gases</i>) are added. For those sectors, a more simple approach is chosen: the average emission trend of the past three years is extrapolated to the projection year. <br>
<br>
  The total projected emissions for the year 2022  can be seen in the figure to the left. Emissions are projected using data up to the respective month on the x-axis. As can be seen, projected yearly emissions are overestimated with only the first few monthly data points, but fit better the more months are used. Again, energy market disruptions in 2022 may have caused stronger consumption decreases during the second half of the year, leading to systematic projection errors. In the lower chart on the left, the two uncertainties are shown. As expected, the uncertainty from consumption extrapolation decreases with increasing monthly data, whereas the emission scaling uncertainty is more or less constant. 
  </div>

  </div>

  