import urllib.request, json 
import pandas as pd
import matplotlib.pyplot as plt

import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

def line_plot(data, data_name, plot_color):
    #Create a line plot with the provided data
    if type(data_name) != list:
        plt.title(f'Current {data_name}')
        plt.ylabel(data_name)
        
    index=0
    if type(data) == list and type(plot_color)==list:
        for d in data:
            d.plot(marker='o',color=plot_color[index],label=data_name[index])
            index+=1
        plt.legend(loc="upper left")
    else:
        data.plot(marker='o',color=plot_color)

def bar_plot(data, data_name, plot_color):
    #Create a bar plot with the provided data calculating the difference day by day
    data_list = list()
    index = 0
    for d in data[1:]:
        data_list.append(d-data[index])
        index+=1
    plt.title(f'New daily {data_name}')
    plt.ylabel(data_name)
    plt.bar([i for i in range(len(data_list))], data_list, color=plot_color)

with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json") as url:
    """ data = json.loads(url.read().decode()) """
    covid_data_italy = pd.read_json(url.read().decode())
    
    #Big line plot with cases, cured, active cases and deaths
    fig, ax = plt.subplots(figsize=(19, 10))
    fig.canvas.set_window_title('Covid-19')
    
    line_plot([covid_data_italy['totale_casi'],
               covid_data_italy['dimessi_guariti'],
               covid_data_italy['totale_positivi'],
               covid_data_italy['deceduti']
              ],
              ['cases','cured','active cases','deaths'],
              ['darkred','limegreen','orangered','black']
             )
    
    #Big line plot with IE patients, hospitalized patients, cured patients and deaths
    fig, ax = plt.subplots(figsize=(19, 10))
    line_plot([covid_data_italy['terapia_intensiva'],
               covid_data_italy['ricoverati_con_sintomi'],
               covid_data_italy['dimessi_guariti'],
               covid_data_italy['deceduti']
              ],
              ['intensive care patients','hospitalized patients','cured patients','deaths'],
              ['red','salmon','limegreen','black']
             )
    
    
    #Small line+bar plots for all of the data above
    #Line plots use total number and bar plots use day by day difference between data
    #Data structures
    fig, ax = plt.subplots(figsize=(19, 30))
    fig.canvas.set_window_title('Covid-19')
    
    plots_data = [covid_data_italy['totale_casi'],
                  covid_data_italy['deceduti'],
                  covid_data_italy['tamponi'],
                  covid_data_italy['terapia_intensiva'],
                  covid_data_italy['ricoverati_con_sintomi'],
                  covid_data_italy['dimessi_guariti'],
                 ]
    plots_data_name = ['cases',
                       'deaths',
                       'swabs',
                       'intensive care patients',
                       'hospitalized patients',
                       'cured patients'
                      ]
    plots_data_color = ['darkred',
                        'black',
                        'blue',
                        'red',
                        'salmon',
                        'limegreen'
                       ]
    i = 0
    subplots = 1
    #creating plots
    for d in plots_data:
        plt.subplot(len(plots_data),2,subplots)
        line_plot(d,plots_data_name[i],plots_data_color[i])
        plt.subplot(len(plots_data),2,subplots+1)
        bar_plot(d,plots_data_name[i],plots_data_color[i])
        i+=1
        subplots+=2
    
    plt.subplots_adjust(hspace = .4)
    plt.show()
