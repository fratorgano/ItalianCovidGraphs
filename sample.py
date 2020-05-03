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
    
    def line_plot(self, linewidth=2, linestyle='-', marker='o', title=False):
        if(title):
            plt.title(f'Number of {self.name}')
        plt.ylabel(self.name)
        plt.plot_date(self.dates, self.data, color=self.color, label=self.name, linewidth=linewidth, linestyle=linestyle, marker=marker)
    
    def variation_bar_plot(self, title='False'):
        if(title):
            plt.title(f'Daily {self.name} variation')
        plt.ylabel(f'Number of {self.name}')
        daily_variation = list()
        """Adding the first value as 0 to have the same length for all the plots"""
        daily_variation.append(0)

        """Calcualting the difference between the current number of x and the last day number of x"""
        for index, d in enumerate(self.data[1:]):
            daily_variation.append(d-self.data[index])
        
        plt.bar(self.dates, daily_variation, color=self.color, align='edge', zorder=2, width=0.6)
