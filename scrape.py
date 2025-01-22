import re
from telethon import TelegramClient
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient('anon', api_id, api_hash)

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, text)

async def scrape_message(client, channel, limit=100):
    emails = set() 
    async for message in client.iter_messages(channel, limit):
        if message.text:
            emails.update(extract_emails(message.text))  
    return emails

def check_and_insert_email(email):
    response = supabase.table("email-telegram1").select("email").eq("email", email).execute()
    if not response.data:
        supabase.table("email-telegram1").insert({"email": email}).execute()
        return f"Email inserido: {email}"
    return f"Email já existe: {email}"

async def main():
    channel_link = 't.me/vagastibr'
    emails = await scrape_message(client, channel_link, 200)
    print()
    for email in sorted(emails):
        result = check_and_insert_email(email)
        print(result)

with client:
    client.loop.run_until_complete(main())