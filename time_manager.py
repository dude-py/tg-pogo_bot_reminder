# time_manager.py

import event
import config
import requests
from time import sleep, tzset
from datetime import datetime
from os import environ


def new_event(event_time, msg, repeat, event_end=0):
    """ event_time - INTEGER, should be time in the future
        in seconds with epoch start
        msg - STRING, the message
        is_regular - BOOLEAN, is regular event?
    """
    if(type(event_time) != int):
        raise TypeError("type err: event_time should be integer")
    if(event_time < int(datetime.now().timestamp())):
        raise Exception("it's no make sense. Time should be in the future")
    if(type(msg) != str):
        raise TypeError("type err: msg shoud be a string")
    if(type(repeat) != int):
        raise TypeError("is_regular should be an INTEGER")

    event.create(event_time, msg, repeat, event_end)


def next_event(lst):
    """ return next event """
    tmp = (None, 99999999999)
    for i in lst:
        if(tmp[1] > i[1]):
            tmp = i
    return tmp
###############################################################################


hour = 3600
week = 604800
timeout = hour

# setting time zone
environ['TZ'] = 'Europe/Kiev'
tzset()

# setting 'events'
spotlight_hour = int(datetime(2020, 7, 14, 18, 0).timestamp())
baloon_time = int(datetime(2020, 7, 14, 18, 0).timestamp())
baloon_time_limeted = int(datetime(2020, 7, 14, 15, 0).timestamp())
end = int(datetime(2020, 7, 15, 21, 0).timestamp())

# add 'events'
new_event(
    spotlight_hour,
    '''Spotlight hour start now!''',
    week
)
new_event(
    baloon_time,
    "Повітряна куля команди R знову з'явилася в піксельному небі.",
    hour * 6,
)
new_event(
    baloon_time_limeted,
    "Це птах? Це літак? Ні, це супе.. це повітряна куля команди Р.",
    hour * 6,
    end
)

# main
while True:
    events = event.read()
    e = next_event(events)
    min_time = e[1]

    # заснути на n секунд
    current_time = int(datetime.now().timestamp())
    sl = 0
    if (min_time > current_time):
        sl = min_time - current_time
    else:
        raise ValueError(
            "\nSleep time should be positive integer. I got {}".format(sl)
            )

    print("next message: {}".format(e[2]), end=" ", flush=True)
    print("\nsleep: " + str(sl))
    sleep(sl)

    # отримати тепершній час
    t1 = datetime.now()
    now = int(t1.timestamp()) - t1.second

    data = {'update_id': 0, 'message': e[2], }
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
