import urllib.request, json 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
import json
from datetime import datetime
from configparser import ConfigParser


""" Disabling some useless warnings, they are not showing up anymore even when commented, leaving them for future reference """
#import warnings
#import matplotlib.cbook
#warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation) 

""" Loading configs """
config = ConfigParser()
#config.read('/home/fra/python/covid/covid-config.ini')
config.read('covid-config.ini')
images = True if config['Output-images-to-File']['enabled'] == 'True' else False
if(images):
    path = config['Output-images-to-File']['path']
save_json = True if config['Save-Json-Data']['enabled'] == 'True' else False
if(save_json):
    json_path = config['Save-Json-Data']['path']
screen = True if config['Output-images-to-Screen']['enabled'] == 'True' else False
logging = True if config['Logging']['enabled'] == 'True' else False



""" Create a line plot with the provided data, can provide a line plot with multiple lines when provided with a list of data,data_name and plot_color, all of the same length """
def line_plot(data, data_name, plot_color):

    """Changing some config for the plots based on if I'm working with list or not"""
    if type(data_name) != list:
        plt.title(f'Number of {data_name}')
        plt.ylabel(data_name)
        
        dates = pd.date_range(start='24/02/2020', periods=len(data))
    else:
        dates = pd.date_range(start='24/02/2020', periods=len(data[0]))

    

    """If working with list plotting a line for every data provided, otherwise plot only the single line with the data provided"""
    if type(data) == list and type(plot_color)==list:
        """enumerate(data) allows to get both index and value in a cool and readable way(comment for future reference)"""
        for index, d in enumerate(data):
            plt.plot_date(dates, d, marker='o' ,color=plot_color[index],label=data_name[index],linewidth=2,linestyle='-')
            plt.legend(loc="upper left")
        
    else:
        plt.plot_date(dates, data, marker='o',color=plot_color, linewidth=2,linestyle='-')
    
"""Create a bar plot with the provided data calculating the daily variation"""
def bar_plot(data, data_name, plot_color):

    dates = pd.date_range(start='24/02/2020', periods=len(data))
    
    daily_variation = list()

    """Adding the first value as 0 to have the same length for all the plots"""
    daily_variation.append(0)

    """Calcualting the difference between the current number of x and the last day number of x"""
    for index, d in enumerate(data[1:]):
        daily_variation.append(d-data[index])

    plt.title(f'Daily {data_name} variation')
    plt.ylabel(data_name)

    plt.bar(dates, daily_variation, color=plot_color)


"""Sets the plot style, used when using a lot of subplots to keep the code a little cleaner"""
def plot_style(ax):
    plt.grid(True)
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))



""""Opening connection to the server where data is hosted, if succeded keep working on  """
with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json") as url:

    """Downloading data and decoding it"""
    covid_data_italy = pd.read_json(url.read().decode())

    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded json data")
        start_time = time.time()

    last_update = f'Last update: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
    file_name = f'{datetime.now().strftime("%y_%m_%d_%H_%M_%S")}.json'

    """Saving the json file to the directory specified in the configs (if requested)"""
    if(save_json):
        with open(f'{json_path}{file_name}', 'w+') as save_file:
            covid_data_italy.to_json(save_file,orient = 'records')
            if(logging):
                print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Saved json data {file_name}")

    
    
    
    """Creating big line plot with cases, cured, active cases and deaths"""
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
    
    

    """Creating Big line plot with IE patients, hospitalized patients, cured patients and deaths"""
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
    


    """Creating small line+bar plots for all of the data above"""
    fig, ax = plt.subplots(figsize=(19, 30))
    fig.canvas.set_window_title('Covid-19')

    """Data structures to plot"""
    plots_data = [covid_data_italy['totale_casi'],
                  covid_data_italy["totale_positivi"],
                  covid_data_italy['dimessi_guariti'],
                  covid_data_italy['deceduti'],
                  covid_data_italy['tamponi'],
                  covid_data_italy['terapia_intensiva'],
                  covid_data_italy['ricoverati_con_sintomi'],
                 ]
    plots_data_name = ['cases',
                       'active cases',
                       'cured patients',
                       'deaths',
                       'swabs',
                       'intensive care patients',
                       'hospitalized patients',
                      ]
    plots_data_color = ['darkred',
                        'orangered',
                        'limegreen',
                        'black',
                        'blue',
                        'red',
                        'pink',
                       ]
    
    """Creating subplots for all the data"""
    subplots = 1
    for i,d in enumerate(plots_data):
        ax = plt.subplot(len(plots_data),2,subplots)
        plot_style(ax)
        line_plot(d,plots_data_name[i],plots_data_color[i])
        ax = plt.subplot(len(plots_data),2,subplots+1)
        plot_style(ax)
        bar_plot(d,plots_data_name[i],plots_data_color[i])
        i+=1
        subplots+=2
    
    """Fixing subplots overlapping"""
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
