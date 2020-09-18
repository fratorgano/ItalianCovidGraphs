"""The class sample is used to store some information about a specific subset of the data and create plots based on it"""
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd

class Sample:

    def __init__(self, data, starting_date, name='data', color='black'):
        self.data = data
        self.name = name
        self.color = color
        starting_date = datetime.strptime(starting_date,'%Y-%m-%d')
        self.dates = pd.date_range(start=starting_date, periods=len(self.data))
        self.daily_variation = list()
        self.daily_variation.append(0)
        for index, d in enumerate(self.data[1:]):
            self.daily_variation.append(d-self.data[index])
    
    def line_plot(self, linewidth=2, linestyle='-', marker='o', title=False):
        if(title):
            plt.title(f'Number of {self.name} (Total: {self.data.iloc[-1]})')
        
        plt.plot_date(self.dates, self.data, color=self.color, label=self.name, linewidth=linewidth, linestyle=linestyle, marker=marker)
    
    def variation_bar_plot(self, title='False'):
        """Calcualting the difference between the current number of x and the last day number of x"""
        plt.bar(self.dates, self.daily_variation, color=self.color, align='edge', zorder=2, width=1)
        if(title):
            plt.title(f'Daily {self.name} variation (Today: {self.daily_variation[-1]})')
