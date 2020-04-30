import urllib.request, json 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
import json
from datetime import datetime
from configparser import ConfigParser


#Disabling some useless warnings
import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

#Loading configs
config = ConfigParser()
config.read('/mnt/c/Users/franc/Desktop/covid/covid-config.ini')
images = True if config['Output-images-to-File']['enabled'] == 'True' else False
if(images):
    path = config['Output-images-to-File']['path']
save_json = True if config['Save-Json-Data']['enabled'] == 'True' else False
if(save_json):
    json_path = config['Save-Json-Data']['path']
screen = True if config['Output-images-to-Screen']['enabled'] == 'True' else False
logging = True if config['Logging']['enabled'] == 'True' else False




def line_plot(data, data_name, plot_color):
    #Create a line plot with the provided data

    if type(data_name) != list:
        plt.title(f'Current {data_name}')
        plt.ylabel(data_name)
        dates = pd.date_range(start='24/02/2020', periods=len(data))
    else:
        dates = pd.date_range(start='24/02/2020', periods=len(data[0]))
    index=0
    if type(data) == list and type(plot_color)==list:
        for d in data:
            #plot = d.plot(marker='o',color=plot_color[index],label=data_name[index],linewidth=2)

            plt.plot_date(dates, d, marker='o' ,color=plot_color[index],label=data_name[index],linewidth=2,linestyle='-')
            index+=1
        plt.legend(loc="upper left")
    else:
        plt.plot_date(dates, data, marker='o',color=plot_color, linewidth=2,linestyle='-')
        #data.plot(marker='o',color=plot_color, linewidth=2)
    

def bar_plot(data, data_name, plot_color):
    #Create a bar plot with the provided data calculating the difference day by day
    dates = pd.date_range(start='24/02/2020', periods=len(data)-1)
    
    data_list = list()
    index = 0

    for d in data[1:]:
        data_list.append(d-data[index])
        index+=1

    plt.title(f'Daily {data_name} variation')
    plt.ylabel(data_name)

    plt.bar(dates, data_list, color=plot_color)
    #print(data_name, len(data_list), data_list,'\n')

def plot_style(ax):
    plt.grid(True)
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))




with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json") as url:
    """ data = json.loads(url.read().decode()) """
    #data_json = json.loads(url.read().decode())
    covid_data_italy = pd.read_json(url.read().decode())
    #covid_data_italy = pd.read_json(data_json)
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded json data")
        start_time = time.time()

    last_update = f'Last update: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
    file_name = f'{datetime.now().strftime("%y_%m_%d_%H_%M_%S")}.json'
    if(save_json):
        with open(f'{json_path}{file_name}', 'w+') as save_file:
            covid_data_italy.to_json(save_file,orient = 'records')
            if(logging):
                print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Saved json data {file_name}")

    
    
    
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

    plot_style(ax)

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

    plot_style(ax)

    if(images):
        plt.savefig(f'{path}line_plot_2.png')
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_2.png")
    #quit()
    


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
        ax = plt.subplot(len(plots_data),2,subplots)
        plot_style(ax)
        line_plot(d,plots_data_name[i],plots_data_color[i])
        ax = plt.subplot(len(plots_data),2,subplots+1)
        plot_style(ax)
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
