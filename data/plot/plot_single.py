# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 19:05:47 2024

@author: Bernhard
"""

import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import json 

def plot_single_go(title = "",
                   unit = "",
                   data_plot = {},
                   filename = "",
                   show_plot = False,
                   unit_fac = 1,
                   legend_inside = True,
                   colors = None,
                   time_res = "monthly",
                   source_text = None,
                   plot_type = "line",
                   plotmax_fac = 1.1):
    
    if source_text == None:
        source_text = "eurostat (%s)" %(data_plot["meta"]["code"])
                      
    if colors == None: 
        colors = px.colors.qualitative.Dark2.copy()
        colors.remove('rgb(231,41,138)')  #removes pink 
        ### swap two colors 
        colors[3],colors[4] = colors[4],colors[3]
          
    
    if time_res == "monthly": 
        hovertemplate = '%{x|%b-%Y}, %{y:.2f}'
    elif time_res == "yearly": 
        hovertemplate = '%{x|%Y}, %{y:.2f}'
    
    fig = go.Figure()
    if plot_type == "line": 
        plotmax = 0
        color_ind = 0
        for data in data_plot["data"]:
            y_data = np.array(data_plot["data"][data]["y"])/unit_fac
            
            error_y = dict()
            stackgroup = None
            
            if "meta" in data_plot: 
                if "uncertainty" in data_plot["meta"]: 
                    if data in data_plot["meta"]["uncertainty"]: 
                        error_y = dict(type = "data", 
                                       visible = True, 
                                       array= data_plot["meta"]["uncertainty"][data]) 
                       
                
                if "areas" in data_plot["meta"]: 
                    if data in data_plot["meta"]["areas"]: 
                        stackgroup = "one" 
                    
            fig.add_trace(
                go.Scatter(x = data_plot["data"][data]["x"], 
                           y = y_data,
                           mode= "lines",
                           stackgroup = stackgroup,
                           name = data,
                           error_y = error_y,
                           line = dict(color = colors[color_ind % 7]),
                           hovertemplate = hovertemplate)
                )
            color_ind += 1
            plotmax = max(plotmax, max(y_data)*plotmax_fac)
            
            
    elif plot_type == "area": 
        color_ind = 0
        sum_data = np.zeros(10)
        
        for data in data_plot["data"]:
            y_data = np.array(data_plot["data"][data]["y"])/unit_fac
            color = colors[color_ind % len(colors)]
            color_opacity = color.rstrip(")")+",0.6)"
            color_opacity = color_opacity.replace("rgb", "rgba")
            if data == "Total": 
                fig.add_trace(
                    go.Scatter(x = data_plot["data"][data]["x"], 
                               y = np.array(data_plot["data"][data]["y"])/unit_fac,
                               mode='lines',
                               name = data,
                               line = dict(color = "black"),
                               hovertemplate = hovertemplate))
            else:
                fig.add_trace(
                    go.Scatter(x = data_plot["data"][data]["x"], 
                               y = y_data,
                               stackgroup = "one",
                               line = dict(color = color),
                               # fill='tonexty', 
                               fillcolor=color_opacity,
                               mode='lines',
                               name = data,
                               hovertemplate = hovertemplate))
                color_ind += 1
            
                if sum(sum_data) == 0: 
                    sum_data = np.array(y_data)
                else: 
                    sum_data += np.array(y_data)
                
        plotmax = max(sum_data)*plotmax_fac
    
    
    elif plot_type == "area_button": 
        buttondata = []
        len_bals = len(data_plot)
        
        bal_ind = 0 
        for bal in data_plot: 
            len_siecs = len(data_plot[bal]["data"])
            
            color_ind = 0
            sum_data = np.zeros(10)
            
            for data in data_plot[bal]["data"]:
                y_data = np.array(data_plot[bal]["data"][data]["y"])/unit_fac
               
                if bal_ind == 0: visible = True 
                else: visible = False 

                fig.add_trace(
                    go.Scatter(x = data_plot[bal]["data"][data]["x"], 
                               y = y_data,
                               stackgroup = "one",
                               line = dict(color = colors[color_ind % len(colors)]),
                               mode='lines',
                               name = data,
                               visible = visible,
                               hovertemplate = hovertemplate))
                color_ind += 1
            
                if sum(sum_data) == 0: 
                    sum_data = np.array(y_data)
                else: 
                    sum_data += np.array(y_data)
                    
            log_list = np.array([False for i in range(int(len_siecs*len_bals))])
            log_list[bal_ind*len_siecs:(bal_ind+1)*len_siecs] = True 
            
            ### data for the dropdown menu batton 
            buttondata.append(dict(label = bal,
                  method = 'update',
                  args = [{'visible': log_list},
                          {'title': title,
                           'showlegend': True}]))
                    
            plotmax = max(sum_data)*plotmax_fac
            bal_ind += 1 
    
    elif plot_type == "bar":         
        hovertemplate= ("%{customdata:> .2f}<extra></extra>")
        start = True 
        color_ind = 0
        fig.update_layout(barmode='stack')
        for data in data_plot["data"]:
            y_data = data_plot["data"][data]["y"]/unit_fac
            
            if data == "Total": 
                fig.add_trace(
                    go.Scatter(x = data_plot["data"][data]["x"], 
                               y = np.array(data_plot["data"][data]["y"])/unit_fac,
                               mode='lines',
                               name = data,
                               customdata = y_data,
                               xhoverformat = "<b>%Y<b>",
                               line = dict(color = "grey"),
                               hovertemplate = hovertemplate))
            else: 
                if start: 
                    sum_data = np.zeros(len(y_data))
                    start = False 
                    
                fig.add_trace(
                    go.Bar(x = data_plot["data"][data]["x"], 
                               y = y_data,
                               customdata = y_data,
                               name = data,
                               xhoverformat = "<b>%Y<b>",
                               hoverlabel  = dict(align = "right"),
                               marker_color = colors[color_ind],
                               base = sum_data,
                               hovertemplate = hovertemplate))
      
                sum_data += np.array(y_data)
                color_ind += 1 
            plotmax = max(sum_data)*plotmax_fac    
        
        fig.update_layout(hovermode="x unified")
        
    if legend_inside: 
        legend_dict= dict(
            yanchor="bottom",
            y=0.01,
            xanchor="left",
            x=0.01)
        bottomshift = 0 
    else: 
        legend_dict=dict(
            yanchor="top",
            y=-0.07,
            xanchor="left",
            x=0.01)
        bottomshift = 50
    
    
    if plot_type == "area_button": 
        fig.update_layout(
            updatemenus=[go.layout.Updatemenu(
                active=0,
                buttons=list(buttondata),
                x=-0.05,
                xanchor="left",
                y=1.16,
                yanchor="top"
                )])
        title_shift_x = 0.90
        title_shift_y = -0.05 
        margin_up_shift = 0
        xanchor = "right" 
        
        if plotmax_fac == 1: 
            fig.update_layout(
                yaxis_range=[0, plotmax])
        
        
    else: 
        fig.update_layout(
            yaxis_range=[0, plotmax])
        title_shift_x = 0
        title_shift_y = 0
        margin_up_shift = 0
        xanchor = "left"
    
    
    
    fig.update_layout(
        yaxis_title= unit,
        legend=legend_dict,
        yaxis = dict(
            tickfont = dict(
                size = 12),
            titlefont = dict(
                size = 12)
            ),
        xaxis = dict(
            tickfont = dict(
                size = 12)
            ),        
        height = 500,
        title = dict(
            text = title,
            x = 0.05+title_shift_x,
            xanchor = xanchor,
            y = 0.99+title_shift_y,
            font = dict(
                size = 14)
            ),
        margin=dict(
            l=40,
            r=20,
            b=120-bottomshift,
            t=30+margin_up_shift,
            ),
        )

    fig.add_annotation(dict(
        font=dict(size=7),
        x=1,
        y=-0.06,
        showarrow=False,
        text=("Chart by B.Thaler | Austria Transition Tracker | "
            "<a href = \"https://creativecommons.org/licenses/by/4.0/\">CC BY 4.0</a>"
            "<br>Data source: " +source_text),
        xanchor='right',
        yanchor = "top",
        xref="paper",
        yref="paper",
        align = "right"))

    
    """ save figure data as static json file """
    data_dict = {}
    if plot_type == "area_button": 
        for bal in data_plot:
            data_dict[bal] = {}
            for data in data_plot[bal]["data"]:
                data_dict[bal][data] = {}
                x = data_plot[bal]["data"][data]["x"]
                for i in range(len(x)):
                    data_dict[bal][data][x[i].strftime('%Y-%m-%d')] = data_plot[bal]["data"][data]["y"][i]/unit_fac
    
    else:
        for data in data_plot["data"]:
            data_dict[data] = {}
            x = data_plot["data"][data]["x"]
            for i in range(len(x)):
                data_dict[data][x[i].strftime('%Y-%m-%d')] = data_plot["data"][data]["y"][i]
                
    with open("../../docs/assets/data_charts/%s.json" %(filename), "w") as fp:
        json.dump(data_dict, fp, indent = 6)


    """ show and save plot """
    if show_plot: 
        fig.show(renderer = "browser")
    fig.write_html("../../docs/_includes/%s.html" %(filename),
                    include_plotlyjs='cdn',
                    config = {"modeBarButtons": [[
                        "zoom2d", 
                        "pan2d",
                        'zoomIn2d', 
                        'zoomOut2d',
                        'resetViews',
                        'autoScale2d',
                        'toImage']]})
    
    
    """ add download button as direct js code in html file """
    custom_button = (""
        "{name: \'Download data\',"
        "icon: {\'width\': 500,"
                "\'height': 500,"
                "\'path': 'M256,409.7,152.05,305.75,173.5,284.3l67.33,67.32V34h30.34V351.62L338.5,284.3,360,305.75ZM445.92,351v93.22a3.61,3.61,0,0,1-3.47,3.48H69.15a3.3,3.3,0,0,1-3.07-3.48V351H35.74v93.22A33.66,33.66,0,0,0,69.15,478h373.3a33.85,33.85,0,0,0,33.81-33.82V351Z'},"     
                "click: () => {"
                "var filename = \'%s.json\';"
                "var jsonUrl = \'{{site.baseurl}}assets/data_charts/%s.json\';"
                "var link = document.createElement(\'a\');"
                "link.href = jsonUrl;"
                "link.setAttribute(\'download\', filename);"
                "document.body.appendChild(link);"
                "link.click(); "
                "document.body.removeChild(link);}"                      
                "},"  %(filename, filename)
                )
    
    ### load old file and add the custom download button to the modeBarButtons config 
    fp_old = open("../../docs/_includes/%s.html" %(filename), "r") 
    lines = fp_old.readlines() 
    fp_old.close()
    
    fp_new = open("../../docs/_includes/%s.html" %(filename), "w") 
    for line in lines:
        if "modeBarButtons" in line: 
            text_before = line.split("\"zoom2d\"")[0]
            text_after = line.split("\"zoom2d\"")[1]
            new_text = text_before + custom_button + "\"zoom2d\"" + text_after 
            fp_new.write(new_text)
        else:
            fp_new.write(line)

    
    
    
