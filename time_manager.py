# time_manager.py

import event
import config
import requests
import event_manager
from time import sleep, tzset
from datetime import datetime
from os import environ


def next_event(lst):
    """ return next event """
    tmp = (None, 99999999999)
    for i in lst:
        if(tmp[1] > i[1]):
            tmp = i
    return tmp


def get_sleep_time():
    current_time = int(datetime.now().timestamp())
    sl = 0
    if (min_time >= current_time):
        sl = min_time - current_time
    else:
        raise ValueError(
            "\nSleep time should be positive integer. I got {}".format(sl)
            )
    return sl
###############################################################################


# setting time zone
environ['TZ'] = 'Europe/Kiev'
tzset()

# main
while True:
    events = event.read(config.table_name)
    e = next_event(events)
    min_time = e[1]

    # заснути на n секунд
    sl = get_sleep_time()
    mesg = event_manager.get_mesg(e[2])

    print("\nsleep: " + str(sl))
    print("next message: {}".format(mesg), end=" ", flush=True)
    sleep(sl)

    # отримати тепершній час
    t1 = datetime.now()
    now = int(t1.timestamp()) - t1.second

    data = {'update_id': 0, 'message': mesg, }
    requests.post(config.outer_url, json=data)
    print("   OK\n")

    # delete old 'events' or update to new datetime
    if (e[4] <= now) and (e[4] != 0):
        event.delete(e[0])
        continue

    if e[3] > 0:
        event.update(e[0], 'event_time', e[1] + e[3])
        continue

    event.delete(e[0])
