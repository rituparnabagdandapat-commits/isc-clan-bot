import discord
from discord.ext import commands
from discord.ui import View, Button
import os
import asyncio
import random

# --- CONFIG ---
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# --- VIEWS (Persistent) ---
class VerifyView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="✅ Verify", style=discord.ButtonStyle.green, custom_id="verify_btn")
    async def verify(self, interaction: discord.Interaction, button: Button):
        role = discord.utils.get(interaction.guild.roles, name="Verified")
        if not role:
            role = await interaction.guild.create_role(name="Verified")
        await interaction.user.add_roles(role)
        await interaction.response.send_message("✅ You are verified!", ephemeral=True)

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🎫 Create Ticket", style=discord.ButtonStyle.blurple, custom_id="ticket_btn")
    async def ticket(self, interaction: discord.Interaction, button: Button):
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True)
        }
        channel = await interaction.guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
        await channel.send(f"{interaction.user.mention} Ticket created! Staff will be here soon.", view=CloseView())
        await interaction.response.send_message(f"Ticket created: {channel.mention}", ephemeral=True)

class CloseView(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.red, custom_id="close_btn")
    async def close(self, interaction: discord.Interaction, button: Button):
        await interaction.channel.delete()

# --- EVENTS ---
@bot.event
async def setup_hook():
    bot.add_view(VerifyView())
    bot.add_view(TicketView())
    bot.add_view(CloseView())
    # Try to load extra.py if exists, don't crash if not
    try:
        await bot.load_extension("extra")
        print("Loaded extra.py")
    except Exception as e:
        print(f"Skipping extra.py: {e}")

@bot.event
async def on_ready():
    print(f"🔥 ISC ULTRA GOD MODE {bot.user} - Bot is Online!")
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands!")
    except Exception as e:
        print(f"Sync failed: {e}")
    await bot.change_presence(activity=discord.Game(name="ISC Clan | !help"))

# --- SLASH COMMANDS (These will now show in Discord!) ---
@bot.tree.command(name="ping", description="Check bot ping")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"🏓 Pong! {round(bot.latency*1000)}ms")

@bot.tree.command(name="verify-panel", description="Send verify panel")
async def verify_panel(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admin!", ephemeral=True)
    embed = discord.Embed(title="ISC Verification", description="Click to verify and get access!", color=discord.Color.green())
    await interaction.response.send_message(embed=embed, view=VerifyView())
    # Send followup as actual panel
    await interaction.followup.send(embed=embed, view=VerifyView())

@bot.tree.command(name="ticket-panel", description="Send ticket panel")
async def ticket_panel(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Only admin!", ephemeral=True)
    embed = discord.Embed(title="ISC Support", description="Click to create a ticket!", color=discord.Color.blurple())
    await interaction.channel.send(embed=embed, view=TicketView())
    await interaction.response.send_message("Panel sent!", ephemeral=True)

# --- PREFIX COMMANDS (Your old ! commands - still work) ---
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency*1000)}ms")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 Kicked {member}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 Banned {member}")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    await ctx.channel.purge(limit=amount+1)
    await ctx.send(f"🧹 Cleared {amount} messages!", delete_after=3)

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="ISC Clan Bot Commands", color=0x00ff00)
    embed.add_field(name="!ping, !kick, !ban, !clear", value="Mod commands", inline=False)
    embed.add_field(name="/ping, /verify-panel, /ticket-panel", value="Slash commands", inline=False)
    await ctx.send(embed=embed)

# --- RUN ---
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
if not TOKEN:
    print("❌ ERROR: No TOKEN found in Environment Variables!")
else:
    bot.run(TOKEN)
