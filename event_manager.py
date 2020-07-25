import config
import event
import random
import time
# from time import tzset, time
from datetime import datetime
from os import environ

# setting time zone
environ['TZ'] = 'Europe/Kiev'
time.tzset()

hour = 3600
week = 604800
timeout = hour


def get_mesg(event_id):
    messages = event.read(config.messages, 'message', event_id)
    mesg = messages[random.randint(0, len(messages)-1)][0]
    return mesg


def new_event(event_time, event_id, repeat, event_end=0, mesgs=[]):
    """ event_time - INTEGER, should be time in the future
        in seconds with epoch start
        msg - STRING, the message
        is_regular - BOOLEAN, is regular event?
    """
    if(type(event_time) != int):
        raise TypeError("type err: event_time should be integer")
    if(event_time < int(time.time())):
        raise Exception("it's no make sense. Time should be in the future")
    if(type(event_id) != str):
        raise TypeError("type err: msg shoud be a string")
    if(type(repeat) != int):
        raise TypeError("is_regular should be an INTEGER")

    event.create(
        config.table_name, config.schema[1:],
        event_time, event_id, repeat, event_end
        )

    if len(mesgs) > 0:
        for msg in mesgs:
            event.create(
                config.messages, config.messages_schema[1:],
                event_id, msg
                )


if(__name__ == "__main__"):
    # setting 'events'
    spotlight_hour = int(datetime(2020, 7, 21, 18, 0).timestamp())
    raid_hour = int(datetime(2020, 7, 22, 18, 0).timestamp())
    baloon_time = int(datetime(2020, 7, 16, 6, 0).timestamp())
    go_fest = int(datetime(2020, 7, 17, 8, 0).timestamp())
    cd_start = int(datetime(2020, 7, 19, 11, 0).timestamp())

    # add 'events'
    msg = ["Spotlight hour start now! В центрі увагі Одіш та 2х пилі за ловлю"]
    new_event(
        spotlight_hour,
        "spotlight_hour",
        week,
        mesgs=msg,
    )

    msg = ["Година рейдів почалася! Кайрем вже на всіх джимах!"]
    new_event(
        raid_hour,
        "raid_hour",
        week,
        mesgs=msg
    )

    go_fest_msg = ["Новий покемон, Петіліл, почав з`являтися в Pokemon GO,\
 а також можна знайти шайні Белспраут та Пікачу в літній шапці -- це почалася\
 'GO Fest Weekly Challenge: Friendship'. P.S. Не забудьте сфотографувати свого\
 улюбленого покемона ;)"]
    new_event(
        go_fest,
        'go_fest',
        0,
        mesgs=go_fest_msg
    )

    msg = ["День спільноти з Гастлі почався! Від тепер і до 17:00 інкубатори \
будуть на 1/4 ефективніші, інсенс працюватиме 3 години, а Генгар зможе вивчити\
 атаку 'Shadow punch'. Приємного полювання за привидами."]
    new_event(
        cd_start,
        'community_day',
        0,
        mesgs=msg,
    )

    msg = [
        "Повітряна куля команди Р знову на піксельному небі",
        "Це птах? Це літак? Ні, це су... це повітряна куля команди Р)",
        "Там воздушный шар команды Р. Попробуй ещё разок, а то сидишь без\
 шайни, шадоу кофинга/еканса как лох",
        "Команда R опять хочет в тартарары",
        "Команда Пакетов на воздушном мяуткабриолете желает улететь\
 в красивом пируэте",
        "Эув слушь, кожаные мешки!? Там виртуальная реальность\
 бросает вам вызов",
        "Команда Р знову на горизонті та хоче викрасти ваших покемонів",
    ]
    new_event(
        baloon_time,
        "baloon",
        hour * 6,
        mesgs=msg,
    )
