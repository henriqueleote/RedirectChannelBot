import time

from telethon.sync import TelegramClient, events
import re
import redirect_config
import os, psutil

# API CONFIG
api_id = redirect_config.api_id
api_hash = redirect_config.api_hash
channel_id = redirect_config.channel_id

print(f"Memory used: {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2}MB")

lastWortenProductStatus = time.time()
lastTalkProductStatus = time.time()
wortenBotStatus = True
talkBotStatus = True


def calculate_discount_percentage(message):
    if "gratis" in message or "free" in message:
        return 100

    for word in ["herren", "kinder", "man", "men", "baby"]:
        if word in message.lower():
            print('skipped one')
            return None

    pattern = r"(\d{1,3}(?:[.,\s']?\d{3})*(?:,\d{2,})?)\s?€"
    prices = re.findall(pattern, message.lower())

    # Handle missing or multiple prices
    if not prices:
        return None
    elif len(prices) == 1:
        # Consider single price as original price (no discount)
        return 0
    else:
        # Assuming the highest price is the original price
        formatted_prices = [
            float(price.replace(',', '').replace('.', '')) for price in prices
        ]

        max_price = max(formatted_prices)
        min_price = min(formatted_prices)
        discount_percentage = ((max_price - min_price) / max_price) * 100
        return discount_percentage


with TelegramClient('session', api_id, api_hash) as client:
    @client.on(events.NewMessage(incoming=True))
    async def handle_new_message(event):

        global lastWortenProductStatus, lastTalkProductStatus, wortenBotStatus, talkBotStatus

        message = event.message
        await client.send_read_acknowledge(message.chat_id, message)

        # bot from status
        if message.chat_id == redirect_config.bot_status_id:
            if 'Last worten product' in message.message:
                lastWortenProductStatus = time.time()
                wortenBotStatus = True
            elif 'Last talk product' in message.message:
                lastTalkProductStatus = time.time()
                talkBotStatus = True

        # check if worten bot is down for 10 minutes
        if time.time() - lastWortenProductStatus > 300 and wortenBotStatus is True:
            lastWortenProductStatus = time.time()
            wortenBotStatus = False
            await client.send_message(channel_id, f'\u274c Worten bot is down. \u274c')
        elif wortenBotStatus is False and time.time() - lastWortenProductStatus > 1800:
            lastWortenProductStatus = time.time()
            await client.send_message(channel_id, '\u274c Worten bot is down. \u274c')

        # check if talkpoint bot is down for 10 minutes
        if time.time() - lastTalkProductStatus > 600 and talkBotStatus is True:
            lastTalkProductStatus = time.time()
            talkBotStatus = False
            await client.send_message(channel_id, '\u274c Talkpoint bot is down. \u274c')
        elif talkBotStatus is False and time.time() - lastTalkProductStatus > 1800:
            lastTalkProductStatus = time.time()
            await client.send_message(channel_id, '\u274c Talkpoint bot is down. \u274c')

        if message.chat_id in redirect_config.chat_list:
            discount_percentage = calculate_discount_percentage(message.message)
            if discount_percentage is not None and discount_percentage >= redirect_config.discount_val:
                await client.forward_messages(channel_id, message)
            print(f"The discount percentage is: {discount_percentage}%")


    client.run_until_disconnected()
