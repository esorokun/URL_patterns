import pandas as pd
from log_reader import Log_Reader
from plot_builder import Plot_Builder
import matplotlib.pyplot as plt
from datetime import datetime

if __name__ == '__main__':
    log = Log_Reader('~/Desktop/log_file_full.txt', '~/Desktop/output.csv')
    plots = Plot_Builder(log.log_read())
    plots.plot_build('majorIOV')
