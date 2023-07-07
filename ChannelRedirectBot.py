from telethon import TelegramClient, events
import re
import config

# API CONFIG
api_id = config.api_id
api_hash = config.api_hash
channel_id = config.channel_id
client = TelegramClient('my-client', api_id, api_hash)
chat_list = config.chat_list

# Minimum discount to redirect
discount_val = 45

# Function to calculate the percentage discount based on prices
def calcDiscount(prices):
    prices.sort()
    if prices[0] > prices[1]:
        max_val = prices[0]
        min_val = prices[1]
    else:
        max_val = prices[1]
        min_val = prices[0]
    val = float(max_val) - float(min_val)
    val2 = val / float(max_val)
    percentage_discount = format(val2 * 100, '.0f')
    return float(percentage_discount)

# Function to extract prices from text and calculate the percentage discount
def getPercentage(text):
    pattern = r"(\d{1,3}(?:[.,\s']?\d{3})*(?:[.,]\d+)?)\s?€"
    if "gratis" in text or "grátis" in text or "free" in text:
        return 90
    prices = re.findall(pattern, text)
    formatted_prices = [price.replace('.', '').replace(',', '.') for price in prices]
    print(formatted_prices)
    if len(formatted_prices) == 2:
        return calcDiscount(formatted_prices)
    return False


# Event handler for new messages in the specified chat_list
@client.on(events.NewMessage)
async def my_event_handler(event):
    await event.message.mark_read()
    percentage = getPercentage(event.message.message)
    if percentage and percentage >= discount_val:
        await client.forward_messages(channel_id, event.message)
    else:
        print(percentage)

# Start the client, run the send_start_message function, and run the client until disconnected
client.start()
client.run_until_disconnected()
