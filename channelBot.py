import os

import psutil as psutil
from telethon import TelegramClient, events
import re

# Austrian number account
api_id = '24877751'
api_hash = 'aed5482cd0ee156892ac0eab0f2bf3f4'
channel_id = -1001921638321
client = TelegramClient('my-client', api_id, api_hash)
chat_list = [-1001314249243, -1001458489616, -1001174207332, -1001395637146, -1001007590845, -1001103963350, -1001493765825, -1001314084172, -1001537106037]


def calcDiscount(prices):
    prices.sort()
    print(prices)
    if prices[0] > prices[1]:
        max_val = prices[0]
        min_val = prices[1]
    else:
        max_val = prices[1]
        min_val = prices[0]
    val = float(max_val) - float(min_val)
    val2 = val / float(max_val)
    percentage_discount = format(val2 * 100, '.0f')
    print(f'% -> {percentage_discount}')
    return float(percentage_discount)


def getPercentage(text):
    #pattern = r"(\d{1,2}[.,]?\d{0,2})\s*€"  # Regex pattern to match prices after the Euro symbol
    pattern = r"(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{1,2})?)\s*€"
    matches = re.findall(pattern, text)
    if matches and len(matches) == 2:
        prices = [float(match.replace(',', '.')) for match in matches]
        return calcDiscount(prices)
    return False

@client.on(events.NewMessage(chats=chat_list))
async def my_event_handler(event):
    await event.message.mark_read()
    percentage = getPercentage(event.message.message)
    if (percentage):
        if(percentage) >= 65:
            await client.forward_messages(channel_id, event.message)
        else:
            print(f'{percentage} -> {event.message.message}')

async def send_start_message():
    channel = await client.get_entity(channel_id)
    print('running...')
    print(psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2)
    #await client.send_message(channel, "Now redirecting products with discount over 65%!")

client.start()
client.loop.run_until_complete(send_start_message())
client.run_until_disconnected()
