---
layout: home
---


<div class="row">
  <div class="column_left">
  <br>
  <b>Welcome to the <i>Austria Transition Tracker!</i> </b> <br>
  This site collects and displays various data connected to the sustainable transition in Austria. <br>
  <br>
  On the chart to the right you can see the historical greenhouse gas (GHG) emissions and corresponding sector contributions in Austria. The target of this page is to track the (hopefully) continuing transition to zero emissions with public available data. <br> 
  <br>  
  On the top menu you can navigate to different sub-sector pages that show detailed data of each sector. <br>
  <br> 
  Additional datasets might be added in future - any suggestions are very welcome! <br>
  For more information, data sources, and technical details please visit the <b><a href= "{{ "/about/" | relative_url }}">About page.</a></b> <br> 
  <br>   
  </div>

  <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_co2_emissions_sectors.html %}
  </div>
</div> 

<div class="row">
  <div class="column_left"> 
   {% include AT_timeseries_emissions_projection_yearly.html %}
   </div>

  <div class="spacer"></div>

  <div class="column_right">
  <br> 
    Official detailed emission statistics are only available several months after the respective year. However, rough emission projections are possible with more timely available fossil fuel consumption data. On the chart to the left a projection of Austrian greenhouse gas emissions with latest available data is shown. The exact methodology <b><a href= "{{ "/consumption-estimation/" | relative_url }}">is described here</a></b>. In short, eurostat data of fossil fuel consumption is extrapolated to the full year and scaled with emission factors to arrive at actual energy-sector related emission estimations (Transport, Buildings, Energy & Industry, including process emissions). Other sectors (Agriculture, Waste, Fluorinated Gases) are extrapolated based on current trends. <br> 
    <br> 
    The model is rather simple and based on past data and temporal correlation. Extrapolated data must therefore be interpreted with great care, especially early in the year! <br> 
    <br> 
    Yearly and monthly fuel consumption data (including extrapolations) of all considered fossil fuels are shown below.<br><br>

  </div>
</div> 


<div class="row">
</div> 

<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_natural_gas_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
   {% include AT_timeseries_consumption_natural_gas_yearly.html %}
  </div>
</div> 

<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_gasoline_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_consumption_gasoline_yearly.html %}
  </div>
</div> 


<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_diesel_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_consumption_diesel_yearly.html %}
  </div>
</div> 


<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_heating_oil_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_consumption_heating_oil_yearly.html %}
  </div>
</div> 


<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_refinery_gas_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_consumption_refinery_gas_yearly.html %}
  </div>
</div> 



<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_hard_coal_electricity_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_consumption_hard_coal_electricity_yearly.html %}
  </div>
</div> 


<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_hard_coal_industry_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_consumption_hard_coal_industry_yearly.html %}
  </div>
</div> 



<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_hard_coal_coke_ovens_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_consumption_hard_coal_coke_ovens_yearly.html %}
  </div>
</div> 




<div class="row">
  <div class="column_left">
    {% include AT_timeseries_consumption_coke_oven_coke_monthly.html %}
  </div>
  
 <div class="spacer"></div>

  <div class="column_right">
      {% include AT_timeseries_consumption_coke_oven_coke_yearly.html %}
  </div>
</div> 

