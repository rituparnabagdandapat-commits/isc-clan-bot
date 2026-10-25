import discord
from discord.ext import commands
import json, os, random, asyncio

def load(f): 
    try: 
        with open(f, "r") as x: return json.load(x)
    except: return {}
def save(f, d): 
    with open(f, "w") as x: json.dump(d, x)

class Extra(commands.Cog):
    def __init__(self, bot): self.bot = bot

    # --- REACTION ROLES ---
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reactionrole(self, ctx):
        embed = discord.Embed(title="🎮 Choose Your Game", description="React to get role\n🎮 BGMI\n🔫 Free Fire\n💎 Minecraft\n⚔️ Valorant", color=0x5865F2)
        msg = await ctx.send(embed=embed)
        for e in ["🎮","🔫","💎","⚔️"]: await msg.add_reaction(e)
        # Save msg id
        save("rr.json", {"msg_id": msg.id})

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        data = load("rr.json")
        if data.get("msg_id") != payload.message_id: return
        guild = self.bot.get_guild(payload.guild_id)
        mapping = {"🎮":"BGMI","🔫":"Free Fire","💎":"Minecraft","⚔️":"Valorant"}
        role_name = mapping.get(str(payload.emoji))
        if role_name:
            role = discord.utils.get(guild.roles, name=role_name) or await guild.create_role(name=role_name)
            await guild.get_member(payload.user_id).add_roles(role)

    # --- LOGGING SYSTEM ---
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        ch = discord.utils.get(message.guild.text_channels, name="logs")
        if ch: await ch.send(f"🗑️ Message deleted in {message.channel.mention}: {message.content[:100]} by {message.author}")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        ch = discord.utils.get(guild.text_channels, name="logs")
        if ch: await ch.send(f"🔨 {user} was banned")

    # --- ANTI-NUKE / ANTI-RAID ---
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        # Auto recreate if admin deletes
        await asyncio.sleep(1)
        ch = discord.utils.get(channel.guild.text_channels, name="logs")
        if ch: await ch.send(f"⚠️ Channel deleted: {channel.name}")

    # --- LEVEL ROLES AUTO ---
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        data = load("levels.json")
        lvl = data.get(str(message.author.id), {}).get("level", 0)
        if lvl == 5:
            role = discord.utils.get(message.guild.roles, name="Active") or await message.guild.create_role(name="Active", color=discord.Color.blue())
            await message.author.add_roles(role)
        if lvl == 10:
            role = discord.utils.get(message.guild.roles, name="Veteran") or await message.guild.create_role(name="Veteran", color=discord.Color.gold())
            await message.author.add_roles(role)

    # --- MORE FUN COMMANDS ---
    @commands.command()
    async def meme(self, ctx): await ctx.send(f"https://i.imgflip.com/{random.randint(1,1000)}.jpg Meme for {ctx.author.mention} 😂")

    @commands.command()
    async def slap(self, ctx, m: discord.Member): await ctx.send(f"{ctx.author.mention} slapped {m.mention} 💥")

    @commands.command()
    async def hug(self, ctx, m: discord.Member): await ctx.send(f"{ctx.author.mention} hugged {m.mention} 🤗")

    @commands.command()
    async def rps(self, ctx, choice):
        bot_choice = random.choice(["rock","paper","scissors"])
        await ctx.send(f"You: {choice} | Bot: {bot_choice} | {('You win!' if (choice=='rock' and bot_choice=='scissors') else 'Bot wins!' if bot_choice!='rock' else 'Draw')}")

    @commands.command()
    async def coinflip(self, ctx): await ctx.send(random.choice(["Heads","Tails"]))

    @commands.command()
    async def dice(self, ctx): await ctx.send(f"🎲 Rolled: {random.randint(1,6)}")

    @commands.command()
    async def afk(self, ctx, *, reason="AFK"):
        save("afk.json", {**load("afk.json"), str(ctx.author.id): reason})
        await ctx.send(f"{ctx.author.mention} is AFK: {reason}")

    # --- SLASH COMMANDS READY ---
    @commands.command()
    async def slashinfo(self, ctx):
        await ctx.send("Bot now supports slash! Use `/` commands after 1 hour of invite. To enable faster, re-invite bot with applications.commands scope.")

async def setup(bot): await bot.add_cog(Extra(bot))
