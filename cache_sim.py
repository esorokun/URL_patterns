from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt
import pandas as pd

n = 100

time_stamps = [datetime.now() + timedelta(seconds=random.random()) for i in range(n)]
time_stamps.sort()
major_iovs = [random.randint(0, 1000) for i in range(n)]
# urls = [f'payloadiovs/majorIOV={x}' for x in major_iovs]

raw_data = {'time_stamp': time_stamps, 'major_iov': major_iovs}#, 'url': urls}

cache = set()
db_counter = 0

for major_iov in major_iovs:
    if major_iov not in cache:
        db_counter += 1
        cache.add(major_iov)


print(f'db_counter = {db_counter}')


exit(0)


#def get(url):
#    if url not in cache:
#        cache[url] = database.get(url)
#    return cache[url]


df = pd.DataFrame(raw_data)

plt.plot(time_stamps, major_iovs)
plt.show()

print(df)