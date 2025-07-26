import 1396545613595803848
from discord.ext import commands
from datetime import datetime

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

active_users = {}

@bot.command()
async def belép(ctx):
    user = str(ctx.author)
    now = datetime.now()
    active_users[user] = now
    await ctx.send(f"✅ {user} szolgálatba lépett: {now.strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command()
async def kilép(ctx):
    user = str(ctx.author)
    now = datetime.now()
    if user in active_users:
        start = active_users.pop(user)
        elapsed = int((now - start).total_seconds() / 60)
        await ctx.send(f"🚪 {user} kilépett. Szolgálatban töltött idő: {elapsed} perc.")
    else:
        await ctx.send("❌ Nem voltál szolgálatban!")

bot.run(MTM5NjU0NTYxMzU5NTgwMzg0OA.GgoOk_.Dh7gjfAxzVfAnaZbuoZoys_ruvJtBhZ-nrGShk)