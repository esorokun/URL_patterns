from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt
import pandas as pd


def create_sim_data(n, max_rand):
    time_stamps = [datetime.now() + timedelta(seconds=random.random()) for i in range(n)]
    time_stamps.sort()
    major_iovs = [random.randint(0, max_rand) for i in range(n)]

    # urls = [f'payloadiovs/majorIOV={x}' for x in major_iovs]

    raw_data = {'time_stamp': time_stamps, 'major_iov': major_iovs}#, 'url': urls}
    return pd.DataFrame(raw_data)


class CacheSim:
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def __str__(self):
        return f"This class was created for cache simulation"

    def plot_data(self):
        df = self.data_frame
        plt.scatter(df['time_stamp'], df['major_iov'])
        plt.show()

    def cache_use(self, show=False):
        cache = set()
        db_counter = 0
        df = self.data_frame
        major_iovs = df['major_iov']

        for major_iov in major_iovs:
            if major_iov not in cache:
                db_counter += 1
                cache.add(major_iov)

        print(f'db_counter = {db_counter}')

        if show:
            self.plot_data()



#def get(url):
#    if url not in cache:
#        cache[url] = database.get(url)
#    return cache[url]