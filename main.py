import discord
from discord.ext import commands
from discord.ui import View, Button
import os, random, asyncio
from datetime import datetime, timedelta

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ========== VIEWS ==========
class VerifyView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="✅ Verify", style=discord.ButtonStyle.green, custom_id="v1")
    async def v(self, i, b):
        r = discord.utils.get(i.guild.roles, name="Verified") or await i.guild.create_role(name="Verified")
        await i.user.add_roles(r); await i.response.send_message("✅ Verified!", ephemeral=True)

class TicketView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="🎫 Create Ticket", style=discord.ButtonStyle.blurple, custom_id="t1")
    async def t(self, i, b):
        ow = {i.guild.default_role: discord.PermissionOverwrite(view_channel=False), i.user: discord.PermissionOverwrite(view_channel=True), i.guild.me: discord.PermissionOverwrite(view_channel=True)}
        ch = await i.guild.create_text_channel(f"ticket-{i.user.name}", overwrites=ow)
        await ch.send(f"{i.user.mention} Support here!", view=CloseView())
        await i.response.send_message(f"Ticket: {ch.mention}", ephemeral=True)

class CloseView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="🔒 Close", style=discord.ButtonStyle.red, custom_id="c1")
    async def c(self, i, b): await i.channel.delete()

@bot.event
async def setup_hook():
    bot.add_view(VerifyView()); bot.add_view(TicketView()); bot.add_view(CloseView())
    try: await bot.load_extension("extra")
    except: print("No extra.py - skipping")

@bot.event
async def on_ready():
    s = await bot.tree.sync()
    print(f"✅ Synced {len(s)} slash commands! - ISC ULTRA GOD {bot.user}")
    await bot.change_presence(activity=discord.Game(name=f"ISC | /help | {len(s)} cmds"))

# ========== HELP ==========
@bot.tree.command(name="help", description="Show all 50 commands")
async def help_c(i):
    e = discord.Embed(title="🔥 ISC ULTRA - 50 COMMANDS", color=0xFF0000)
    e.add_field(name="🛡️ Mod (13)", value="`/kick /ban /unban /timeout /untimeout /clear /nuke /lock /unlock /slowmode /warn /purgeuser /announce`", inline=False)
    e.add_field(name="ℹ️ Info (10)", value="`/ping /userinfo /serverinfo /avatar /botinfo /membercount /roleinfo /channelinfo /invite /uptime`", inline=False)
    e.add_field(name="🎫 Utility (7)", value="`/verify-panel /ticket-panel /poll /embed /say /dm /afk`", inline=False)
    e.add_field(name="😂 Fun (10)", value="`/8ball /coinflip /roll /rps /meme /joke /roast /howgay /pp /iq`", inline=False)
    e.add_field(name="💰 Economy Fun (10)", value="`/balance /work /daily /beg /slots /rob /leaderboard /give /ship /slap`", inline=False)
    await i.response.send_message(embed=e)

# ========== MODERATION 13 ==========
@bot.tree.command(name="kick", description="Kick member")
@discord.app_commands.checks.has_permissions(kick_members=True)
async def kick_c(i, member: discord.Member, reason: str="No reason"): await member.kick(reason=reason); await i.response.send_message(f"👢 Kicked {member}")

@bot.tree.command(name="ban", description="Ban member")
@discord.app_commands.checks.has_permissions(ban_members=True)
async def ban_c(i, member: discord.Member, reason: str="No reason"): await member.ban(reason=reason); await i.response.send_message(f"🔨 Banned {member}")

@bot.tree.command(name="unban", description="Unban by ID")
@discord.app_commands.checks.has_permissions(ban_members=True)
async def unban_c(i, user_id: str):
    u = await bot.fetch_user(int(user_id)); await i.guild.unban(u); await i.response.send_message(f"✅ Unbanned {u}")

@bot.tree.command(name="timeout", description="Timeout member")
@discord.app_commands.checks.has_permissions(moderate_members=True)
async def timeout_c(i, member: discord.Member, minutes: int): await member.timeout(discord.utils.utcnow()+timedelta(minutes=minutes)); await i.response.send_message(f"⏰ Timeout {member} {minutes}m")

@bot.tree.command(name="untimeout", description="Remove timeout")
@discord.app_commands.checks.has_permissions(moderate_members=True)
async def untimeout_c(i, member: discord.Member): await member.timeout(None); await i.response.send_message(f"✅ Untimeout {member}")

@bot.tree.command(name="clear", description="Clear messages")
@discord.app_commands.checks.has_permissions(manage_messages=True)
async def clear_c(i, amount: int): await i.response.defer(ephemeral=True); await i.channel.purge(limit=amount); await i.followup.send(f"🧹 Cleared {amount}", ephemeral=True)

@bot.tree.command(name="purgeuser", description="Purge messages from user")
@discord.app_commands.checks.has_permissions(manage_messages=True)
async def purgeuser_c(i, member: discord.Member, amount: int=10):
    def check(m): return m.author==member
    await i.response.defer(ephemeral=True); await i.channel.purge(limit=100, check=check); await i.followup.send(f"🧹 Purged {member}", ephemeral=True)

@bot.tree.command(name="nuke", description="Nuke channel")
@discord.app_commands.checks.has_permissions(manage_channels=True)
async def nuke_c(i): ch=i.channel; new=await ch.clone(); await ch.delete(); await new.send(f"💥 Nuked by {i.user.mention}")

@bot.tree.command(name="lock", description="Lock channel")
@discord.app_commands.checks.has_permissions(manage_channels=True)
async def lock_c(i): await i.channel.set_permissions(i.guild.default_role, send_messages=False); await i.response.send_message("🔒 Locked")

@bot.tree.command(name="unlock", description="Unlock channel")
@discord.app_commands.checks.has_permissions(manage_channels=True)
async def unlock_c(i): await i.channel.set_permissions(i.guild.default_role, send_messages=True); await i.response.send_message("🔓 Unlocked")

@bot.tree.command(name="slowmode", description="Set slowmode")
@discord.app_commands.checks.has_permissions(manage_channels=True)
async def slowmode_c(i, seconds: int): await i.channel.edit(slowmode_delay=seconds); await i.response.send_message(f"🐢 Slowmode {seconds}s")

@bot.tree.command(name="warn", description="Warn member")
@discord.app_commands.checks.has_permissions(kick_members=True)
async def warn_c(i, member: discord.Member, reason: str): await i.response.send_message(f"⚠️ {member.mention} warned: {reason}")

@bot.tree.command(name="announce", description="Announce")
@discord.app_commands.checks.has_permissions(administrator=True)
async def announce_c(i, title: str, message: str):
    e=discord.Embed(title=title, description=message, color=0xFF0000); await i.channel.send(embed=e); await i.response.send_message("✅ Sent", ephemeral=True)

# ========== INFO 10 ==========
@bot.tree.command(name="ping", description="Bot ping")
async def ping_c(i): await i.response.send_message(f"🏓 {round(bot.latency*1000)}ms")

@bot.tree.command(name="userinfo", description="User info")
async def userinfo_c(i, member: discord.Member=None):
    m=member or i.user; e=discord.Embed(title=str(m), color=m.color); e.set_thumbnail(url=m.display_avatar.url); e.add_field(name="ID", value=m.id); e.add_field(name="Joined", value=m.joined_at.strftime("%d/%m/%Y"))
    await i.response.send_message(embed=e)

@bot.tree.command(name="serverinfo", description="Server info")
async def serverinfo_c(i): g=i.guild; e=discord.Embed(title=g.name, color=0x00ff00); e.add_field(name="Members", value=g.member_count); e.add_field(name="Owner", value=str(g.owner)); await i.response.send_message(embed=e)

@bot.tree.command(name="avatar", description="Get avatar")
async def avatar_c(i, member: discord.Member=None): m=member or i.user; await i.response.send_message(m.display_avatar.url)

@bot.tree.command(name="botinfo", description="Bot info")
async def botinfo_c(i): await i.response.send_message(f"ISC ULTRA GOD | Servers: {len(bot.guilds)} | Ping: {round(bot.latency*1000)}ms | Commands: 50")

@bot.tree.command(name="membercount", description="Member count")
async def membercount_c(i): await i.response.send_message(f"👥 Members: {i.guild.member_count}")

@bot.tree.command(name="roleinfo", description="Role info")
async def roleinfo_c(i, role: discord.Role): await i.response.send_message(f"Role {role.mention} | Members: {len(role.members)} | Color: {role.color}")

@bot.tree.command(name="channelinfo", description="Channel info")
async def channelinfo_c(i): await i.response.send_message(f"Channel: {i.channel.mention} | ID: {i.channel.id} | Created: {i.channel.created_at.strftime('%d/%m/%Y')}")

@bot.tree.command(name="invite", description="Bot invite")
async def invite_c(i): await i.response.send_message(f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands")

@bot.tree.command(name="uptime", description="Bot uptime")
async def uptime_c(i): await i.response.send_message(f"✅ Online since <t:{int(discord.utils.utcnow().timestamp())}:R>")

# ========== UTILITY 7 ==========
@bot.tree.command(name="verify-panel", description="Verify panel")
@discord.app_commands.checks.has_permissions(administrator=True)
async def vp_c(i): e=discord.Embed(title="✅ Verify", description="Click to verify!", color=discord.Color.green()); await i.channel.send(embed=e, view=VerifyView()); await i.response.send_message("Sent!", ephemeral=True)

@bot.tree.command(name="ticket-panel", description="Ticket panel")
@discord.app_commands.checks.has_permissions(administrator=True)
async def tp_c(i): e=discord.Embed(title="🎫 Support", description="Click to open ticket!", color=discord.Color.blurple()); await i.channel.send(embed=e, view=TicketView()); await i.response.send_message("Sent!", ephemeral=True)

@bot.tree.command(name="poll", description="Create poll")
async def poll_c(i, question: str): e=discord.Embed(title="📊 Poll", description=question, color=0x00ff00); msg=await i.channel.send(embed=e); await msg.add_reaction("✅"); await msg.add_reaction("❌"); await i.response.send_message("Poll created!", ephemeral=True)

@bot.tree.command(name="embed", description="Make embed")
async def embed_c(i, title: str, description: str): e=discord.Embed(title=title, description=description, color=0xFF0000); await i.channel.send(embed=e); await i.response.send_message("Sent!", ephemeral=True)

@bot.tree.command(name="say", description="Say as bot")
async def say_c(i, message: str): await i.response.send_message("Sent!", ephemeral=True); await i.channel.send(message)

@bot.tree.command(name="dm", description="DM a user")
@discord.app_commands.checks.has_permissions(administrator=True)
async def dm_c(i, member: discord.Member, message: str):
    try: await member.send(message); await i.response.send_message(f"✅ DM sent to {member}", ephemeral=True)
    except: await i.response.send_message("❌ Can't DM", ephemeral=True)

@bot.tree.command(name="afk", description="Set AFK")
async def afk_c(i, reason: str="AFK"): await i.response.send_message(f"💤 {i.user.mention} is AFK: {reason}")

# ========== FUN 10 ==========
@bot.tree.command(name="8ball", description="Magic 8ball")
async def eight_c(i, question: str): await i.response.send_message(f"🎱 Q: {question}\nA: {random.choice(['Yes!', 'No!', 'Maybe', 'ISC says YES! 🔥', 'Never!'])}")

@bot.tree.command(name="coinflip", description="Flip coin")
async def cf_c(i): await i.response.send_message(random.choice(["Heads!", "Tails!"]))

@bot.tree.command(name="roll", description="Roll dice")
async def roll_c(i, max: int=100): await i.response.send_message(f"🎲 {random.randint(1,max)}")

@bot.tree.command(name="rps", description="Rock Paper Scissors")
async def rps_c(i, choice: str):
    bot_c=random.choice(["rock","paper","scissors"]); await i.response.send_message(f"You: {choice} | Bot: {bot_c} | {'You Win!' if (choice=='rock' and bot_c=='scissors') or (choice=='paper' and bot_c=='rock') or (choice=='scissors' and bot_c=='paper') else 'You Lose!' if choice!=bot_c else 'Draw!'}")

@bot.tree.command(name="meme", description="Random meme text")
async def meme_c(i): await i.response.send_message(random.choice(["POV: You are in ISC Clan 🔥", "When you get banned from ISC 😭", "ISC ULTRA GOD MODE ACTIVATED"]))

@bot.tree.command(name="joke", description="Random joke")
async def joke_c(i): await i.response.send_message(random.choice(["Why did the bot cross the road? To sync 50 commands! 😂", "ISC Clan > All"]))

@bot.tree.command(name="roast", description="Roast someone")
async def roast_c(i, member: discord.Member): await i.response.send_message(f"{member.mention} you fight like you code - badly 😭🔥 (jk)")

@bot.tree.command(name="howgay", description="How gay")
async def howgay_c(i, member: discord.Member=None): m=member or i.user; await i.response.send_message(f"🏳️‍🌈 {m.mention} is {random.randint(0,100)}% gay!")

@bot.tree.command(name="pp", description="PP size")
async def pp_c(i, member: discord.Member=None): m=member or i.user; await i.response.send_message(f"🍆 {m.mention}'s pp: 8{'='*random.randint(0,10)}D")

@bot.tree.command(name="iq", description="IQ test")
async def iq_c(i, member: discord.Member=None): m=member or i.user; await i.response.send_message(f"🧠 {m.mention} IQ: {random.randint(20,200)}")

# ========== ECONOMY FUN 10 ==========
@bot.tree.command(name="balance", description="Check balance")
async def bal_c(i): await i.response.send_message(f"💰 {i.user.mention} Balance: ${random.randint(0,10000)} (fake economy)")

@bot.tree.command(name="work", description="Work for money")
async def work_c(i): await i.response.send_message(f"💼 You worked and earned ${random.randint(100,1000)}!")

@bot.tree.command(name="daily", description="Daily reward")
async def daily_c(i): await i.response.send_message(f"🎁 Daily: ${random.randint(500,2000)} claimed!")

@bot.tree.command(name="beg", description="Beg for money")
async def beg_c(i): await i.response.send_message(random.choice([f"Someone gave you $10", "No one gave you anything lol", f"You got ${random.randint(1,100)}"]))

@bot.tree.command(name="slots", description="Slot machine")
async def slots_c(i): emojis=["🍒","🍋","💎","7️⃣","🍀"]; res=[random.choice(emojis) for _ in range(3)]; win="WIN" if res[0]==res[1]==res[2] else "LOSE"; await i.response.send_message(f"{' | '.join(res)} - {win}!")

@bot.tree.command(name="rob", description="Rob someone")
async def rob_c(i, member: discord.Member): await i.response.send_message(f"🦹 You robbed {member.mention} and got ${random.randint(0,500)}!")

@bot.tree.command(name="leaderboard", description="Top users")
async def lb_c(i): await i.response.send_message("🏆 Leaderboard (fake):\n1. ISC God - $10000\n2. You - $5000\n3. Bot - $0")

@bot.tree.command(name="give", description="Give money")
async def give_c(i, member: discord.Member, amount: int): await i.response.send_message(f"💸 {i.user.mention} gave ${amount} to {member.mention}!")

@bot.tree.command(name="ship", description="Ship 2 users")
async def ship_c(i, member1: discord.Member, member2: discord.Member): await i.response.send_message(f"💖 {member1.mention} + {member2.mention} = {random.randint(0,100)}% match!")

@bot.tree.command(name="slap", description="Slap someone")
async def slap_c(i, member: discord.Member): await i.response.send_message(f"👋 {i.user.mention} slapped {member.mention}!")

TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
bot.run(TOKEN)
