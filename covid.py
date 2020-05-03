import urllib.request
import time
import json
from datetime import datetime
from configparser import ConfigParser

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sample import Sample


""" Disabling some useless warnings, they are not showing up anymore even when commented, leaving them for future reference """
#import warnings
#import matplotlib.cbook
#warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation) 

""" Loading configs """
config = ConfigParser()
#config.read('/home/fra/python/covid/covid-config.ini')
config.read('/mnt/c/Users/franc/Desktop/covid/covid-config.ini')
images = True if config['Output-images-to-File']['enabled'] == 'True' else False
if(images):
    path = config['Output-images-to-File']['path']
save_json = True if config['Save-Json-Data']['enabled'] == 'True' else False
if(save_json):
    json_path = config['Save-Json-Data']['path']
screen = True if config['Output-images-to-Screen']['enabled'] == 'True' else False
logging = True if config['Logging']['enabled'] == 'True' else False

"""Sets the plot style, used when using a lot of subplots to keep the code a little cleaner"""
def plot_style(ax):
    plt.grid(True)
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    ax.xaxis.set_minor_locator(mdates.DayLocator())

""""Opening connection to the server where data is hosted, if succeded keep working on  """
with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json") as url:

    """Downloading data and decoding it"""
    covid_data_italy = pd.read_json(url.read().decode())
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded json data")
        start_time = time.time()

    last_update = f'Last update: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'

    """Saving the json file to the directory specified in the configs (if requested)"""
    if(save_json):
        file_name = f'{datetime.now().strftime("%y_%m_%d_%H_%M_%S")}.json'
        with open(f'{json_path}{file_name}', 'w+') as save_file:
            covid_data_italy.to_json(save_file,orient = 'records')
            if(logging):
                print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Saved json data {file_name}")


    """Creating Sample objects for the data I'm interested in"""
    starting_date = covid_data_italy['data'][0][:10]

    total_cases = Sample(covid_data_italy['totale_casi'], starting_date,color='darkred', name='cases')
    active_cases =  Sample(covid_data_italy['totale_positivi'], starting_date, color='orangered', name='active cases')
    recovered = Sample(covid_data_italy['dimessi_guariti'], starting_date, color='limegreen', name='recovered')
    deaths =  Sample(covid_data_italy['deceduti'], starting_date, color='black', name='deaths')
    intensive_care = Sample(covid_data_italy['terapia_intensiva'], starting_date, color='red', name='intensive care patients')
    hospitalized = Sample(covid_data_italy['ricoverati_con_sintomi'], starting_date, color='pink', name='hospitalized patients')
    swabs = Sample(covid_data_italy['tamponi'], starting_date, color='blue', name='swabs')


    """Creating big line plot with cases, active cases, recovered and deaths"""
    fig, ax = plt.subplots(figsize=(19, 10))
    plt.suptitle(last_update, fontsize=20)
    plot_style(ax)

    total_cases.line_plot()
    active_cases.line_plot()
    recovered.line_plot()
    deaths.line_plot()

    plt.legend(loc="upper left")

    if(images):
        plt.savefig(f'{path}line_plot_1.png')
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_1.png")

    if(screen):
        plt.show()
    

    """Creating Big line plot with IC patients, hospitalized patients, cured patients and deaths"""
    fig, ax = plt.subplots(figsize=(19, 10))
    plot_style(ax)

    intensive_care.line_plot()
    hospitalized.line_plot()
    recovered.line_plot()
    deaths.line_plot()

    plt.legend(loc="upper left")
    
    if(images):
        plt.savefig(f'{path}line_plot_2.png')
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_2.png")
    
    if(screen):
        plt.show()
    

    """Creating small line+bar plots for all of the data above"""
    fig, ax = plt.subplots(figsize=(19, 30))
    fig.canvas.set_window_title('Covid-19')

    ax = plt.subplot(7,2,1)
    plot_style(ax)
    total_cases.line_plot(title=True, marker='.')
    ax = plt.subplot(7,2,2)
    plot_style(ax)
    total_cases.variation_bar_plot(title=True)

    ax = plt.subplot(7,2,3)
    plot_style(ax)
    active_cases.line_plot(title=True, marker='.')
    ax = plt.subplot(7,2,4)
    plot_style(ax)
    active_cases.variation_bar_plot(title=True)

    ax = plt.subplot(7,2,5)
    plot_style(ax)
    recovered.line_plot(title=True, marker='.')
    ax = plt.subplot(7,2,6)
    plot_style(ax)
    recovered.variation_bar_plot(title=True)

    ax = plt.subplot(7,2,7)
    plot_style(ax)
    deaths.line_plot(title=True, marker='.')
    ax = plt.subplot(7,2,8)
    plot_style(ax)
    deaths.variation_bar_plot(title=True)

    ax = plt.subplot(7,2,9)
    plot_style(ax)
    swabs.line_plot(title=True, marker='.')
    ax = plt.subplot(7,2,10)
    plot_style(ax)
    swabs.variation_bar_plot(title=True)

    ax = plt.subplot(7,2,11)
    plot_style(ax)
    intensive_care.line_plot(title=True, marker='.')
    ax = plt.subplot(7,2,12)
    plot_style(ax)
    intensive_care.variation_bar_plot(title=True)

    ax = plt.subplot(7,2,13)
    plot_style(ax)
    hospitalized.line_plot(title=True, marker='.')
    ax = plt.subplot(7,2,14)
    plot_style(ax)
    hospitalized.variation_bar_plot(title=True)

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
