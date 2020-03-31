import urllib.request, json 
import pandas as pd
import matplotlib.pyplot as plt

import warnings
import matplotlib.cbook
warnings.filterwarnings("ignore",category=matplotlib.cbook.mplDeprecation)

with urllib.request.urlopen("https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json") as url:
    """ data = json.loads(url.read().decode()) """
    covid_data_italy = pd.read_json(url.read().decode())
    fig, ax = plt.subplots(figsize=(19, 10))
    plt.title('Data starting from 24/02/2020')
    plt.ylabel('Cases')
    covid_data_italy['totale_casi'].plot(marker='o',color='darkred',label='cases')
    covid_data_italy['dimessi_guariti'].plot(marker='o',color='limegreen', label='cured')
    covid_data_italy['totale_positivi'].plot(marker='o',color='red',label='active cases')
    covid_data_italy['deceduti'].plot(marker='o',color='black', label='deaths')
    plt.legend(loc="upper left")
    fig.canvas.set_window_title('Covid-19')
    plt.show()

    fig, ax = plt.subplots(figsize=(19, 10))
    fig.canvas.set_window_title('Covid-19')
    """ fig.tight_layout() """
    plt.subplot(3,2,1)
    plt.title('Total cases starting from 24/02/2020')
    plt.ylabel('Cases')
    covid_data_italy['totale_casi'].plot(marker='o',color='red')
    
    plt.subplot(3,2,2)
    new_cases_per_day = list()
    for index, row in covid_data_italy.iterrows():
        if index > 0:
            new_cases_per_day.append(row['totale_casi']-covid_data_italy.iloc[index-1]['totale_casi'])
    plt.title('New daily cases starting 24/02/2020')
    plt.ylabel('Daily cases')
    plt.bar([i for i in range(len(new_cases_per_day))], new_cases_per_day, color='red')

    plt.subplot(3,2,3)
    plt.ylabel('Cases')
    plt.title('Total deaths starting 24/02/2020')
    covid_data_italy['deceduti'].plot(marker='o',color='black')

    plt.subplot(3,2,4)
    new_deaths_per_day = list()
    for index, row in covid_data_italy.iterrows():
        if index > 0:
            new_deaths_per_day.append(row['deceduti']-covid_data_italy.iloc[index-1]['deceduti'])
    plt.title('New daily deaths starting 24/02/2020')
    plt.ylabel('Daily deaths')
    plt.bar([i for i in range(len(new_deaths_per_day))], new_deaths_per_day, color='black')

    plt.subplot(3,2,5)
    plt.ylabel('Cases')
    plt.title('Total tests starting 24/02/2020')
    covid_data_italy['tamponi'].plot(marker='o',color='orange')

    plt.subplot(3,2,6)
    new_tests_per_day = list()
    for index, row in covid_data_italy.iterrows():
        if index > 0:
            new_tests_per_day.append(row['tamponi']-covid_data_italy.iloc[index-1]['tamponi'])
    plt.title('New daily tests starting 24/02/2020')
    plt.ylabel('Daily tests')
    plt.bar([i for i in range(len(new_tests_per_day))], new_tests_per_day, color='orange')
    
    plt.subplots_adjust(hspace = .4)
    plt.show()

    fig, ax = plt.subplots(figsize=(19, 10))
    plt.title('Hospital data from 24/02/2020')
    plt.ylabel('Cases')
    covid_data_italy['terapia_intensiva'].plot(marker='o',color='darkred',label='Intensive care')
    covid_data_italy['ricoverati_con_sintomi'].plot(marker='o',color='red', label='Hospitalized')
    covid_data_italy['dimessi_guariti'].plot(marker='o',color='limegreen',label='Cured')
    covid_data_italy['deceduti'].plot(marker='o',color='black', label='Deaths')
    plt.legend(loc="upper left")
    fig.canvas.set_window_title('Covid-19')
    plt.show()

    fig, ax = plt.subplots(figsize=(19, 10))
    fig.canvas.set_window_title('Covid-19')
    """ fig.tight_layout() """
    plt.subplot(3,2,1)
    plt.title('Intensive care patients starting from 24/02/2020')
    plt.ylabel('IEP')
    covid_data_italy['terapia_intensiva'].plot(marker='o',color='darkred')
    
    plt.subplot(3,2,2)
    new_IE_per_day = list()
    for index, row in covid_data_italy.iterrows():
        if index > 0:
            new_IE_per_day.append(row['terapia_intensiva']-covid_data_italy.iloc[index-1]['terapia_intensiva'])
    plt.title('New daily intensive care patients starting 24/02/2020')
    plt.ylabel('New daily IEP')
    plt.bar([i for i in range(len(new_IE_per_day))], new_IE_per_day, color='darkred')

    plt.subplot(3,2,3)
    plt.title('Hospitalized patients starting from 24/02/2020')
    plt.ylabel('HP')
    covid_data_italy['ricoverati_con_sintomi'].plot(marker='o',color='red')
    
    plt.subplot(3,2,4)
    new_HP_per_day = list()
    for index, row in covid_data_italy.iterrows():
        if index > 0:
            new_HP_per_day.append(row['ricoverati_con_sintomi']-covid_data_italy.iloc[index-1]['ricoverati_con_sintomi'])
    plt.title('New daily hospitalized patients starting 24/02/2020')
    plt.ylabel('New daily HP')
    plt.bar([i for i in range(len(new_HP_per_day))], new_HP_per_day, color='red')

    plt.subplot(3,2,5)
    plt.title('Cured patients starting from 24/02/2020')
    plt.ylabel('Cured')
    covid_data_italy['dimessi_guariti'].plot(marker='o',color='limegreen')
    
    plt.subplot(3,2,6)
    new_cured_per_day = list()
    for index, row in covid_data_italy.iterrows():
        if index > 0:
            new_cured_per_day.append(row['dimessi_guariti']-covid_data_italy.iloc[index-1]['dimessi_guariti'])
    plt.title('New daily cured patients starting 24/02/2020')
    plt.ylabel('New daily cured')
    plt.bar([i for i in range(len(new_cured_per_day))], new_cured_per_day, color='limegreen')

    plt.subplots_adjust(hspace = .4)
    plt.show()
