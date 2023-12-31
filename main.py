import pandas as pd
from log_reader import LogReader
from plot_builder import PlotBuilder
import matplotlib.pyplot as plt
from datetime import datetime
from cache_sim import CacheSim, create_sim_data

def log_build():
    log = LogReader('C:/Users/Ernest/PycharmProjects/URL Pattern seeker/files/log_file_full.txt',
                    'C:/Users/Ernest/PycharmProjects/URL Pattern seeker/files/output.csv')
    plots = PlotBuilder(log.log_read())
    plots.plot_top_6()
    plots.plot_build('minorIOV')


if __name__ == '__main__':
    for i in range(1, 2):
        df = create_sim_data(100, 15)
        cache = CacheSim(df, 10, 0)
        cache.cache_use()
