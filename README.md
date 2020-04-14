# ItalianCovidGraphs
Python program to make some plots with official italian covid data
## You can see an updated (every day at 18:05 CEST) version of the graphs [here](covid.fratorgano.me) 
## Features 
* Creates graph with official covid italian ~~spaghetti~~ data. 
  1. Line plot with total cases, cured, active cases and deaths
  2. Line plot with hospitalized patients, intensive care patients, cured patients and deaths
  3. Small line+bar plots. Line plots use total number and bar plots use day by day difference between data points. A pair of plots for all of the data types used above(+swabs).
* Fully adjustable output(and output location) through config.ini file.
## Data
All data used is taken from [Presidenza del Consiglio dei Ministri/COVID-19](https://github.com/pcm-dpc/COVID-19)
## 3rd party libraries used
* [Matplotlib](https://github.com/matplotlib/matplotlib)
* [Pandas](https://github.com/pandas-dev/pandas)
* [Urllib](https://github.com/urllib3/urllib3)
