# |*|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|*|
# |*| AUTHOR: Sandesh Gade                                  |*|
# |*| github: github.com/cyberbeast                         |*|
# |*| email: sandeshgade@gmail.com                          |*|
# |*|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|*|
# |*| ALGORITHM for script:                                 |*|
# |*| 1.    Loop through                                    |*|
# |*| 2.    ---- make request & start timer                 |*|
# |*| 3.    ---- check response status                      |*|
# |*| 4.    ---- if response status is 200                  |*|
# |*| 5.    ---- ---- stop timer, calculate elapsed time    |*|
# |*| 6.    ---- ---- push elapsed time to list             |*|
# |*| 7.    ---- else print appropriate message             |*|
# |*| 8.    Calculate min, max and average latency.         |*|
# |*| 9.    plot a graph and export graph as image.         |*|
# |*|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|*|

import sys
import requests
from requests.exceptions import HTTPError
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# read params
url = input('Enter url: \t')
max_hits = int(input('Enter max_hits: \t'))
time_between_hits = float(input('Enter time between hits: \t'))
file_prefix = str(input('Enter file prefix for graph file: \t'))

# init vars
cur_hits = 0
total_latency_list = []
round_trip_without_data_list = []
round_trip_time_data_only_list = []

while(cur_hits < max_hits):
    try:
        start = time.time()
        r = requests.get(url)
        r.raise_for_status()
        end = time.time()
        cur_hits += 1 #increment cur_hit counter
        round_trip = end - start
        round_trip_without_data = r.elapsed.total_seconds()

        print("HIT " + str(cur_hits) + "\t: STATUS " + str(r.status_code) + "\t: TOTAL " + str(round_trip) + "\t: INIT+HEADERS " + str(r.elapsed.total_seconds()) + "\t: DATA " + str(round_trip - round_trip_without_data))
        total_latency_list.append(round_trip)
        round_trip_without_data_list.append(r.elapsed.total_seconds())
        round_trip_time_data_only_list.append(round_trip - round_trip_without_data)
        time.sleep(time_between_hits)
    except HTTPError:
        print("HTTPError -- " + str(r.status_code))
        print("Exiting...")
        sys.exit()

print("Testing complete. Calculating results...")
print("MAX \t " + str(max(total_latency_list)))
print("MIN \t " + str(min(total_latency_list)))
print("AVG \t " + str(sum(total_latency_list)/len(total_latency_list)))

# GRAPHING
print("Results calculated. Generating graphs...")
ind = [x for x in range(max_hits)]
p1 = plt.bar(ind, round_trip_without_data_list, color='#d62728')
p2 = plt.bar(ind, round_trip_time_data_only_list, bottom=round_trip_without_data_list)
plt.ylabel('Latency (s)')
plt.xlabel('HIT')
plt.legend((p1[0], p2[0]), ('INIT+HEADERS', 'DATA'))
print("Saving graph as " + '"' + file_prefix + " " + time.strftime("%c") + '.png"')
plt.savefig(file_prefix + " " + time.strftime("%c"))
# plt.show()