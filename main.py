import pandas as pd
from log_reader import Log_reader
from plot_builder import Plot_builder
import matplotlib.pyplot as plt
from datetime import datetime

if __name__ == '__main__':
    log = Log_reader('C:/Users/Ernest/PycharmProjects/URL Pattern seeker/files/log_file_full.txt',
                     'C:/Users/Ernest/PycharmProjects/URL Pattern seeker/files/output.csv')
    plots = Plot_builder(log.log_read())
    plots.plot_top_6()
    plots.plot_build('minorIOV')
