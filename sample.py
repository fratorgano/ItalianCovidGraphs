"""The class sample is used to store some information about a specific subset of the data and create plots based on it"""
from datetime import datetime

import matplotlib.pyplot as plt
from numpy import fix
import pandas as pd

class Sample:

    def __init__(self, data, starting_date, name='data', color='black', fix_zero=False):
        self.data = data
        self.name = name
        self.color = color
        starting_date = datetime.strptime(starting_date,'%Y-%m-%d')
        self.dates = pd.date_range(start=starting_date, periods=len(self.data))
        self.daily_variation = list()
        self.daily_variation.append(0)
        """Calcualting the difference between the current number of x and the last day number of x"""
        for index, d in enumerate(self.data[1:]):
            if(fix_zero):
                self.daily_variation.append(d-self.data[index] if d-self.data[index]>0 else 0)
            else:
                self.daily_variation.append(d-self.data[index])
        self.percentage_variation_total = 100*((self.data.iloc[-1]-self.data.iloc[-2])/(self.data.iloc[-2]))
        self.percentage_variation_variation = 100*((self.daily_variation[-1]-self.daily_variation[-2])/(self.daily_variation[-2]))
        #self.rolling_avg_14days_variation =  pd.DataFrame({'data':self.daily_variation}).rolling(14).mean()
        #print(self.rolling_avg_14days_variation)

        
    
    def line_plot(self, linewidth=2, linestyle='-', marker='o', title=False):
        if(title):
                plt.title(f'Number of {self.name} (Total: {self.data.iloc[-1]}, {self.percentage_variation_total:+.2f}%)')
        plt.plot_date(self.dates, self.data, color=self.color, label=self.name, linewidth=linewidth, linestyle=linestyle, marker=marker)
        
    
    def variation_bar_plot(self, title=False, linewidth=1, linestyle='-'):
        plt.bar(self.dates, self.daily_variation, color=self.color, align='edge', zorder=2, width=1)
        #plt.plot_date(self.dates, self.rolling_avg_14days_variation,color='black', linewidth=linewidth, linestyle=linestyle, marker='')
        
        if(title):
            plt.title(f'Daily {self.name} variation (Today: {self.daily_variation[-1]}, {self.percentage_variation_variation:+.2f}%)')
