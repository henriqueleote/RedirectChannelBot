from telethon.sync import TelegramClient, events
import re
import config

# API CONFIG
api_id = config.api_id
api_hash = config.api_hash
channel_id = config.channel_id
chat_list = config.chat_list

while True:
    def calculate_discount_percentage(message):
        pattern = r"(\d{1,3}(?:[.,\s']?\d{3})*(?:,\d{2,})?)\s?€"
        if "gratis" in message or "grátis" in message or "free" in message:
            return 90
        prices = re.findall(pattern, message)
        formatted_prices = [float(price.replace(',', '.')) for price in prices]
        if len(formatted_prices) == 2:
            max_price = max(formatted_prices)
            min_price = min(formatted_prices)
            discount_percentage = ((max_price - min_price) / max_price) * 100
            return discount_percentage

        return None


    with TelegramClient('session', api_id, api_hash) as client:
        @client.on(events.NewMessage)
        async def handle_new_message(event):
            # Get information about the received message
            message = event.message
            if message.chat_id in chat_list:
                await client.send_read_acknowledge(message.chat_id, message)
                discount_percentage = calculate_discount_percentage(message.message)
                if discount_percentage is not None and discount_percentage >= 50:
                    await client.forward_messages(channel_id, message)
                print(f"The discount percentage is: {discount_percentage}%")


        client.run_until_disconnected()
