import pandas as pd
import datetime
import re
import time
import pytz
import numpy as np
from log_reader import Log_Reader
import seaborn as sns
import matplotlib.pyplot as plt

class Plot_Builder:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def __str__(self):
        return f"Class that we are using to build plots from different features \n" \
               f"For major and minor IOV you can use plot_num() \n" \
               f"If you are trying to build plot for words (gtName, client IP) - try plot_word()"

    def plot_build(self, name):
        df = self.data_frame
        if name in ['minorIOV', 'majorIOV', 'status']:
            y_axis = df[name]
        else:
            unique_names = list(set(df[name]))
            name_to_num = {word: i for i, word in enumerate(unique_names)}
            y_axis = [name_to_num[word] for word in df[name]]
            plt.yticks(range(len(unique_names)), unique_names)
        plt.scatter(x=df['timestamp'], y=y_axis, s=2)
        plt.xlabel('Timestamp')
        plt.ylabel(name)
        plt.show()

