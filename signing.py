from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient('anon', api_id, api_hash)

async def scrape_message(client, channel, limit=100 ):
  async for message in client.iter_messages(channel, limit):
    if message.text:
      print(message.text)

async def main():
  channel_link = 't.me/vagastibr'
  await scrape_message(client, channel_link, 5)

with client:
  client.loop.run_until_complete(main())