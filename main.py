# ISC ULTRA v100 - 100 SLASH + PREFIX - FINAL - CLEANED
import discord, asyncio, json, os, random, io
from discord.ext import commands
from discord.ui import View
from datetime import timedelta
from PIL import Image, ImageDraw, ImageFont
import aiohttp

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# 👑 PUT YOUR DISCORD ID HERE
OWNER_ID = 123456789012345678  # <-- change this to your ID

for f, d in [("levels.json", {}), ("economy.json", {}), ("wars.json", {}), ("invites.json", {}), ("warnings.json", {})]:
    if not os.path.exists(f):
        open(f, "w").write("{}")

def load(f): 
    try: return json.load(open(f,"r"))
    except: return {}
def save(f,d): json.dump(d, open(f,"w"), indent=4)

class TicketView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green, custom_id="ticket_v3")
    async def create(self, interaction, button):
        if discord.utils.get(interaction.guild.text_channels, name=f"ticket-{interaction.user.name.lower()}"):
            return await interaction.response.send_message("Ticket exists!", ephemeral=True)
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False), interaction.user: discord.PermissionOverwrite(view_channel=True), interaction.guild.me: discord.PermissionOverwrite(view_channel=True)}
        ch = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", overwrites=overwrites)
        await ch.send(embed=discord.Embed(title="ISC SUPPORT", description=f"{interaction.user.mention} Support here!", color=0x00ff00), view=CloseView())
        await interaction.response.send_message(f"Created {ch.mention}", ephemeral=True)

class CloseView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Close", style=discord.ButtonStyle.red, custom_id="close_v3")
    async def close(self, interaction, button):
        await interaction.response.send_message("Closing 3s..."); await asyncio.sleep(3); await interaction.channel.delete()

class VerifyView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Verify", style=discord.ButtonStyle.green, custom_id="verify_v3")
    async def verify(self, interaction, button):
        role = discord.utils.get(interaction.guild.roles, name="ISC Member") or await interaction.guild.create_role(name="ISC Member", color=discord.Color.green())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("Verified!", ephemeral=True)

def get_chat_reply(username, message):
    msg = message.lower()
    if any(w in msg for w in ["hi","hey","hello","yo"]): return f"Yo {username}! ISC Sniper here!"
    if "event" in msg: return "Halloween till Nov 3! Farm keys!"
    if "rivals" in msg: return "Rivals: Sniper+Katana OP!"
    if "bye" in msg or "gn" in msg: return f"GN {username}!"
    return f"Yeah {username}, {message} - ISC OP!"

@bot.event
async def on_ready():
    bot.add_view(TicketView()); bot.add_view(CloseView()); bot.add_view(VerifyView())
    synced = await bot.tree.sync()
    print(f"ISC 100 SLASH {bot.user} - {len(synced)} commands synced!")

@bot.event
async def on_message(message):
    if message.author.bot: return
    if not message.author.guild_permissions.manage_messages:
        if "discord.gg" in message.content or ("http://" in message.content and "tenor" not in message.content):
            await message.delete()
            return await message.channel.send(f"{message.author.mention} No links!", delete_after=5)
    data=load("levels.json"); uid=str(message.author.id)
    if uid not in data: data[uid]={"xp":0,"level":1}
    data[uid]["xp"]+=5
    if data[uid]["xp"]>=data[uid]["level"]*100: data[uid]["level"]+=1; await message.channel.send(f"GG {message.author.mention} Level {data[uid]['level']}!")
    save("levels.json", data)
    if bot.user in message.mentions:
        clean=message.content.replace(f'<@{bot.user.id}>','').strip() or "hi"
        await message.reply(get_chat_reply(message.author.name, clean))
    await bot.process_commands(message)

# 100 HYBRID COMMANDS
@bot.hybrid_command(name="kick", description="Kick member")
async def kick(ctx, m: discord.Member, *, r="No reason"): await m.kick(reason=r); await ctx.send(f"Kicked {m}")
@bot.hybrid_command(name="ban", description="Ban member")
async def ban(ctx, m: discord.Member, *, r="No reason"): await m.ban(reason=r); await ctx.send(f"Banned {m}")
@bot.hybrid_command(name="timeout", description="Timeout")
async def timeout(ctx, m: discord.Member, min: int=10): await m.timeout(discord.utils.utcnow()+timedelta(minutes=min)); await ctx.send(f"Timeout {m}")
@bot.hybrid_command(name="clear", description="Clear")
async def clear(ctx, a: int=10): await ctx.channel.purge(limit=a+1)
@bot.hybrid_command(name="nuke", description="Nuke")
async def nuke(ctx): await ctx.channel.clone(); await ctx.channel.delete()
@bot.hybrid_command(name="warn", description="Warn")
async def warn(ctx, m: discord.Member, *, r="Warn"): d=load("warnings.json"); d[str(m.id)]=d.get(str(m.id),0)+1; save("warnings.json", d); await ctx.send(f"Warned {m}")
@bot.hybrid_command(name="warnings", description="Warnings")
async def warnings(ctx, m: discord.Member): d=load("warnings.json"); await ctx.send(f"{d.get(str(m.id),0)} warns")
@bot.hybrid_command(name="unwarn", description="Unwarn")
async def unwarn(ctx, m: discord.Member): d=load("warnings.json"); d[str(m.id)]=0; save("warnings.json", d); await ctx.send("Cleared")
@bot.hybrid_command(name="mute", description="Mute")
async def mute(ctx, m: discord.Member): r=discord.utils.get(ctx.guild.roles, name="Muted") or await ctx.guild.create_role(name="Muted"); await m.add_roles(r); await ctx.send(f"Muted {m}")
@bot.hybrid_command(name="unmute", description="Unmute")
async def unmute(ctx, m: discord.Member): r=discord.utils.get(ctx.guild.roles, name="Muted"); await m.remove_roles(r); await ctx.send(f"Unmuted {m}")
@bot.hybrid_command(name="lock", description="Lock")
async def lock(ctx): await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False); await ctx.send("Locked")
@bot.hybrid_command(name="unlock", description="Unlock")
async def unlock(ctx): await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True); await ctx.send("Unlocked")
@bot.hybrid_command(name="role", description="Give role")
async def role(ctx, m: discord.Member, *, role_name): r=discord.utils.get(ctx.guild.roles, name=role_name); await m.add_roles(r); await ctx.send("Gave role")
@bot.hybrid_command(name="removerole", description="Remove role")
async def removerole(ctx, m: discord.Member, *, role_name): r=discord.utils.get(ctx.guild.roles, name=role_name); await m.remove_roles(r); await ctx.send("Removed")
@bot.hybrid_command(name="nick", description="Nick")
async def nick(ctx, m: discord.Member, *, n): await m.edit(nick=n); await ctx.send(f"Nick {n}")
@bot.hybrid_command(name="balance", description="Balance")
async def balance(ctx): eco=load("economy.json"); await ctx.send(f"${eco.get(str(ctx.author.id),0)}")
@bot.hybrid_command(name="bal", description="Bal")
async def bal(ctx): eco=load("economy.json"); await ctx.send(f"${eco.get(str(ctx.author.id),0)}")
@bot.hybrid_command(name="daily", description="Daily")
async def daily(ctx): eco=load("economy.json"); eco[str(ctx.author.id)]=eco.get(str(ctx.author.id),0)+500; save("economy.json", eco); await ctx.send("Daily $500")
@bot.hybrid_command(name="work", description="Work")
async def work(ctx): e=random.randint(100,400); eco=load("economy.json"); eco[str(ctx.author.id)]=eco.get(str(ctx.author.id),0)+e; save("economy.json", eco); await ctx.send(f"+${e}")
@bot.hybrid_command(name="rob", description="Rob")
async def rob(ctx, m: discord.Member): eco=load("economy.json"); s=random.randint(50,200); eco[str(ctx.author.id)]=eco.get(str(ctx.author.id),0)+s
