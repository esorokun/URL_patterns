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

    def plot_num(self, num_name):
        df = self.data_frame
        plt.scatter(x=df['timestamp'], y=df[num_name], s=2)
        plt.xlabel('Timestamp')
        plt.ylabel(num_name)
        plt.show()

    def plot_word(self, word_name):
        df = self.data_frame
        unique_words = list(set(df[word_name]))
        word_to_num = {word: i for i, word in enumerate(unique_words)}

        y = [word_to_num[word] for word in df[word_name]]

        plt.scatter(x=df['timestamp'], y=y, s=2)
        plt.xlabel('Timestamp')
        plt.ylabel(word_name)
        plt.yticks(range(len(unique_words)), unique_words)
        plt.show()
