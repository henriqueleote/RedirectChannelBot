# Telegram Channel Discount Forwarder

This script forwards messages from Telegram channels to another channel if they contain a specified discount percentage. It uses the Telethon library to interact with the Telegram API and provides functionality to calculate and filter messages based on the discount percentage.

## Requirements

- Telethon

## Installation

1. Clone the repository:

```python
git clone https://github.com/henriqueleote/RedirectChannelBot.git
cd RedirectChannelBot
```

2. Install the required dependencies:

```python
pip install -r requirements.txt

```

3. Obtain API credentials by creating a Telegram application. Refer to the Telethon documentation for detailed instructions.

4. Update the `api_id` and `api_hash` variables in the script with your API credentials.

5. Update the `channel_id` variable with the ID of the channel where you want to forward the messages.

6. Customize the `chat_list` variable with the list of channel IDs you want to monitor for discount messages.

7. Adjust the `discount_val` variable to specify the minimum discount percentage required for forwarding a message.

## Usage

1. Run the script:

```python
py ChannelRedirectBot.py
```
2. The script will start monitoring the specified channels for new messages.

3. When a new message arrives, it will check if it contains a discount percentage. If the percentage is equal to or greater than the `discount_val` or contains the words "free" or "gratis", the message will be forwarded to the specified channel.

## Customization

- You can modify the `getPercentage()` function to adjust the pattern used for extracting prices and calculating the discount percentage.
- Customize the `discount_val` variable to set your desired minimum discount percentage.
- Adjust the `chat_list` variable to include the IDs of the channels you want to monitor.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

[MIT License](LICENSE)
