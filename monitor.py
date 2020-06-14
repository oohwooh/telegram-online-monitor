import os
from telethon import TelegramClient, events
import datetime
import logging
import random
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('online-monitor', api_id, api_hash)
client.start()
print('Logged in to telegram!')
last_seen = None


async def main():
    global last_seen
    watch_id = 116390971
    await client.get_dialogs()
    entity = await client.get_entity(watch_id)
    try:
        last_seen = entity.status.was_online
    except AttributeError:
        pass

    @client.on(events.UserUpdate(chats=watch_id))
    async def handler(event):
        global last_seen
        if event.status:
            if event.online and last_seen:
                now = datetime.datetime.now()
                delta = now.replace(tzinfo=None) - last_seen.replace(tzinfo=None)
                s = delta.total_seconds() + 18000  # Add 5 hours for whatever reason idk
                hours, remainder = divmod(s, 3600)
                minutes, seconds = divmod(remainder, 60)
                msg = 'May was offline for '
                if hours > 0:
                    msg += f'{int(hours)} hours, {int(minutes)} minutes, and {int(seconds)} seconds.'
                elif minutes > 0:
                    msg += f'{int(minutes)} minutes, and {int(seconds)} seconds.'
                else:
                    msg += f'{int(seconds)} seconds.'
                fluff = ['Welcome back cutie <3', 'We missed you!', 'I\'m so glad you\'re here :)']
                msg += ' '
                msg += random.choice(fluff)
                await client.send_message(-1001411926375, msg)
            else:
                last_seen = event.status.was_online
    await client.run_until_disconnected()
client.loop.run_until_complete(main())
