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
    print(f'✅ Bejelentkezve mint {bot.user.name}')

@bot.command()
async def belép(ctx):
    user = str(ctx.author)
    now = datetime.now()
    active_users[user] = now
    await ctx.send(f"✅ {user} szolgálatba lépett: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    sheet = get_sheet().worksheet("Aktív")
    sheet.append_row([user, now.strftime("%Y-%m-%d %H:%M:%S"), "", ""])

@bot.command()
async def kilép(ctx):
    user = str(ctx.author)
    now = datetime.now()
    if user in active_users:
        start = active_users.pop(user)
        elapsed = int((now - start).total_seconds() / 60)
        await ctx.send(f"🚪 {user} kilépett. Szolgálatban töltött idő: {elapsed} perc.")
        sheet = get_sheet().worksheet("Aktív")
        records = sheet.get_all_records()
        for i, record in enumerate(records, start=2):
            if record['Név'] == user and record['Kijelentkezett'] == "":
                sheet.update_cell(i, 3, now.strftime("%Y-%m-%d %H:%M:%S"))
                sheet.update_cell(i, 4, str(elapsed))
                break
    else:
        await ctx.send("❌ Nem voltál szolgálatban!")

bot.run(os.environ["MTM5NjU0NTYxMzU5NTgwMzg0OA.GgoOk_.Dh7gjfAxzVfAnaZbuoZoys_ruvJtBhZ-nrGShk"])
