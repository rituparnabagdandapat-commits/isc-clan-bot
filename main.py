import os
import discord
from discord.ext import commands

# Bot-Hosting reads TOKEN from Environment Variables, not from code
TOKEN = os.getenv("TOKEN") or os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} - ISC Bot Online!")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="!help | ISC Bot"))

@bot.tree.command(name="ping", description="Check if bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms - ISC Bot Online!")

@bot.tree.command(name="hello", description="Say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}! 👋 Welcome to ISC!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: No TOKEN found! Put TOKEN in Bot-Hosting Environment Variables")
    else:
        bot.run(TOKEN)
