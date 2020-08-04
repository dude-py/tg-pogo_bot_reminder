# time_manager.py

import event
import config
import requests
import asyncio
import event_manager
from time import tzset, time
from os import environ


def get_sleep_time(current_time, min_time):
    sl = min_time - current_time
    if (sl < 0):
        raise ValueError(f"Sleep time should be positive integer. I got {sl}")
    return sl
###############################################################################


# setting time zone
environ['TZ'] = 'Europe/Kiev'
tzset()

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
    requests.post(config.outer_url, json=data)

    if e[3] > 0:
        e[1] = int(time()) + e[3]
        loop.create_task(timelapse(e, loop))


loop = asyncio.get_event_loop()
for e in event.read(config.table_name):
    loop.create_task(timelapse(list(e), loop))
loop.run_forever()
