# ItalianCovidGraphs
Python program to make some plots with official italian covid and vaccine data
## You can see an updated version of the graphs [here](https://covid.fratorgano.me) 
## Features 
* Creates graph with official covid italian ~~spaghetti~~ data. 
  1. Line plot with total cases, cured, active cases, stay at home people and deaths.
  2. Line plot with hospitalized patients and  intensive care patients.
  3. Small line+bar plots. Line plots use total number and bar plots use day by day difference between data points. A pair of plots for all of the data types used above(+swabs).
  4. Plot with the percentage of daily positive swabs out ot all the swabs done that day.
  5. Line plot with first vaccine doses and seconda vaccine doses only.
  6. Bar plot with vaccines used per region.
  7. Horizontal bar plot with percentage of vaccinated people per region.
  8. Percentage of used vaccines out of distributed ones per region.
  9. Pie chart with vaccines suppliers.
* Fully adjustable output(and its location) through config.ini file.
* Checks if the downloaded data is updated before plotting. If it's not updated, waits 5 minutes and retries.

## What's new (02/02/2021)
* Added new plots with vaccines data
* Removed european plots (problem with data formats and timings)
* Bug fixing

## What's new (19/10/2020)
* Added a new plot with the percentage of daily positive swabs out ot all the swabs done that day
* Some bug fixing

## What's new (18/09/2020)
* Added a new plot with the top 20 european(continent) countries by number of new cases. 
* Improved performance a bit(still abysimal though).
* Now throws and exception if the config file is not read.
* Config settings now correctly used everywhere they should.
* Deletes old images so it won't fill your hdd.

## What's new (12/05/2020)
* The program now checks if the data was updated before graphing. If it wasn't, it waits 5 minutes and tries again.
* Fixed a bug showing a label on y axis on some plots that shouldn't have been there. 

## What's new (03/05/2020)
* The code is now more OOP friendly, thanks to the Sample class.
* Fixed a bug that showed the grid on top of bar plots.
* Fixed alignment of data with indicators on the axis. 
* Fixed a bug with the Output-images-to-Screen option in the config

## What's new (30/04/2020)
* Save the downloaded JSON data as json file (editable with config.ini file).
* Enabled grid for all plots.
* Now X axis values are dates instead of numbers. 
* Showing X axis values only every week, on mondays.

## Data
All data used is taken from [Presidenza del Consiglio dei Ministri/COVID-19](https://github.com/pcm-dpc/COVID-19) and [Italia/covid19-opendata-vaccini](https://github.com/italia/covid19-opendata-vaccini)

## 3rd party libraries used
* [Matplotlib](https://github.com/matplotlib/matplotlib)
* [Pandas](https://github.com/pandas-dev/pandas)
* [Numpy](https://github.com/numpy/numpy)
* [Requests](https://github.com/psf/requests)

