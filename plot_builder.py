import pandas as pd
import datetime
import re
import time
import pytz
import numpy as np
from log_reader import Log_Reader
import seaborn as sns
import matplotlib.pyplot as plt


class Plot_builder:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def __str__(self):
        return f"Class that we are using to build plots from different features plot_build(feature)"

    def plot_build(self, name, show=1):
        df = self.data_frame
        if name in ['minorIOV', 'majorIOV']:
            y_axis = df[name]
        else:
            unique_names = list(set(df[name]))
            name_to_num = {word: i for i, word in enumerate(unique_names)}
            y_axis = [name_to_num[word] for word in df[name]]
            plt.yticks(range(len(unique_names)), unique_names)
        plt.scatter(x=df['timestamp'], y=y_axis, s=2)
        plt.xlabel('Timestamp')
        plt.ylabel(name)
        if show:
            plt.show()

    def plot_top_6(self):
        plt.subplot(2, 3, 1)
        self.plot_build('client IP', 0)
        plt.subplot(2, 3, 2)
        self.plot_build('majorIOV', 0)
        plt.subplot(2, 3, 3)
        self.plot_build('minorIOV', 0)
        plt.subplot(2, 3, 4)
        self.plot_build('request', 0)
        plt.subplot(2, 3, 5)
        self.plot_build('gtName', 0)
        plt.subplot(2, 3, 6)
        self.plot_build('status', 0)
        plt.show()

