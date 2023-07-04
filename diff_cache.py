from datetime import datetime, timedelta
import random
from abc import ABC
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

class Cache(ABC):
    def __init__(self):
        self.counter = 0

    def consider(self, time_stamp, value):
        return NotImplemented

    def get_size(self):
        return NotImplemented


class SimpleCache(Cache):
    def __init__(self):
        super().__init__()
        self.contents = set()

    def __str__(self):
        return self.__class__.__name__

    def consider(self, time_stamp, value):
        if value in self.contents:
            self.counter += 1
        self.contents.add(value)

    def get_size(self):
        return len(self.contents)


class TimedCache(Cache):
    def __init__(self, life_time=timedelta(days=1)):
        super().__init__()
        self.life_time = life_time
        self.value_ts_dict = {}  # {iov_1: ts_1, iov_2: ts_2, ...}

    def __str__(self):
        return self.__class__.__name__

    def consider(self, time_stamp, value):
        if value in self.value_ts_dict:
            old_ts = self.value_ts_dict[value]
            if (time_stamp - old_ts) < self.life_time:
                self.counter += 1
        self.value_ts_dict[value] = time_stamp

    def get_size(self):
        return len(self.value_ts_dict)


class SizeCache(Cache):
    def __init__(self, size=15):
        super().__init__()
        self.size = size
        self.contents = set()

    def __str__(self):
        return self.__class__.__name__

    def consider(self, time_stamp, value):
        if value in self.contents:
            self.counter += 1
        if len(self.contents) > self.size:
            self.contents.pop()
        self.contents.add(value)

    def get_size(self):
        return len(self.contents)


class LinearCache(Cache):
    def __init__(self, size=10):
        super().__init__()
        self.size = size
        self.value_ts_dict = {}  # {iov_1: ts_1, iov_2: ts_2, ...}
        self.prediction = {}

    def __str__(self):
        return self.__class__.__name__

    def consider(self, time_stamp, value):
        # if value in self.value_ts_dict:
        #     self.counter += 1
        if len(self.value_ts_dict) > 2:
            date_list = np.array(list(self.value_ts_dict.values()))
            timestamp = np.array([dt.timestamp() for dt in date_list])
            timestamp = timestamp.reshape(-1, 1)
            values = np.array(list(self.value_ts_dict.keys()))
            #print(timestamp)
            model = LinearRegression()
            model.fit(timestamp, values)
            X_pred = np.array([datetime.timestamp(time_stamp)]).reshape(1, -1)
            predicted_value = round(model.predict(X_pred)[0])
            # if predicted_value == value:
            #     self.counter += 1
            if predicted_value - 2 < value < predicted_value + 2:
                self.counter += 1

        if len(self.value_ts_dict) > self.size:
            del self.value_ts_dict[next(iter(self.value_ts_dict))]
        self.value_ts_dict[value] = time_stamp

    def get_size(self):
        return len(self.value_ts_dict)


def generate_ts_value_pairs(n=100):
    time_stamps = [datetime.now() + timedelta(seconds=random.random()) for i in range(n)]
    time_stamps.sort()
    values = [random.randint(0, 100) for i in range(n)]
    # time_stamps = [datetime.now() + timedelta(seconds=i) for i in range(n)]
    # values = [0 for _ in range(n)]
    return list(zip(time_stamps, values))


def linear_data(n=100, rand=2):
    time_stamps = [datetime.now() + timedelta(seconds=random.random()) for i in range(n)]
    time_stamps.sort()
    tm = np.array([tm.timestamp() for tm in time_stamps])
    start = tm[0]
    values = [round((i - start)*100) + random.randint(0, rand) for i in tm]
    return list(zip(time_stamps, values))


def test_cache(cache: Cache, ts_values_pairs):
    for ts, value in ts_values_pairs:
        cache.consider(ts, value)
    print(f'cache.counter of {str(cache)} = {cache.counter}')


if __name__ == '__main__':
    test_data = linear_data(300, 2) #generate_ts_value_pairs(100)
    test_cache(SimpleCache(), test_data)
    test_cache(TimedCache(life_time=timedelta(seconds=0.1)), test_data)
    test_cache(SizeCache(), test_data)
    test_cache(LinearCache(), test_data)

    array = linear_data()
    tm, values = zip(*array)
    plt.plot(tm, values)
    plt.show()


