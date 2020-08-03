# time_manager.py

import event
import config
import requests
import asyncio
import event_manager
from time import tzset, time
from os import environ


def next_event(lst):
    """ return next event """
    tmp = (None, 99999999999)
    for i in lst:
        if(tmp[1] > i[1]):
            tmp = i
    return tmp


def get_sleep_time(current_time, min_time):
    sl = min_time - current_time
    if (sl < 0):
        raise ValueError(f"Sleep time should be positive integer. I got {sl}")
    return sl
###############################################################################


# setting time zone
environ['TZ'] = 'Europe/Kiev'
tzset()

# main
# while True:
#     events = event.read(config.table_name)
#     e = next_event(events)
#     current_time = int(time())
#     min_time = e[1]

#     # заснути на n секунд
#     sl = get_sleep_time(current_time, min_time)
#     mesg = event_manager.get_mesg(e[2])

#     print("\nsleep: " + str(sl))
#     print("next message: {}".format(mesg), end=" ", flush=True)
#     sleep(sl)

#     # отримати тепершній час
#     now = current_time - (current_time % 60)

#     data = {'update_id': 0, 'message': mesg, }
#     # requests.post(config.outer_url, json=data)
#     print(data)
#     print("   OK\n")

#     # delete old 'events' or update to new datetime
#     if (e[4] <= now) and (e[4] != 0):
#         event.delete(e[0])
#         continue

#     if e[3] > 0:
#         event.update(e[0], 'event_time', e[1] + e[3])
#         continue

#     event.delete(e[0])

# asyncronius version


async def timelapse(e, loop):
    current_time = int(time())
    min_time = e[1]

    # заснути на n секунд
    sl = get_sleep_time(current_time, min_time)
    mesg = event_manager.get_mesg(e[2])

    print("\nsleep: " + str(sl))
    print("next message: {}".format(mesg))

    await asyncio.sleep(sl)

    data = {'update_id': 0, 'message': mesg, }
    # requests.post(config.outer_url, json=data)
    print(data)

    if e[3] > 0:
        e[1] = int(time()) + e[3]
        loop.create_task(timelapse(e, loop))


loop = asyncio.get_event_loop()
for e in event.read(config.table_name):
    loop.create_task(timelapse(list(e), loop))
loop.run_forever()
