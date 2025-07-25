
import discord
from discord.ext import commands
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

def get_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = json.loads(os.environ["GOOGLE_CREDS_JSON"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("SzolgálatBot")
    return spreadsheet

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

active_users = {}

@bot.event
async def on_ready():
    print(f'Bejelentkezve mint {bot.user.name}')

bot.run(os.environ["DISCORD_TOKEN"])
