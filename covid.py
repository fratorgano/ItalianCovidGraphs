import time
import json
import os
from datetime import datetime, timedelta
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
config.read('covid-config.ini')
if(len(config)==1):
    raise Exception("Could not find config file")
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
    plt.box(False)
    plt.grid(True)
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0))
    #ax.xaxis.set_minor_locator(mdates.DayLocator())

lastUpdate = f"{datetime.now().strftime('%d%m%Y%H%M%S')}"

"""Creating json file with the last updated time"""
if(images):
    with open(f'{path}update.json','w+') as outfile:
        data ={
            'lastUpdate': lastUpdate,
        }
        json.dump(data,outfile)


"""Downloading data and decoding it into a pandas dataframe"""
covid_data_italy = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")
if(logging):
    print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded italian json data")
    start_time = time.time()

"""Checks if data is updated, if it's not, wait five minutes and tries again, otherwise keeps going"""
while(covid_data_italy['data'][len(covid_data_italy['data'])-1][:10]!=datetime.now().strftime("%Y-%m-%d")):
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Data is outdated({covid_data_italy['data'][len(covid_data_italy['data'])-1][:10]}), waiting 5 minutes and retrying ")
    time.sleep(60*5)
    covid_data_italy = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded json data")

"""Delete old plots"""
if(images):
    images_dir = os.listdir(path)
    for item in images_dir:
        if item.endswith(".png"):
            os.remove(os.path.join(path, item))
            if(logging):
                print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Deleted old image")

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
home_isolation = Sample(covid_data_italy['isolamento_domiciliare'], starting_date, color='c', name='stay at home people')


"""Creating big line plot with cases, active cases, recovered and deaths"""
fig, ax = plt.subplots(figsize=(19, 10))
plot_style(ax)

total_cases.line_plot()
active_cases.line_plot()
recovered.line_plot()
deaths.line_plot()
home_isolation.line_plot()

plt.legend(loc="upper left")
fig.tight_layout()

if(images):
    plt.savefig(f'{path}line_plot_1_{lastUpdate}.png', transparent=True)
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_1")

if(screen):
    plt.show()


"""Creating Big line plot with IC patients, hospitalized patients, cured patients and deaths"""
fig, ax = plt.subplots(figsize=(19, 10))
plot_style(ax)

intensive_care.line_plot()
hospitalized.line_plot()
#recovered.line_plot()
deaths.line_plot()

plt.legend(loc="upper left")
fig.tight_layout()

if(images):
    plt.savefig(f'{path}line_plot_2_{lastUpdate}.png', transparent=True)
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_2")

if(screen):
    plt.show()


"""Creating small line+bar plots for all of the data above"""
fig, ax = plt.subplots(figsize=(19, 40))
fig.canvas.set_window_title('Covid-19')

ax = plt.subplot(8,2,1)
plot_style(ax)
total_cases.line_plot(title=True, marker='', linewidth=3)
ax = plt.subplot(8,2,2)
plot_style(ax)
total_cases.variation_bar_plot(title=True)

ax = plt.subplot(8,2,3)
plot_style(ax)
active_cases.line_plot(title=True, marker='', linewidth=3)
ax = plt.subplot(8,2,4)
plot_style(ax)
active_cases.variation_bar_plot(title=True)

ax = plt.subplot(8,2,5)
plot_style(ax)
recovered.line_plot(title=True, marker='', linewidth=3)
ax = plt.subplot(8,2,6)
plot_style(ax)
recovered.variation_bar_plot(title=True)

ax = plt.subplot(8,2,7)
plot_style(ax)
home_isolation.line_plot(title=True, marker='', linewidth=3)
ax = plt.subplot(8,2,8) 
plot_style(ax)
home_isolation.variation_bar_plot(title=True)

ax = plt.subplot(8,2,9)
plot_style(ax)
hospitalized.line_plot(title=True, marker='', linewidth=3)
ax = plt.subplot(8,2,10) 
plot_style(ax)
hospitalized.variation_bar_plot(title=True)

ax = plt.subplot(8,2,11)
plot_style(ax)
intensive_care.line_plot(title=True, marker='', linewidth=3)
ax = plt.subplot(8,2,12)
plot_style(ax)
intensive_care.variation_bar_plot(title=True)

ax = plt.subplot(8,2,13)
plot_style(ax)
deaths.line_plot(title=True, marker='', linewidth=3)
ax = plt.subplot(8,2,14)
plot_style(ax)
deaths.variation_bar_plot(title=True)

ax = plt.subplot(8,2,15)
plot_style(ax)
swabs.line_plot(title=True, marker='', linewidth=3)
ax = plt.subplot(8,2,16)
plot_style(ax)
swabs.variation_bar_plot(title=True)

"""Fixing subplots overlapping"""
fig.tight_layout()
#plt.subplots_adjust(hspace = .4)

if(images):
    plt.savefig(f'{path}mini_plots_{lastUpdate}.png', transparent=True)
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created mini_plots")

if(screen):
    plt.show()

"""Downloading european covid data"""
europe_data = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
if(logging):
    print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded european csv data")

"""Keeping only data from today and yesterday(cause of Spain) from european continent only"""
yesterday = (datetime.now()-timedelta(days=1)).strftime('%d/%m/%Y')
today = datetime.now().strftime('%d/%m/%Y')
#europe_data = europe_data[(europe_data['continentExp']=='Europe')]
europe_data = europe_data[(europe_data['continentExp']=='Europe')&((europe_data['dateRep']==today)|(europe_data['dateRep']==yesterday))].drop_duplicates(subset='countriesAndTerritories')
""" europe_data_yesterday = europe_data[(europe_data['dateRep']==yesterday)]
europe_data= pd.concat([europe_data_today,europe_data_yesterday]).drop_duplicates(subset='countriesAndTerritories') """

""""Sorting the data by number of new cases"""
europe_data=europe_data[['countriesAndTerritories','cases','dateRep']].sort_values(by=['cases'], ascending=False)

"""Creating a plot with the countries that had the most new covid cases"""
fig, ax = plt.subplots(figsize=(19, 10))
plt.box(False)
plt.grid(True)
plt.xticks(rotation=45, horizontalalignment='right')

plt.title('Top 20 European countries by new covid cases')

#ax = europe_data.plot.bar(x='countriesAndTerritories', y='cases')
ax.bar(europe_data['countriesAndTerritories'][:20],europe_data['cases'][:20], color='darkred')

fig.tight_layout()

if(images):
    plt.savefig(f'{path}europe{lastUpdate}.png', transparent=True)
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created europe")

if(screen):
    plt.show()

if(logging):
    print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Runtime = {(time.time() - start_time)}")
    print('\n')
