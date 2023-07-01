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
discount_val = 60

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
    prices = re.findall(pattern, text)
    formatted_prices = [price.replace('.', '').replace(',', '.') for price in prices]
    if len(formatted_prices) == 2:
        return calcDiscount(formatted_prices)
    return False

# Command handler for /changeDiscount command to change the minimum discount value
@client.on(events.NewMessage(pattern='/changeDiscount (\d+)'))
async def run_method_handler(event):
    global discount_val
    channel = await client.get_entity(channel_id)
    new_discount = event.pattern_match.group(1)
    discount_val = int(new_discount)
    await client.send_message(channel, f"Now redirecting channel products with discount over {discount_val}%!")
    await event.message.mark_read()

# Event handler for new messages in the specified chat_list
@client.on(events.NewMessage(chats=chat_list))
async def my_event_handler(event):
    await event.message.mark_read()
    percentage = getPercentage(event.message.message)
    if percentage:
        if percentage >= discount_val:
            await client.forward_messages(channel_id, event.message)

# Function to send a start message to the channel
async def send_start_message():
    print('running...')
    channel = await client.get_entity(channel_id)

# Start the client, run the send_start_message function, and run the client until disconnected
client.start()
client.loop.run_until_complete(send_start_message())
client.run_until_disconnected()
