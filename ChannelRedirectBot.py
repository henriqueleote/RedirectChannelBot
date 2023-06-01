from telethon import TelegramClient, events
import re

# Austrian number account
api_id = '24877751'
api_hash = 'aed5482cd0ee156892ac0eab0f2bf3f4'
channel_id = -1001921638321
client = TelegramClient('my-client', api_id, api_hash)
chat_list = [-1001314249243, -1001458489616, -1001174207332, -1001395637146, -1001007590845, -1001103963350, -1001493765825, -1001314084172, -1001537106037]
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
    pattern = r'(\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?)\s?€'
    prices = re.findall(pattern, text)
    formatted_prices = [price.replace(',', '.') for price in prices]
    print(formatted_prices)
    if len(formatted_prices) == 2:
        return calcDiscount(formatted_prices)
    return False

# Event handler for new messages in the specified chat_list
@client.on(events.NewMessage(chats=chat_list))
async def my_event_handler(event):
    await event.message.mark_read()
    percentage = getPercentage(event.message.message)
    if percentage:
        if percentage >= discount_val:
            await client.forward_messages(channel_id, event.message)
        else:
            print(f'{event.message.message} -> {percentage}% discount')

# Function to send a start message to the channel
async def send_start_message():
    channel = await client.get_entity(channel_id)
    print('running...')
    await client.send_message(channel, f"Now redirecting channel products with discount over {discount_val}%!")

# Start the client, run the send_start_message function, and run the client until disconnected
client.start()
client.loop.run_until_complete(send_start_message())
client.run_until_disconnected()
