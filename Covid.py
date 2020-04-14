import urllib.request, json 
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime
from configparser import ConfigParser

#Disabling some useless warnings
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

#Loading configs
config = ConfigParser()
config.read('covid-config.ini')
images = True if config['Output-images-to-File']['enabled'] == 'True' else False
if(images):
    path = config['Output-images-to-File']['path']
screen = True if config['Output-images-to-Screen']['enabled'] == 'True' else False
logging = True if config['Logging']['enabled'] == 'True' else False


def line_plot(data, data_name, plot_color):
    #Create a line plot with the provided data
    if type(data_name) != list:
        plt.title(f'Current {data_name}')
        plt.ylabel(data_name)
    
    index=0
    if type(data) == list and type(plot_color)==list:
        for d in data:
            d.plot(marker='o',color=plot_color[index],label=data_name[index],linewidth=2)
            index+=1
        plt.legend(loc="upper left")
    else:
        data.plot(marker='o',color=plot_color, linewidth=2)

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

    last_update = f'Last update: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded json data")
        start_time = time.time()
    
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
    plt.suptitle(last_update, fontsize=20)

    if(images):
        plt.savefig(f'{path}line_plot_1.png')
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_1.png")
    
    



    #Big line plot with IE patients, hospitalized patients, cured patients and deaths
    fig, ax = plt.subplots(figsize=(19, 10))
    line_plot([covid_data_italy['terapia_intensiva'],
               covid_data_italy['ricoverati_con_sintomi'],
               covid_data_italy['dimessi_guariti'],
               covid_data_italy['deceduti']
              ],
              ['intensive care patients','hospitalized patients','cured patients','deaths'],
              ['red','pink','limegreen','black']
             )
    if(images):
        plt.savefig(f'{path}line_plot_2.png')
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_2.png")
    
    



    #Small line+bar plots for all of the data above
    #Line plots use total number and bar plots use day by day difference between data

    #Data structures
    fig, ax = plt.subplots(figsize=(19, 30))
    fig.canvas.set_window_title('Covid-19')
    
    plots_data = [covid_data_italy['totale_casi'],
                  covid_data_italy["totale_positivi"],
                  covid_data_italy['deceduti'],
                  covid_data_italy['tamponi'],
                  covid_data_italy['terapia_intensiva'],
                  covid_data_italy['ricoverati_con_sintomi'],
                  covid_data_italy['dimessi_guariti']
                 ]
    plots_data_name = ['cases',
                       'active cases',
                       'deaths',
                       'swabs',
                       'intensive care patients',
                       'hospitalized patients',
                       'cured patients',
                      ]
    plots_data_color = ['darkred',
                        'orangered',
                        'black',
                        'blue',
                        'red',
                        'pink',
                        'limegreen',
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
    if(images):
        plt.savefig(f'{path}mini_plots.png')
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created mini_plots.png")
    
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Runtime = {(time.time() - start_time)}")
        print('\n')
    if(screen):
        plt.show()
