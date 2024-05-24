from telethon.sync import TelegramClient, events
import re
import config
import os, psutil

# API CONFIG
api_id = config.api_id
api_hash = config.api_hash
channel_id = config.channel_id

print(f"Memory used: {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2}MB")


def calculate_discount_percentage(message):
    if "gratis" in message or "free" in message:
        return 100

    for word in ["damen", "herren", "kinder"]:
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
        # Get information about the received message
        message = event.message
        await client.send_read_acknowledge(message.chat_id, message)
        discount_percentage = calculate_discount_percentage(message.message)
        if discount_percentage is not None and discount_percentage >= config.discount_val:
            await client.forward_messages(channel_id, message)
        print(f"The discount percentage is: {discount_percentage}%")


    client.run_until_disconnected()

