# ISC ULTRA v100 - 100 SLASH + PREFIX - FINAL - CLEANED - V2 CHATBOT
import discord, asyncio, json, os, random, io, re
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

# ✅ YOUR MODEL - LOCKED
MODEL_NAME = "IndSnprKnfrClan"
MODEL_NO = "6A21ESW22"

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

# ========== V2 CHATBOT - KNOWS EVERYTHING ==========
def clean_text(text):
    text = re.sub(r'<@!?\d+>', '', text)
    text = re.sub(r'<#\d+>', '', text)
    text = re.sub(r'<@&\d+>', '', text)
    text = text.replace('@everyone', '').replace('@here', '')
    return text.strip()

def get_chat_reply_v2(display_name, message):
    msg_clean = clean_text(message)
    msg = msg_clean.lower()
    # ✅ MODEL NAME + NO.
    if "model" in msg or "model name" in msg or "model no" in msg:
        return f"Model Name: {MODEL_NAME}\nModel No.: {MODEL_NO}\nOwner: {display_name} — ISC OP! 🔥"
    if any(w in msg for w in ["hi","hey","hello","yo"]):
        return f"Yo {display_name}! ISC Sniper here! Ask me model, loadout, war, keys?"
    if "loadout" in msg or "sniper" in msg:
        return "Best Loadout: Sniper + Katana + Medkit + Smoke. Hold high ground, don't rush!"
    if "katana" in msg:
        return "Katana: Best mobility. Dash + slash. Combo: Katana dash -> Sniper shot. OP in 1v1!"
    if "keys" in msg:
        return "Keys: Daily Tasks + Contracts. Halloween event till Nov 6! Farm keys!"
    if "event" in msg:
        return "RIVALSWEEN event till Nov 6! Do contracts, farm keys, get Halloween skins!"
    if "gamemode" in msg or "mode" in msg:
        return "Today's rotating mode changes every 24h in Play page. Cycle: 1v1v1 -> Spleef -> Juggernaut -> Swift Standoff -> Bunny Sniping -> Tag Team -> Chicken Game -> RIVALS RNG -> Head Honcho -> Hardcore Parkour -> Double Trouble -> Mirror Matchup -> Limitless Loadout"
    if "war" in msg:
        return "ISC War: /createwar <enemy> to start, /joinwar to join, /warlist to see wars. ISC always wins!"
    if "rivals" in msg:
        return "RIVALS: Sniper + Katana OP! Hold high ground!"
    if "clan" in msg or "isc" in msg:
        return "ISC = Indian Sniper Clan. Best clan in RIVALS. Sniper + Katana OP!"
    if "rank" in msg:
        return "Ranked: 1v1, 2v2, 3v3. Win streak = more ELO. Don't tilt!"
    if "map" in msg:
        return "Best maps: Station, Docks, Big Arena for Sniper. Small maps: Shotgun + Katana."
    if "help" in msg:
        return "Mention me or use /chat <msg> or /helpisc for 100 commands!"
    if "bye" in msg or "gn" in msg:
        return f"GN {display_name}!"
    if "gm" in msg or "good morning" in msg:
        return f"GM {display_name}! Ready for grind?"
    if "how are you" in msg:
        return "I'm OP bro! Always online for ISC Clan 🔥"
    if "what is your name" in msg or "your name" in msg:
        return f"I'm ISC Bot - V2! Model Name: {MODEL_NAME} | Model No.: {MODEL_NO}"
    if not msg_clean:
        return f"Yo {display_name}!\nModel Name: {MODEL_NAME}\nModel No.: {MODEL_NO}"
    return f"Yo {display_name}!\nModel Name: {MODEL_NAME}\nModel No.: {MODEL_NO} — Ask me model, loadout, war, keys?"

# Keep old name for compatibility
def get_chat_reply(username, message):
    return get_chat_reply_v2(username, message)

@bot.event
async def on_ready():
    bot.add_view(TicketView()); bot.add_view(CloseView()); bot.add_view(VerifyView())
    # ✅ FORCE CLEAR old cached commands (fixes 'owner not found')
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
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
        clean = clean_text(message.content.replace(f'<@{bot.user.id}>','').replace(f'<@!{bot.user.id}>',''))
        await message.reply(get_chat_reply_v2(message.author.display_name, clean))
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
async def rob(ctx, m: discord.Member): eco=load("economy.json"); s=random.randint(50,200); eco[str(ctx.author.id)]=eco.get(str(ctx.author.id),0)+s; save("economy.json", eco); await ctx.send(f"Robbed ${s}")
@bot.hybrid_command(name="leaderboard", description="Leaderboard")
async def leaderboard(ctx): eco=load("economy.json"); top=sorted(eco.items(), key=lambda x:x[1], reverse=True)[:5]; await ctx.send(str(top))
@bot.hybrid_command(name="lb", description="LB")
async def lb(ctx): eco=load("economy.json"); top=sorted(eco.items(), key=lambda x:x[1], reverse=True)[:5]; await ctx.send(str(top))
@bot.hybrid_command(name="pay", description="Pay")
async def pay(ctx, m: discord.Member, amount: int): eco=load("economy.json"); eco[str(ctx.author.id)]-=amount; eco[str(m.id)]=eco.get(str(m.id),0)+amount; save("economy.json", eco); await ctx.send(f"Paid ${amount}")
@bot.hybrid_command(name="beg", description="Beg")
async def beg(ctx): e=random.randint(10,100); eco=load("economy.json"); eco[str(ctx.author.id)]=eco.get(str(ctx.author.id),0)+e; save("economy.json", eco); await ctx.send(f"+${e}")
@bot.hybrid_command(name="slots", description="Slots")
async def slots(ctx, bet: int=50): s=[random.choice(["A","B","C"]) for _ in range(3)]; await ctx.send(' '.join(s))
@bot.hybrid_command(name="shop", description="Shop")
async def shop(ctx): await ctx.send("Shop: Sniper $1000 ISC $500 VIP $5000")
@bot.hybrid_command(name="buy", description="Buy")
async def buy(ctx, *, item): await ctx.send(f"Bought {item}")
@bot.hybrid_command(name="inventory", description="Inv")
async def inventory(ctx): eco=load("economy.json"); await ctx.send(f"${eco.get(str(ctx.author.id),0)}")
@bot.hybrid_command(name="flip", description="Flip")
async def flip(ctx): await ctx.send(random.choice(["Heads","Tails"]))
@bot.hybrid_command(name="createwar", description="Create war")
async def createwar(ctx, *, enemy): wars=load("wars.json"); wars[enemy]={"players":[ctx.author.id]}; save("wars.json", wars); await ctx.send(f"War {enemy}")
@bot.hybrid_command(name="joinwar", description="Join war")
async def joinwar(ctx, *, enemy): wars=load("wars.json"); wars[enemy]["players"].append(ctx.author.id); save("wars.json", wars); await ctx.send(f"Joined {enemy}")
@bot.hybrid_command(name="warlist", description="War list")
async def warlist(ctx): wars=load("wars.json"); await ctx.send(str(list(wars.keys())))
@bot.hybrid_command(name="warinfo", description="War info")
async def warinfo(ctx, *, enemy): wars=load("wars.json"); await ctx.send(f"{enemy} players")
@bot.hybrid_command(name="endwar", description="End war")
async def endwar(ctx, *, enemy): wars=load("wars.json"); wars.pop(enemy,None); save("wars.json", wars); await ctx.send("Ended")
@bot.hybrid_command(name="declare", description="Declare")
async def declare(ctx, *, enemy): await ctx.send(f"War on {enemy}!")
@bot.hybrid_command(name="surrender", description="Surrender")
async def surrender(ctx, *, enemy): await ctx.send(f"Surrender {enemy}")
@bot.hybrid_command(name="roster", description="Roster")
async def roster(ctx): await ctx.send(str(load("wars.json")))
@bot.hybrid_command(name="rank", description="Rank")
async def rank(ctx): d=load("levels.json"); await ctx.send(f"Level {d.get(str(ctx.author.id),{}).get('level',1)}")
@bot.hybrid_command(name="level", description="Level")
async def level(ctx, m: discord.Member=None): m=m or ctx.author; d=load("levels.json"); await ctx.send(f"Level {d.get(str(m.id),{}).get('level',1)}")
@bot.hybrid_command(name="chat", description="Chat with V2 bot - knows everything")
async def chat(ctx, *, msg="hi"): await ctx.send(get_chat_reply_v2(ctx.author.display_name, msg))
@bot.hybrid_command(name="talk", description="Talk V2")
async def talk(ctx, *, msg="hi"): await ctx.send(get_chat_reply_v2(ctx.author.display_name, msg))
@bot.hybrid_command(name="iscchat", description="Chat help")
async def iscchat(ctx): await ctx.send("Mention me or use /chat /talk")
@bot.hybrid_command(name="rivals", description="Rivals")
async def rivals(ctx): await ctx.send("Sniper+Katana+Medkit+Smoke")
@bot.hybrid_command(name="event", description="Event")
async def event(ctx): await ctx.send("RIVALSWEEN till Nov 6")
@bot.hybrid_command(name="grind", description="Grind")
async def grind(ctx): await ctx.send("3 Contracts +5 Night")
@bot.hybrid_command(name="status", description="Status")
async def status(ctx): await ctx.send("ISC ULTRA v100 Online")
@bot.hybrid_command(name="avatar", description="Avatar")
async def avatar(ctx, m: discord.Member=None): m=m or ctx.author; await ctx.send(m.display_avatar.url)
@bot.hybrid_command(name="av", description="Av")
async def av(ctx, m: discord.Member=None): m=m or ctx.author; await ctx.send(m.display_avatar.url)
@bot.hybrid_command(name="say", description="Say")
async def say(ctx, *, t): await ctx.send(t)
@bot.hybrid_command(name="8ball", description="8ball")
async def _8ball(ctx, *, q): await ctx.send(random.choice(["Yes","No","ISC OP"]))
@bot.hybrid_command(name="serverinfo", description="Serverinfo")
async def serverinfo(ctx): await ctx.send(f"{ctx.guild.name} {ctx.guild.member_count}")
@bot.hybrid_command(name="si", description="SI")
async def si(ctx): await ctx.send(f"{ctx.guild.name}")
@bot.hybrid_command(name="poll", description="Poll")
async def poll(ctx, *, q): m=await ctx.send(f"Poll: {q}"); await m.add_reaction("✅"); await m.add_reaction("❌")
@bot.hybrid_command(name="giveaway", description="Giveaway")
async def giveaway(ctx, min: int, *, prize): m=await ctx.send(f"Giveaway {prize}"); await m.add_reaction("🎉")
@bot.hybrid_command(name="invites", description="Invites")
async def invites(ctx, m: discord.Member=None): m=m or ctx.author; await ctx.send(f"{m} invites")
@bot.hybrid_command(name="hug", description="Hug")
async def hug(ctx, m: discord.Member): await ctx.send(f"Hugged {m}")
@bot.hybrid_command(name="slap", description="Slap")
async def slap(ctx, m: discord.Member): await ctx.send(f"Slapped {m}")
@bot.hybrid_command(name="kiss", description="Kiss")
async def kiss(ctx, m: discord.Member): await ctx.send(f"Kissed {m}")
@bot.hybrid_command(name="roast", description="Roast")
async def roast(ctx, m: discord.Member=None): await ctx.send(f"{m.mention if m else 'You'} bot")
@bot.hybrid_command(name="joke", description="Joke")
async def joke(ctx): await ctx.send("ISC OP cause Sniper never misses!")
@bot.hybrid_command(name="meme", description="Meme")
async def meme(ctx): await ctx.send("Meme: ISC on top!")
@bot.hybrid_command(name="rps", description="RPS")
async def rps(ctx, choice): await ctx.send(f"You {choice} vs {random.choice(['rock','paper','scissors'])}")
@bot.hybrid_command(name="dice", description="Dice")
async def dice(ctx): await ctx.send(f"{random.randint(1,6)}")
@bot.hybrid_command(name="coinflip", description="Coinflip")
async def coinflip(ctx): await ctx.send(random.choice(["Heads","Tails"]))
@bot.hybrid_command(name="howgay", description="Howgay")
async def howgay(ctx, m: discord.Member=None): m=m or ctx.author; await ctx.send(f"{m} {random.randint(0,100)}% gay")
@bot.hybrid_command(name="howcool", description="Howcool")
async def howcool(ctx, m: discord.Member=None): m=m or ctx.author; await ctx.send(f"{m} {random.randint(0,100)}% cool")
@bot.hybrid_command(name="pp", description="PP")
async def pp(ctx, m: discord.Member=None): m=m or ctx.author; await ctx.send(f"8{'='*random.randint(0,10)}D")
@bot.hybrid_command(name="ship", description="Ship")
async def ship(ctx, m1: discord.Member, m2: discord.Member): await ctx.send(f"{m1.display_name}+{m2.display_name}={random.randint(0,100)}%")
@bot.hybrid_command(name="sniper", description="Sniper")
async def sniper(ctx): await ctx.send("Hold angle smoke katana")
@bot.hybrid_command(name="loadout", description="Loadout")
async def loadout(ctx): await ctx.send("Sniper Katana Medkit Smoke")
@bot.hybrid_command(name="tips", description="Tips")
async def tips(ctx): await ctx.send("High ground dont rush")
@bot.hybrid_command(name="clan", description="Clan")
async def clan(ctx): await ctx.send("ISC CLAN TOP!")
@bot.hybrid_command(name="isc", description="ISC")
async def isc(ctx): await ctx.send("ISC = Sniper Clan")
@bot.hybrid_command(name="model", description="Show Model Name and No.")
async def model_cmd(ctx): await ctx.send(f"Model Name: {MODEL_NAME}\nModel No.: {MODEL_NO}\nISC OP! 🔥")

# ✅ FIXED OWNER - Shows BOT owner, not server owner
@bot.hybrid_command(name="owner", description="Owner")
async def owner(ctx):
    try:
        user = await bot.fetch_user(OWNER_ID)
        await ctx.send(f"👑 ISC Bot Owner: {user.mention}")
    except:
        await ctx.send(f"👑 ISC Bot Owner ID: {OWNER_ID}")

@bot.hybrid_command(name="botinfo", description="Botinfo")
async def botinfo(ctx): await ctx.send(f"Ping {round(bot.latency*1000)}ms")
@bot.hybrid_command(name="ping", description="Ping")
async def ping(ctx): await ctx.send(f"Pong {round(bot.latency*1000)}ms")
@bot.hybrid_command(name="uptime", description="Uptime")
async def uptime(ctx): await ctx.send("Always online")
@bot.hybrid_command(name="invite", description="Invite")
async def invite(ctx): await ctx.send("discord.gg/isc")
@bot.hybrid_command(name="join", description="Join VC")
async def join(ctx): await ctx.send("Join VC")
@bot.hybrid_command(name="leave", description="Leave VC")
async def leave(ctx): await ctx.send("Leave VC")
@bot.hybrid_command(name="play", description="Play")
async def play(ctx, *, url): await ctx.send(f"Playing {url}")
@bot.hybrid_command(name="stop", description="Stop")
async def stop(ctx): await ctx.send("Stopped")
@bot.hybrid_command(name="queue", description="Queue")
async def queue(ctx): await ctx.send("Empty")
@bot.hybrid_command(name="ticketpanel", description="Ticket panel")
async def ticketpanel(ctx): await ctx.send(embed=discord.Embed(title="SUPPORT"), view=TicketView())
@bot.hybrid_command(name="verifypanel", description="Verify panel")
async def verifypanel(ctx): await ctx.send(embed=discord.Embed(title="Verify"), view=VerifyView())
@bot.hybrid_command(name="rules", description="Rules")
async def rules(ctx): await ctx.send("1.No spam 2.Respect 3.No NSFW 4.No links 5.ISC OP")
@bot.hybrid_command(name="helpisc", description="Help ISC 100 commands")
async def helpisc(ctx): await ctx.send("100 commands: kick ban timeout clear nuke warn warnings unwarn mute unmute lock unlock role removerole nick balance bal daily work rob leaderboard lb pay beg slots shop buy inventory flip createwar joinwar warlist warinfo endwar declare surrender roster rank level chat talk iscchat rivals event grind status avatar av say 8ball serverinfo si poll giveaway invites hug slap kiss roast joke meme rps dice coinflip howgay howcool pp ship sniper loadout tips clan isc model owner botinfo ping uptime invite join leave play stop queue ticketpanel verifypanel rules helpisc help")

# ✅ FIXED HELP - Only one help command now
@bot.hybrid_command(name="help", description="Help")
async def help_cmd(ctx):
    await ctx.send("Use /helpisc for 100 commands")

# ✅ FIXED TOKEN - Works with both DISCORD_TOKEN and TOKEN
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN")
bot.run(TOKEN)
