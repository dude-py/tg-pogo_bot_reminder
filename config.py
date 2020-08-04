# config.py

db_name = 'events.db'
outer_url = ''
table_name = 'events'
messages = 'messages'
schema = (
    'id', 'event_time', 'event_id', 'repeat', 'event_end'
)
messages_schema = (
    'id', 'event_id', 'message'
)
