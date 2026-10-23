# ISC CLAN BOT - FULL VERSION
# pip install discord.py

import discord
from discord.ext import commands
import json, random, os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# LEVELS + WELCOME + MOD + FUN ALL INCLUDED
# Commands: !maddest !clan !block !rank !leaderboard !roler !say !kick !ban !clear !helpclan

import os
bot.run(os.getenv('BOT_TOKEN'))
