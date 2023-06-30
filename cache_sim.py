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


class UniqueList(list):
    def append(self, item):
        if item in self:
            self.remove(item)
        super().append(item)
        print(self[0][0])
        #for item in self:
         #   item[1] -= 1
          #  if item[1] <= 0:
           #     self.remove(item)


class CacheSim:
    def __init__(self, data_frame, max_cache_size, life_time):
        self.data_frame = data_frame
        self.max_cache_size = max_cache_size
        self.life_time = life_time

    def __str__(self):
        return f"This class was created for cache simulation"

    def plot_data(self):
        df = self.data_frame
        plt.scatter(df['time_stamp'], df['major_iov'])
        plt.show()

    def cache_use(self, show=False):
        cache = UniqueList()
        db_counter = 0
        df = self.data_frame
        major_iovs = df['major_iov']

        for major_iov in major_iovs:
            if major_iov not in (item[0] for item in cache):
                db_counter += 1
                cache.append([major_iov, self.life_time])
                if len(cache) >= self.max_cache_size:
                    del cache[0]
            else:
                cache.append([major_iov, self.life_time])
            #print(cache)
        print(f'db_counter = {db_counter}')
        print(f'cache % = {round(1 - db_counter/len(major_iovs),2)}')

        if show:
            self.plot_data()



#def get(url):
#    if url not in cache:
#        cache[url] = database.get(url)
#    return cache[url]