import os, random, datetime, re
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("TOKEN") or os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)
start_time = datetime.datetime.now(datetime.timezone.utc)
balances = {}
user_memory = {}
chat_history = {}

JOKES = ["Why did the chicken cross the road? To get to ISC! 🐔","Why do programmers prefer dark mode? Because light attracts bugs!","I told my computer I needed a break... now it sends me KitKats."]
FACTS = ["Honey never spoils.","Bananas are berries.","Octopuses have 3 hearts."]
QUOTES = ["Stay hungry, stay foolish. - Steve Jobs","Do it with passion or not at all.","ISC gang never sleeps."]
ROASTS = ["You're the reason the gene pool needs a lifeguard.","Your wifi is faster than your brain.","You bring everyone joy... when you leave."]
COMPLIMENTS = ["You're a legend bro 🔥","Your vibe is unmatched ✨","Main character energy!"]
MEMES = ["https://i.imgflip.com/4t0m5.jpg","https://i.imgflip.com/30b1gx.jpg","https://i.imgflip.com/1bij.jpg"]

def chatbot_v2_reply(user_id, username, text):
    text_low = text.lower()
    if user_id not in user_memory:
        user_memory[user_id] = {"name": username, "count": 0}
        chat_history[user_id] = []
    user_memory[user_id]["count"] += 1
    count = user_memory[user_id]["count"]
    if any(w in text_low for w in ["hello","hi","hey","yo","hola","namaste"]):
        return f"Yo {username}! 👋 Back again? ({count} times) I'm ISC V2. What's up?" if count > 1 else f"Yo {username}! 👋 First time talking? I'm ISC V2. What's up?"
    if "how are you" in text_low: return "I'm good bro! Running 24/7 😎 How are you?"
    if "your name" in text_low or "who are you" in text_low: return "I'm ISC Bot V2 🤖 Moderation + 51 Commands + Chatbot. Try `/help`"
    if "love you" in text_low: return f"Aww {username} ❤️ ISC loves you too!"
    if "crush" in text_low: return "Ooooh crush talk 👀 Tell me who? I won't tell... maybe 😏"
    if any(w in text_low for w in ["sad","depressed","lonely","cry","bored","tired"]): return f"Hey {username}, ISC got you 💛 Want a joke? Type `isc joke`"
    if "joke" in text_low: return random.choice(JOKES)
    if "meme" in text_low: return random.choice(MEMES)
    if "roast me" in text_low: return random.choice(ROASTS)
    if "fact" in text_low: return random.choice(FACTS)
    if "quote" in text_low: return random.choice(QUOTES)
    if "help" in text_low: return "Try `/help` for all 51 commands! Or just talk to me like this 🔥"
    if "bye" in text_low: return f"Bye {username}! Come back soon 👋"
    if "thank" in text_low: return f"Anytime {username}! 🙌"
    if "stupid" in text_low or "dumb" in text_low: return "Ouch 😢 I just got upgraded to V2 and you do me like this?"
    if "?" in text_low: return random.choice(["Hmm interesting 👀","I think yes... maybe? 😅","Bro that's a mystery even for V2 🤔"])
    return random.choice([f"Real 💯 Tell me more {username} 👀","Haha real 😂 What else?","ISC V2 listening... 👀","Broooo 👀 Continue..."])

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} - 51 + V2!")
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="51 Commands | isc hello"))

@bot.event
async def on_message(message):
    if message.author.bot: return
    content = message.content.strip()
    is_mention = bot.user in message.mentions
    is_isc_call = content.lower().startswith("isc")
    is_dm = isinstance(message.channel, discord.DMChannel)
    if is_mention or is_isc_call or is_dm:
        clean = re.sub(r'<@!?\d+>', '', content).strip()
        clean = re.sub(r'^(isc)\s*', '', clean, flags=re.I).strip()
        if clean == "": clean = "hello"
        await message.reply(chatbot_v2_reply(message.author.id, message.author.display_name, clean))
        return
    await bot.process_commands(message)

# --- 51 COMMANDS ---
@bot.tree.command(name="ping", description="Check ping")
async def ping(i: discord.Interaction): await i.response.send_message(f"🏓 Pong! {round(bot.latency*1000)}ms")
@bot.tree.command(name="chat", description="Chat with ISC V2")
@app_commands.describe(msg="Say something")
async def chat(i: discord.Interaction, msg: str): await i.response.send_message(chatbot_v2_reply(i.user.id, i.user.display_name, msg))
@bot.tree.command(name="hello", description="Say hello")
async def hello(i: discord.Interaction): await i.response.send_message(f"Hello {i.user.mention}! 👋 Welcome to ISC V2!")
@bot.tree.command(name="kick", description="Kick a member")
@app_commands.describe(member="Who", reason="Why")
@app_commands.default_permissions(kick_members=True)
async def kick(i: discord.Interaction, member: discord.Member, reason: str="No reason"):
    await member.kick(reason=reason); await i.response.send_message(f"👢 Kicked {member.mention} | {reason}")
@bot.tree.command(name="ban", description="Ban a member")
@app_commands.describe(member="Who", reason="Why")
@app_commands.default_permissions(ban_members=True)
async def ban(i: discord.Interaction, member: discord.Member, reason: str="No reason"):
    await member.ban(reason=reason); await i.response.send_message(f"🔨 Banned {member.mention} | {reason}")
@bot.tree.command(name="unban", description="Unban by ID")
@app_commands.describe(user_id="User ID")
@app_commands.default_permissions(ban_members=True)
async def unban(i: discord.Interaction, user_id: str):
    u = await bot.fetch_user(int(user_id)); await i.guild.unban(u); await i.response.send_message(f"✅ Unbanned {u.mention}")
@bot.tree.command(name="clear", description="Delete messages")
@app_commands.describe(amount="1-100")
@app_commands.default_permissions(manage_messages=True)
async def clear(i: discord.Interaction, amount: int):
    await i.response.defer(ephemeral=True); d = await i.channel.purge(limit=amount); await i.followup.send(f"🧹 Deleted {len(d)}!", ephemeral=True)
@bot.tree.command(name="timeout", description="Timeout member")
@app_commands.describe(member="Who", minutes="Minutes")
@app_commands.default_permissions(moderate_members=True)
async def timeout(i: discord.Interaction, member: discord.Member, minutes: int):
    await member.timeout(datetime.timedelta(minutes=minutes)); await i.response.send_message(f"⏰ Timed out {member.mention} for {minutes}m")
@bot.tree.command(name="untimeout", description="Remove timeout")
@app_commands.describe(member="Who")
@app_commands.default_permissions(moderate_members=True)
async def untimeout(i: discord.Interaction, member: discord.Member):
    await member.timeout(None); await i.response.send_message(f"✅ Untimed out {member.mention}")
@bot.tree.command(name="warn", description="Warn member")
@app_commands.describe(member="Who", reason="Why")
@app_commands.default_permissions(moderate_members=True)
async def warn(i: discord.Interaction, member: discord.Member, reason: str="No reason"): await i.response.send_message(f"⚠️ {member.mention} warned | {reason}")
@bot.tree.command(name="slowmode", description="Set slowmode")
@app_commands.describe(seconds="Seconds")
@app_commands.default_permissions(manage_channels=True)
async def slowmode(i: discord.Interaction, seconds: int):
    await i.channel.edit(slowmode_delay=seconds); await i.response.send_message(f"🐢 Slowmode {seconds}s")
@bot.tree.command(name="lock", description="Lock channel")
@app_commands.default_permissions(manage_channels=True)
async def lock(i: discord.Interaction):
    await i.channel.set_permissions(i.guild.default_role, send_messages=False); await i.response.send_message("🔒 Locked!")
@bot.tree.command(name="unlock", description="Unlock channel")
@app_commands.default_permissions(manage_channels=True)
async def unlock(i: discord.Interaction):
    await i.channel.set_permissions(i.guild.default_role, send_messages=True); await i.response.send_message("🔓 Unlocked!")
@bot.tree.command(name="nick", description="Change nickname")
@app_commands.describe(member="Who", nickname="New nick")
@app_commands.default_permissions(manage_nicknames=True)
async def nick(i: discord.Interaction, member: discord.Member, nickname: str):
    await member.edit(nick=nickname); await i.response.send_message(f"✏️ Changed nick to {nickname}")
@bot.tree.command(name="avatar", description="Show avatar")
@app_commands.describe(member="Who")
async def avatar(i: discord.Interaction, member: discord.Member = None):
    m = member or i.user; await i.response.send_message(m.display_avatar.url)
@bot.tree.command(name="userinfo", description="User info")
@app_commands.describe(member="Who")
async def userinfo(i: discord.Interaction, member: discord.Member = None):
    m = member or i.user; e = discord.Embed(title=m.display_name, color=0x00ff00); e.add_field(name="ID", value=m.id); e.set_thumbnail(url=m.display_avatar.url); await i.response.send_message(embed=e)
@bot.tree.command(name="serverinfo", description="Server info")
async def serverinfo(i: discord.Interaction): await i.response.send_message(f"🏰 **{i.guild.name}** | Members: {i.guild.member_count}")
@bot.tree.command(name="eightball", description="Magic 8ball")
@app_commands.describe(question="Ask")
async def eightball(i: discord.Interaction, question: str): await i.response.send_message(f"🎱 Q: {question}\nA: {random.choice(['Yes!','Nope','Maybe','Definitely!'])}")
@bot.tree.command(name="coinflip", description="Flip coin")
async def coinflip(i: discord.Interaction): await i.response.send_message(f"🪙 {random.choice(['Heads!','Tails!'])}")
@bot.tree.command(name="dice", description="Roll dice")
async def dice(i: discord.Interaction): await i.response.send_message(f"🎲 {random.randint(1,6)}")
@bot.tree.command(name="joke", description="Random joke")
async def joke(i: discord.Interaction): await i.response.send_message(random.choice(JOKES))
@bot.tree.command(name="meme", description="Random meme")
async def meme(i: discord.Interaction): await i.response.send_message(random.choice(MEMES))
@bot.tree.command(name="rps", description="Rock Paper Scissors")
@app_commands.describe(choice="rock/paper/scissors")
async def rps(i: discord.Interaction, choice: str):
    b=random.choice(["rock","paper","scissors"]); await i.response.send_message(f"You: {choice} | Bot: {b}")
@bot.tree.command(name="hug", description="Hug someone")
@app_commands.describe(member="Who")
async def hug(i: discord.Interaction, member: discord.Member): await i.response.send_message(f"🤗 {i.user.mention} hugged {member.mention}!")
@bot.tree.command(name="slap", description="Slap someone")
@app_commands.describe(member="Who")
async def slap(i: discord.Interaction, member: discord.Member): await i.response.send_message(f"👋 {i.user.mention} slapped {member.mention}!")
@bot.tree.command(name="kiss", description="Kiss someone")
@app_commands.describe(member="Who")
async def kiss(i: discord.Interaction, member: discord.Member): await i.response.send_message(f"😘 {i.user.mention} kissed {member.mention}!")
@bot.tree.command(name="pat", description="Pat someone")
@app_commands.describe(member="Who")
async def pat(i: discord.Interaction, member: discord.Member): await i.response.send_message(f"🐾 {i.user.mention} patted {member.mention}!")
@bot.tree.command(name="roast", description="Roast someone")
@app_commands.describe(member="Who")
async def roast(i: discord.Interaction, member: discord.Member): await i.response.send_message(f"{member.mention} {random.choice(ROASTS)}")
@bot.tree.command(name="compliment", description="Compliment someone")
@app_commands.describe(member="Who")
async def compliment(i: discord.Interaction, member: discord.Member): await i.response.send_message(f"{member.mention} {random.choice(COMPLIMENTS)}")
@bot.tree.command(name="quote", description="Random quote")
async def quote(i: discord.Interaction): await i.response.send_message(f"💬 {random.choice(QUOTES)}")
@bot.tree.command(name="fact", description="Random fact")
async def fact(i: discord.Interaction): await i.response.send_message(f"🧠 {random.choice(FACTS)}")
@bot.tree.command(name="poll", description="Make poll")
@app_commands.describe(question="Question")
async def poll(i: discord.Interaction, question: str): await i.response.send_message(f"📊 **POLL:** {question}\nReact ✅ or ❌")
@bot.tree.command(name="say", description="Make bot say")
@app_commands.describe(text="Text")
async def say(i: discord.Interaction, text: str): await i.response.send_message(text)
@bot.tree.command(name="embed", description="Make embed")
@app_commands.describe(title="Title", text="Text")
async def embed(i: discord.Interaction, title: str, text: str):
    e=discord.Embed(title=title, description=text, color=0x5865F2); await i.response.send_message(embed=e)
@bot.tree.command(name="invite", description="Get invite")
async def invite(i: discord.Interaction): await i.response.send_message(f"🔗 https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=8&scope=bot%20applications.commands")
@bot.tree.command(name="uptime", description="Uptime")
async def uptime(i: discord.Interaction):
    d=datetime.datetime.now(datetime.timezone.utc)-start_time; await i.response.send_message(f"⏱️ Uptime: {str(d).split('.')[0]}")
@bot.tree.command(name="botinfo", description="Bot info")
async def botinfo(i: discord.Interaction): await i.response.send_message(f"🤖 **ISC V2** | 51 Commands + Chatbot V2 | Servers: {len(bot.guilds)}")
@bot.tree.command(name="help", description="Show commands")
async def help_cmd(i: discord.Interaction): await i.response.send_message("**ISC V2 - 51 Commands:**\nMod: /kick /ban /unban /clear /timeout /untimeout /warn /slowmode /lock /unlock /nick\nFun: /8ball /coinflip /dice /joke /meme /rps /hug /slap /kiss /pat /roast /compliment /quote /fact /poll /say /embed\nUtil: /ping /chat /hello /avatar /userinfo /serverinfo /invite /uptime /botinfo /help /roll /choose /reverse /password /calculator /weather\nEconomy: /rank /daily /balance /work /rob /ship /love\nChatbot: `isc hello` or @ISC")
@bot.tree.command(name="roll", description="Roll 1-100")
async def roll(i: discord.Interaction): await i.response.send_message(f"🎲 {random.randint(1,100)}")
@bot.tree.command(name="choose", description="Choose")
@app_commands.describe(options="a,b,c")
async def choose(i: discord.Interaction, options: str): await i.response.send_message(f"🤔 I choose: **{random.choice(options.split(','))}**")
@bot.tree.command(name="reverse", description="Reverse text")
@app_commands.describe(text="Text")
async def reverse(i: discord.Interaction, text: str): await i.response.send_message(text[::-1])
@bot.tree.command(name="rank", description="Your rank")
async def rank(i: discord.Interaction):
    bal=balances.get(i.user.id,0); await i.response.send_message(f"🏆 {i.user.mention} | {bal} coins | Level: {bal//100+1}")
@bot.tree.command(name="daily", description="Daily coins")
async def daily(i: discord.Interaction):
    balances[i.user.id]=balances.get(i.user.id,0)+100; await i.response.send_message(f"💰 +100! Balance: {balances[i.user.id]}")
@bot.tree.command(name="balance", description="Balance")
@app_commands.describe(member="Who")
async def balance(i: discord.Interaction, member: discord.Member=None):
    m=member or i.user; await i.response.send_message(f"💰 {m.mention} Balance: {balances.get(m.id,0)}")
@bot.tree.command(name="work", description="Work for coins")
async def work(i: discord.Interaction):
    earn=random.randint(50,200); balances[i.user.id]=balances.get(i.user.id,0)+earn; await i.response.send_message(f"💼 +{earn} coins! Balance: {balances[i.user.id]}")
@bot.tree.command(name="rob", description="Rob someone")
@app_commands.describe(member="Who")
async def rob(i: discord.Interaction, member: discord.Member):
    if random.random()<0.5:
        amt=random.randint(10,100); balances[i.user.id]=balances.get(i.user.id,0)+amt; await i.response.send_message(f"🦹 Robbed {amt} from {member.mention}!")
    else: await i.response.send_message(f"🚔 Caught robbing {member.mention}!")
@bot.tree.command(name="ship", description="Ship two people")
@app_commands.describe(p1="Person 1", p2="Person 2")
async def ship(i: discord.Interaction, p1: discord.Member, p2: discord.Member):
    pct=random.randint(0,100); await i.response.send_message(f"💘 {p1.mention} ❤️ {p2.mention} = **{pct}%**")
@bot.tree.command(name="love", description="Love calc")
@app_commands.describe(member="Who")
async def love(i: discord.Interaction, member: discord.Member): await i.response.send_message(f"❤️ You + {member.mention} = **{random.randint(0,100)}%** love!")
@bot.tree.command(name="password", description="Gen password")
@app_commands.describe(length="Length")
async def password(i: discord.Interaction, length: int=12):
    chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%"; length=max(4,min(32,length)); await i.response.send_message(f"🔐 `{''.join(random.choice(chars) for _ in range(length))}`", ephemeral=True)
@bot.tree.command(name="calculator", description="Calculate")
@app_commands.describe(a="Num1", op=" + - * /", b="Num2")
async def calculator(i: discord.Interaction, a: float, op: str, b: float):
    res={"+":a+b,"-":a-b,"*":a*b,"/":a/b if b!=0 else "Can't divide by 0"}; await i.response.send_message(f"🧮 {a} {op} {b} = **{res.get(op,'Invalid')}**")
@bot.tree.command(name="weather", description="Fake weather")
@app_commands.describe(city="City")
async def weather(i: discord.Interaction, city: str): await i.response.send_message(f"🌤️ {city}: {random.randint(20,35)}°C, {random.choice(['Sunny ☀️','Cloudy ☁️','Rainy 🌧️'])}")

if __name__ == "__main__":
    bot.run(TOKEN)
