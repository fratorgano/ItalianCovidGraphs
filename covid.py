import time
import json
import os
from datetime import datetime, timedelta
from configparser import ConfigParser

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from sample import Sample

import requests


""" Disabling some useless warnings, they are not showing up anymore even when commented, leaving them for future reference """
#import warnings
#import matplotlib.cbook
#warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation) 

""" Loading configs """
config = ConfigParser()
config.read("covid-config.ini")
if(len(config)==1):
    raise Exception("Could not find config file")
images = True if config['Output-images-to-File']['enabled'] == 'True' else False
if(images):
    path = config['Output-images-to-File']['path']
    delete_old = True if config['Output-images-to-File']['delete_old'] == 'True' else False
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
"""Sets the plot style for small plots, used when using a lot of subplots to keep the code a little cleaner"""
def plot_style_mini(ax):
    plt.box(False)
    plt.grid(True)
    plt.xticks(rotation=45)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=24))


"""Downloading data and decoding it into a pandas dataframe"""
covid_data_italy = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")
if(logging):
    print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded covid json data")
    start_time = time.time()

"""Downloading json data about vaccines and prepares it to be used for plots"""
vaccine = True
if(vaccine):
    """Downloading vaccine data"""
    response = json.loads(requests.get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.json").text)
    vaccine_data = pd.DataFrame(response["data"])
    if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded vaccine json data")
    response = json.loads(requests.get("https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.json").text)
    distribution_data = pd.DataFrame(response["data"])
    if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded vaccine distribution json data")
    
    cum_dosi = pd.DataFrame(vaccine_data.groupby(['data_somministrazione'])['prima_dose'].sum()).cumsum()
    cum_dosi['seconda_dose'] = pd.DataFrame(vaccine_data.groupby(['data_somministrazione'])['seconda_dose'].sum()).cumsum()['seconda_dose']

    cum_regioni = pd.DataFrame(vaccine_data.groupby(['nome_area'])['prima_dose'].sum())
    cum_regioni['seconda_dose'] = pd.DataFrame(vaccine_data.groupby(['nome_area'])['seconda_dose'].sum())['seconda_dose']

    cum_regioni['n_dosi'] = pd.DataFrame(distribution_data.groupby(['nome_area'])['numero_dosi'].sum())

    cum_regioni = cum_regioni.rename(index={'Provincia Autonoma Bolzano / Bozen':"Bolzano","Provincia Autonoma Trento":"Trento","Valle d'Aosta / Vallée d'Aoste":"Valle d'Aosta"}, errors="raise")
    cum_regioni = cum_regioni.sort_index()

    cum_regioni['pop'] = [1305770, 556934, 531178, 1924701, 5785861, 4467118, 1211357, 5865544, 1543127, 10103969, 1518400, 302265, 4341375, 4008296, 1630474, 4968410, 3722729, 541098, 880285, 
                          125501, 4907704]

    cum_fornitori = pd.DataFrame(distribution_data.groupby(['fornitore'])['numero_dosi'].sum())

    starting_date_vaccine = vaccine_data['data_somministrazione'][0][:10]


"""Checks if data is updated, if it's not, wait five minutes and tries again, otherwise keeps going"""
while(covid_data_italy['data'][len(covid_data_italy['data'])-1][:10]!=datetime.now().strftime("%Y-%m-%d")):
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Data is outdated({covid_data_italy['data'][len(covid_data_italy['data'])-1][:10]}), waiting 5 minutes and retrying ")
    time.sleep(60*5)
    covid_data_italy = pd.read_json("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json")
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Downloaded json data")

"""Used to differentiate images file's names """
lastUpdate = f"{datetime.now().strftime('%d%m%Y%H%M%S')}"


"""Creating json file with the last updated time"""
if images:
    with open(f'{path}update.json','w+') as outfile:
        data ={
            'lastUpdate': lastUpdate,
        }
        json.dump(data,outfile)

"""Delete old images"""
if delete_old:
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
deaths =  Sample(covid_data_italy['deceduti'], starting_date, color='black', name='deaths', fix_zero=True)
intensive_care = Sample(covid_data_italy['terapia_intensiva'], starting_date, color='red', name='intensive care patients')
hospitalized = Sample(covid_data_italy['ricoverati_con_sintomi'], starting_date, color='pink', name='hospitalized patients')
swabs = Sample(covid_data_italy['tamponi'], starting_date, color='blue', name='swabs',fix_zero=True)
home_isolation = Sample(covid_data_italy['isolamento_domiciliare'], starting_date, color='c', name='stay at home people')
if vaccine:
    prima_dose = Sample(cum_dosi['prima_dose'], starting_date_vaccine, color='#0066cc', name='first vaccine doses')
    seconda_dose = Sample(cum_dosi['seconda_dose'], starting_date_vaccine, color='#ea307d', name='second vaccine doses')


"""Creating big line plot with cases, active cases, recovered, deaths and first dose and second dose vaccine data"""
fig, ax = plt.subplots(figsize=(19, 10))
plot_style(ax)

total_cases.line_plot()
active_cases.line_plot()
recovered.line_plot()
deaths.line_plot()
home_isolation.line_plot()
if vaccine:
    prima_dose.line_plot()
    seconda_dose.line_plot()

plt.legend(loc="upper left")
fig.tight_layout()

if(images):
    plt.savefig(f'{path}line_plot_1_{lastUpdate}.png', transparent=True)
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_1")

if(screen):
    plt.show()


"""Creating Big line plot with IC patients, hospitalized patients and deaths"""
fig, ax = plt.subplots(figsize=(19, 10))
plot_style(ax)

intensive_care.line_plot()
hospitalized.line_plot()
deaths.line_plot()

plt.legend(loc="upper left")
fig.tight_layout()

if(images):
    plt.savefig(f'{path}line_plot_2_{lastUpdate}.png', transparent=True)
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created line_plot_2")

if(screen):
    plt.show()

mini_plots = True
if(mini_plots):
    """Creating small line+bar plots for all of the data above"""
    fig, ax = plt.subplots(figsize=(19, 50 if vaccine else 40))
    fig.canvas.set_window_title('Covid-19')
    rows = 10 if vaccine else 8

    ax = plt.subplot(rows,2,1)
    plot_style_mini(ax)
    total_cases.line_plot(title=True, marker='', linewidth=3)
    ax = plt.subplot(rows,2,2)
    plot_style_mini(ax)
    total_cases.variation_bar_plot(title=True)

    ax = plt.subplot(rows,2,3)
    plot_style_mini(ax)
    active_cases.line_plot(title=True, marker='', linewidth=3)
    ax = plt.subplot(rows,2,4)
    plot_style_mini(ax)
    active_cases.variation_bar_plot(title=True)

    ax = plt.subplot(rows,2,5)
    plot_style_mini(ax)
    recovered.line_plot(title=True, marker='', linewidth=3)
    ax = plt.subplot(rows,2,6)
    plot_style_mini(ax)
    recovered.variation_bar_plot(title=True)

    ax = plt.subplot(rows,2,7)
    plot_style_mini(ax)
    home_isolation.line_plot(title=True, marker='', linewidth=3)
    ax = plt.subplot(rows,2,8) 
    plot_style_mini(ax)
    home_isolation.variation_bar_plot(title=True)

    ax = plt.subplot(rows,2,9)
    plot_style_mini(ax)
    hospitalized.line_plot(title=True, marker='', linewidth=3)
    ax = plt.subplot(rows,2,10) 
    plot_style_mini(ax)
    hospitalized.variation_bar_plot(title=True)

    ax = plt.subplot(rows,2,11)
    plot_style_mini(ax)
    intensive_care.line_plot(title=True, marker='', linewidth=3)
    ax = plt.subplot(rows,2,12)
    plot_style_mini(ax)
    intensive_care.variation_bar_plot(title=True)

    ax = plt.subplot(rows,2,13)
    plot_style_mini(ax)
    deaths.line_plot(title=True, marker='', linewidth=3)
    ax = plt.subplot(rows,2,14)
    plot_style_mini(ax)
    deaths.variation_bar_plot(title=True)

    ax = plt.subplot(rows,2,15)
    plot_style_mini(ax)
    swabs.line_plot(title=True, marker='', linewidth=3)
    ax = plt.subplot(rows,2,16)
    plot_style_mini(ax)
    swabs.variation_bar_plot(title=True)

    if vaccine:
        ax = plt.subplot(rows,2,17)
        plot_style(ax)
        prima_dose.line_plot(title=True, marker='', linewidth=3)
        ax = plt.subplot(rows,2,18)
        plot_style(ax)
        prima_dose.variation_bar_plot(title=True)

        ax = plt.subplot(rows,2,19)
        plot_style(ax)
        seconda_dose.line_plot(title=True, marker='', linewidth=3)
        ax = plt.subplot(rows,2,20)
        plot_style(ax)
        seconda_dose.variation_bar_plot(title=True)
    

    """Fixing subplots overlapping"""
    fig.tight_layout()
    #plt.subplots_adjust(hspace = .4)

    if(images):
        plt.savefig(f'{path}mini_plots_{lastUpdate}.png', transparent=True)
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created mini_plots")

    if(screen):
        plt.show()

"""Plot that calculates the percentage of positive swabs out of on a daily basis """
fig, ax = plt.subplots(figsize=(19, 10))

plot_style(ax)

plt.title(f'Percentage of total cases variation / swabs variation (Today: {total_cases.daily_variation[-1]} / {swabs.daily_variation[-1]} * 100 = {round(total_cases.daily_variation[-1]/swabs.daily_variation[-1]*100,2)}%)')

percentages = [0 if x<=0 or y<=0 else x/y*100 for x,y in zip(total_cases.daily_variation[1:],swabs.daily_variation[1:])]
plt.bar(total_cases.dates[1:], percentages, color=active_cases.color, align='edge', zorder=2, width=1)

fig.tight_layout()

if(images):
    plt.savefig(f'{path}cases_swabs_{lastUpdate}.png', transparent=True)
    if(logging):
        print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created cases_swabs")

if(screen):
    plt.show()



if(vaccine):
    """line plot that shows first and second dose data """
    fig, ax = plt.subplots(figsize=(19, 10))
    plot_style(ax)

    prima_dose.line_plot()
    seconda_dose.line_plot()
    
    plt.title(f"Vaccines (Total:{prima_dose.data[-1]}, {seconda_dose.data[-1]})")
    plt.legend(loc="upper left")
    fig.tight_layout()

    if(images):
        plt.savefig(f'{path}vaccines_{lastUpdate}.png', transparent=True)
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created vaccines")

    if(screen):
        plt.show()



    """bar plot that shows first and second dose data per region """
    fig, ax = plt.subplots(figsize=(19, 10))

    p1 = plt.bar(cum_regioni.index,cum_regioni['prima_dose'], width=0.8, color=prima_dose.color)
    p2 = plt.bar(cum_regioni.index,cum_regioni['seconda_dose'], width=0.4, color=seconda_dose.color)
    plt.legend((p1[0], p2[0]), (prima_dose.name , seconda_dose.name))
    plt.box(False)
    plt.grid(True)
    plt.xticks(rotation=45)
    ax.set_axisbelow(True)
    
    plt.title("Vaccines used per region")
    fig.tight_layout()

    if(images):
        plt.savefig(f'{path}region_vaccines_{lastUpdate}.png', transparent=True)
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created region_vaccines")
            
    if(screen):
        plt.show()


    """Horizontal bar plot that shows percentages of vaccination per region """
    fig, ax = plt.subplots(figsize=(19, 10))
    #cum_regioni.sort_index(ascending=False)
    #print(cum_regioni.index)

    p1 = plt.barh(cum_regioni.index,[x/y*100 for x,y in zip(cum_regioni['prima_dose'],cum_regioni['pop'])], height=0.8, color=prima_dose.color)
    p2 = plt.barh(cum_regioni.index,[x/y*100 for x,y in zip(cum_regioni['seconda_dose'],cum_regioni['pop'])], height=0.4, color=seconda_dose.color)

    plt.xlim([-1,101])
    plt.legend((p1[0], p2[0]), (prima_dose.name , seconda_dose.name))
    plt.box(False)
    plt.grid(True)
    ax.set_axisbelow(True)
    
    plt.title("Percentage of vaccinated people per region")
    fig.tight_layout()

    if(images):
        plt.savefig(f'{path}region_vaccines_percentages_{lastUpdate}.png', transparent=True)
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created region_vaccines_percentages")
            
    if(screen):
        plt.show()
    
    """Bar plot that shows percentages of distributed vaccines per region """
    fig, ax = plt.subplots(figsize=(19, 10))

    distrib_percentages_first_dose = [x/y*100 for x,y in zip(cum_regioni['prima_dose'],cum_regioni['n_dosi'])]
    distrib_percentages_second_dose = [x/y*100 for x,y in zip(cum_regioni['seconda_dose'],cum_regioni['n_dosi'])]

    p1 = plt.bar(cum_regioni.index,distrib_percentages_first_dose, width=0.8, color=prima_dose.color)
    p2 = plt.bar(cum_regioni.index,distrib_percentages_second_dose, width=0.8, color=seconda_dose.color, bottom=distrib_percentages_first_dose)

    plt.legend((p1[0], p2[0]), (prima_dose.name , seconda_dose.name))
    plt.box(False)
    plt.grid(True)
    plt.xticks(rotation=45)
    ax.set_axisbelow(True)
    
    plt.title("Percentage of used vaccines out of distributed vaccines per region")
    fig.tight_layout()

    if(images):
        plt.savefig(f'{path}region_vaccines_distribution_percentages_{lastUpdate}.png', transparent=True)
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created region_vaccines_distribution_percentages")
            
    if(screen):
        plt.show()


    """Pie plot that shows italy vaccines suppliers and their percentages"""
    fig, ax = plt.subplots(figsize=(19, 10))
    distrib_percentages_fornitori = [x/cum_fornitori['numero_dosi'].sum()*100 for x in cum_fornitori['numero_dosi']]
    labels = cum_fornitori.index.values.tolist();

    plt.pie(distrib_percentages_fornitori, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.box(False)
    ax.set_axisbelow(True)
    
    plt.title("Vaccines suppliers")
    fig.tight_layout()

    if(images):
        plt.savefig(f'{path}region_vaccines_suppliers_pie_{lastUpdate}.png', transparent=True)
        if(logging):
            print(f"[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] Created vaccines_suppliers_percentages")
            
    if(screen):
        plt.show()