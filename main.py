import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("TOKEN") or os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.moderation = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} - ISC Bot Online!")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="!help | ISC Moderation"))

# ---------- BASIC ----------
@bot.tree.command(name="ping", description="Check if bot is alive")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency * 1000)}ms")

# ---------- MODERATION ----------
@bot.tree.command(name="kick", description="Kick a member")
@app_commands.describe(member="Who to kick", reason="Why")
@app_commands.default_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 Kicked {member.mention} | Reason: {reason}")

@bot.tree.command(name="ban", description="Ban a member")
@app_commands.describe(member="Who to ban", reason="Why")
@app_commands.default_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 Banned {member.mention} | Reason: {reason}")

@bot.tree.command(name="unban", description="Unban a user by ID")
@app_commands.describe(user_id="User ID to unban")
@app_commands.default_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    user = await bot.fetch_user(int(user_id))
    await interaction.guild.unban(user)
    await interaction.response.send_message(f"✅ Unbanned {user.mention}")

@bot.tree.command(name="clear", description="Delete messages")
@app_commands.describe(amount="How many to delete (1-100)")
@app_commands.default_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"🧹 Deleted {len(deleted)} messages!", ephemeral=True)

@bot.tree.command(name="timeout", description="Timeout a member")
@app_commands.describe(member="Who to timeout", minutes="How many minutes")
@app_commands.default_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int):
    import datetime
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason="Timeout by ISC Bot")
    await interaction.response.send_message(f"⏰ Timed out {member.mention} for {minutes} min")

@bot.tree.command(name="untimeout", description="Remove timeout")
@app_commands.describe(member="Who to untimeout")
@app_commands.default_permissions(moderate_members=True)
async def untimeout(interaction: discord.Interaction, member: discord.Member):
    await member.timeout(None)
    await interaction.response.send_message(f"✅ Removed timeout from {member.mention}")

@bot.tree.command(name="warn", description="Warn a member")
@app_commands.describe(member="Who to warn", reason="Why")
@app_commands.default_permissions(moderate_members=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason"):
    await interaction.response.send_message(f"⚠️ {member.mention} warned | Reason: {reason}")
    try:
        await member.send(f"You were warned in {interaction.guild.name} | Reason: {reason}")
    except:
        pass

# ---------- PREFIX TOO ----------
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR: No TOKEN found!")
    else:
        bot.run(TOKEN)
