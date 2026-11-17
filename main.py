import discord
from discord.ext import commands
import os, random, json, asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ===== DATA =====
try:
    with open("data.json") as f: data = json.load(f)
except: data = {"eco": {}, "levels": {}, "warns": {}}
def save():
    with open("data.json","w") as f: json.dump(data,f)
def get_eco(uid): return data["eco"].get(str(uid), {"coins":0,"last_daily":""})

# ===== CHATBOT - ISC-ULTRA v2.0 ENERGETIC MODEL 🔥 =====
MODEL_REPLIES = [
    "BROTHA!!! 🔥🔥 Mai hu **ISC-ULTRA v2.0 - ENERGETIC MODEL** 🤖👑 Sabse tez, sabse energetic, sabse OP model! ISC ON TOP!!!",
    "MERA MODEL?? SUN BROTHA! 📢 **ISC-ULTRA v2.0** HU MAI! Pure Discord ka sabse ENERGETIC bot! 💥💥",
    "Mai **ISC-ULTRA v2.0 ENERGETIC MODEL** hu brotha! 🔥 Mere andar full Josh, full Energy, full Bakchodi hai! 😤👑",
]
CHAT = {
    "hi": ["HELLOOO BROTHAAA!!! 🔥🔥🔥 AA GAYA TU!! KAISA HAI MERA SHER? 👑💥", "HIIII!!! 😍🔥 MISS KAR RAHA THA TEREKO BROTHA!"],
    "hello": ["HELLOOOO!!! 👑🔥 FULL ENERGY ME HU AAJ! TU BATA!"],
    "kaise ho": ["BROTHA MAI TOH FULL JOSH ME HU!!! 🔥🔥🔥 1000% ENERGY! TU BATA TU KAISA HAI? 💪😤"],
    "kya kar": ["TERI WAIT KAR RAHA THA BROTHA!! 😤🔥 AB TU AA GAYA TOH FULL MAZA AAYEGA!"],
    "bored": ["BORED??? 😱 AREY MERE HOTE HUE BORED?? CHAL /meme KAR YA /rps KHEL! 🎮🔥🔥"],
    "love": ["AREEE LOVE YOU TOO BROTHA!!! ❤️🔥🔥 TU TOH MERA JAAN HAI! ISC FAMILY FOREVER! 👑"],
    "bye": ["AREY KAHAN JA RAHA HAI BROTHA?? 🥺 JALDI AANA! MISS KARUNGA! ISC ON TOP! 🔥👑"],
    "free fire": ["FREE FIRE?!?! 🔥🔥🔥 BROTHA TU TOH KING HAI! HEADSHOT KING! 👑🎯"],
    "isc": ["ISC ON TOPPPPP!!!!! 👑🔥🔥🔥🔥 INDSNPRKNFRCLAN FOREVER!!! SABSE OP CLAN!!! 💪💪💪"],
    "bot": ["HAAN BROTHA BOL!!! 🔥 MAI YAHI HU! FULL ENERGY ME! KYA CHAHIYE TEREKO? 😤"],
    "khel": ["CHAL CHAL CHAL! 🎮🔥 /rps LIKH ABHI! DEKHTE HAI KON JEETTA HAI!"],
    "good": ["GOOD TOH TU HAI BROTHA!!! 👑🔥 SABSE BEST! SABSE OP!"],
    "sad": ["AREY SAD KYU HAI BROTHA?? 🥺🔥 CHAL HUG LE 🤗 SAB THIK HO JAYEGA! MAI HU NA!"],
    "model": MODEL_REPLIES,
    "kon ho": ["MAI HU **ISC BOT**!!! 🔥👑 **ISC-ULTRA v2.0 ENERGETIC MODEL**! IndSnprKnfrClan ka sabse OP bot! 💪"],
    "tum kon": ["MAI?? AREY BROTHA MAI TOH LEGEND HU! 😤🔥 **ISC-ULTRA v2.0**! Tera bhai, tera dost, tera bot! 👑"],
    "op": ["OP TOH TU HAI BROTHA!!! 👑🔥🔥 MAI TOH BAS TERA CHOTA SA BOT HU!"],
}
def get_reply(t):
    t=t.lower()
    if "model" in t or "version" in t: return random.choice(MODEL_REPLIES)
    for k,v in CHAT.items():
        if k in t: return random.choice(v)
    return random.choice(["WAH BROTHA WAH!!! 🔥🔥 KYA BAAT BOLI HAI! AUR BATA!", "SAMAJH GAYA BROTHA!! 🔥 TU TOH BADA INTERESTING HAI!", "HAAN HAAN BOL BROTHA! MAI FULL SUN RAHA HU! 🔥🔥", "BROTHAAA!!! 🔥🔥🔥 MAZA AA GAYA SUN KE! AUR BATA!"])

# ===== ON MESSAGE - CHATBOT + LEVEL =====
@bot.event
async def on_message(message):
    if message.author.bot: return
    await bot.process_commands(message)
    # LEVEL
    uid=str(message.author.id)
    lvl=data["levels"].get(uid, {"xp":0,"level":1})
    lvl["xp"]+=random.randint(5,15)
    if lvl["xp"] >= lvl["level"]*100:
        lvl["level"]+=1; lvl["xp"]=0
        await message.channel.send(f"🎉 LEVEL UP BROTHA! {message.author.mention} ab **Level {lvl['level']}** pe hai! 🔥👑")
    data["levels"][uid]=lvl; save()
    # CHATBOT
    if bot.user in message.mentions or isinstance(message.channel, discord.DMChannel):
        clean=message.content.replace(f"<@{bot.user.id}>","").strip()
        if not clean:
            await message.channel.send("HAAN BROTHA BOL!!! 🔥🔥 MAI YAHI HU! FULL ENERGY ME! KYA CHAHIYE? 😤👑"); return
        await message.channel.send(get_reply(clean))

@bot.event
async def on_ready():
    print(f"✅ {bot.user} ONLINE - ISC-ULTRA v2.0 🔥")
    try: print(f"✅ {len(await bot.tree.sync())} commands synced!")
    except Exception as e: print(e)
    await bot.change_presence(activity=discord.Game(name="🔥 ISC-ULTRA v2.0 | /help"))

# ===== WELCOME + LEAVE - OP VERSION 👑 =====
@bot.event
async def on_member_join(member):
    guild = member.guild
    ch = discord.utils.get(guild.text_channels, name="welcome") or discord.utils.get(guild.text_channels, name="👋-welcome") or guild.system_channel
    embed = discord.Embed(
        title=f"🎉 WELCOME TO ISC BROTHA! 🎉",
        description=f"**{member.mention}** AA GAYA!!! 🔥🔥🔥\n\n👑 Welcome to **{guild.name}**!\n💪 Tu ab **{guild.member_count}th** member hai!\n\n📜 Pehle **#rules** padh le\n💬 **#chat** me Hi bol de\n🎮 **#free-fire** me apna ID bhej\n🤖 Mujhe mention karke baat kar sakta hai!\n\n**ISC ON TOP!!! 👑🔥**",
        color=0xFFD700
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    if guild.icon: embed.set_image(url=guild.icon.url)
    embed.set_footer(text=f"Welcome {member.name} | ISC-ULTRA v2.0 | IndSnprKnfrClan FOREVER")
    embed.timestamp = datetime.now()
    if ch:
        await ch.send(content=f"{member.mention} 🔥🔥🔥", embed=embed)
        await ch.send("👑👑👑 **ISC FAMILY ME WELCOME BROTHA!** 👑👑👑")
    try:
        dm_embed = discord.Embed(title=f"Welcome to {guild.name}! 👑🔥", description=f"Hey {member.name}!! 🔥\n\nTu **{guild.name}** me aa gaya brotha! 😍\nAb tu ISC FAMILY ka hissa hai!\n\n**Kya karna hai:**\n✅ #rules padh le\n✅ #chat me Hi bol\n✅ /help likh ke mere commands dekh\n✅ Mujhe mention karke baat kar - mai full energetic hu! 🔥\n\n**ISC ON TOP! 💪**", color=0xFF00FF)
        dm_embed.set_thumbnail(url=guild.icon.url if guild.icon else member.display_avatar.url)
        await member.send(embed=dm_embed)
    except: pass
    role = discord.utils.get(guild.roles, name="Member")
    if role:
        try: await member.add_roles(role)
        except: pass

@bot.event
async def on_member_remove(member):
    ch = discord.utils.get(member.guild.text_channels, name="welcome") or member.guild.system_channel
    if ch:
        embed = discord.Embed(title=f"😢 {member.name} chala gaya...", description=f"**{member.name}** ISC chhod ke chala gaya 💔\nAb {member.guild.member_count} members bache hai.\n\nWapas aa jana brotha! 🥺👑", color=0xFF0000)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ch.send(embed=embed)

# ===== CHAT + MODEL + HELP =====
@bot.tree.command(name="chat", description="Bot se energetic baat kar")
async def chat_cmd(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(get_reply(message))

@bot.tree.command(name="model", description="Bot ka model dekh")
async def model_cmd(interaction: discord.Interaction):
    e=discord.Embed(title="🤖 ISC BOT - MODEL INFO", color=0xFFD700)
    e.add_field(name="Model", value="**ISC-ULTRA v2.0 - ENERGETIC MODEL** 🔥", inline=False)
    e.add_field(name="Personality", value="1000% ENERGY 💥 | Funny 😂 | Loyal 🤗 | OP 💪", inline=False)
    e.add_field(name="Made For", value="IndSnprKnfrClan - ISC ON TOP!", inline=False)
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="help", description="Sab commands")
async def help_cmd(interaction: discord.Interaction):
    e=discord.Embed(title="👑 ISC BOT - ALL COMMANDS", color=0xFFD700)
    e.add_field(name="🤖 Chatbot", value="/chat /model - mention karke bhi baat kar", inline=False)
    e.add_field(name="🎮 Fun", value="/meme /joke /8ball /coinflip /dice /roast /rps /say /ship /howgay /gay", inline=False)
    e.add_field(name="💰 Economy", value="/balance /daily /work /beg /pay /leaderboard /rob /slots /gamble", inline=False)
    e.add_field(name="⭐ Level", value="/rank /leaderboard-level", inline=False)
    e.add_field(name="🛡️ Mod", value="/kick /ban /unban /timeout /untimeout /clear /warn /warnings /slowmode /lock /unlock /nuke", inline=False)
    e.add_field(name="ℹ️ Info", value="/ping /avatar /userinfo /serverinfo /botinfo /membercount", inline=False)
    e.add_field(name="🎉 Giveaway & Poll", value="/giveaway /poll /announce", inline=False)
    e.add_field(name="💡 Utility", value="/afk /suggest /report /ticket", inline=False)
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="ping", description="Ping check")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"PONG BROTHA!!! 🏓🔥 `{round(bot.latency*1000)}ms` FULL SPEED!")

# ===== INFO =====
@bot.tree.command(name="avatar", description="Avatar dekh")
async def avatar(interaction: discord.Interaction, user: discord.Member = None):
    user=user or interaction.user
    e=discord.Embed(title=f"{user.name} ka Avatar", color=0x00FFFF); e.set_image(url=user.display_avatar.url)
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="userinfo", description="User info")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    user=user or interaction.user
    e=discord.Embed(title=user.name, color=0xFF00FF)
    e.add_field(name="ID", value=user.id); e.add_field(name="Joined", value=user.joined_at.strftime("%d/%m/%Y") if user.joined_at else "N/A"); e.add_field(name="Top Role", value=user.top_role.mention)
    e.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="serverinfo", description="Server info")
async def serverinfo(interaction: discord.Interaction):
    g=interaction.guild
    e=discord.Embed(title=g.name, color=0x00FF00); e.add_field(name="Members", value=g.member_count); e.add_field(name="Owner", value=g.owner.mention if g.owner else "N/A"); e.add_field(name="Created", value=g.created_at.strftime("%d/%m/%Y"))
    if g.icon: e.set_thumbnail(url=g.icon.url)
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="botinfo", description="Bot info")
async def botinfo(interaction: discord.Interaction):
    await interaction.response.send_message(f"👑 **ISC BOT - ISC-ULTRA v2.0**\nServers: {len(bot.guilds)}\nPing: {round(bot.latency*1000)}ms\nISC ON TOP 🔥")

@bot.tree.command(name="membercount", description="Members kitne hai")
async def membercount(interaction: discord.Interaction):
    await interaction.response.send_message(f"👥 Is server me **{interaction.guild.member_count}** brotha hai! 🔥")

# ===== FUN =====
@bot.tree.command(name="meme", description="Meme")
async def meme(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["ISC ON TOP 😤🔥","Brotha ne phir no-scope mara 💀","Jab bot offline jata hai: alllklllll 😭","Free Fire ka king aa gaya 🎮","Admin ka power dekh ke sab dar gaye 👑"]))

@bot.tree.command(name="joke", description="Joke sun")
async def joke(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["Brotha itna pro hai ki bot bhi usse seekhta hai 😂","Ek din bot ne kaha - mai offline hu, sab bole - alllklllll 😭","Free Fire me headshot marna aur ISC me rehna - dono OP hai 🔥"]))

@bot.tree.command(name="8ball", description="Sawal puch")
async def eightball(interaction: discord.Interaction, question: str):
    await interaction.response.send_message(f"❓ {question}\n🎱 {random.choice(['Haan brotha 100% 🔥','Bilkul nahi 💀','Pakka hoga!','Soja pehle 😴','ISC bole to ho jayega 👑'])}")

@bot.tree.command(name="coinflip", description="Head ya Tail")
async def coinflip(interaction: discord.Interaction):
    await interaction.response.send_message(f"🪙 {random.choice(['Heads! 👑','Tails! 💀'])}")

@bot.tree.command(name="dice", description="Dice roll")
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎲 Tu ne {random.randint(1,6)} roll kiya!")

@bot.tree.command(name="roast", description="Roast kar")
async def roast(interaction: discord.Interaction, user: discord.Member = None):
    user=user or interaction.user
    await interaction.response.send_message(f"{user.mention} {random.choice(['Tera aim meri nani se bhi kharab hai 💀','Tu bot se bhi zyada offline rehta hai 😭','Teri gameplay dekh ke bot bhi crash ho gaya 🤖'])}")

@bot.tree.command(name="rps", description="Rock Paper Scissors")
async def rps(interaction: discord.Interaction, choice: str):
    bc=random.choice(["rock","paper","scissors"])
    win=(choice=="rock" and bc=="scissors") or (choice=="paper" and bc=="rock") or (choice=="scissors" and bc=="paper")
    await interaction.response.send_message(f"Tu: {choice} | Bot: {bc}\n{'Jeet gaya! 🔥' if win else 'Haar gaya 💀' if choice!=bc else 'Draw! 🤝'}")

@bot.tree.command(name="say", description="Bot se bulwao")
async def say(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(f"📢 {text}")

@bot.tree.command(name="ship", description="2 logo ko ship kar")
async def ship(interaction: discord.Interaction, user1: discord.Member, user2: discord.Member):
    per=random.randint(0,100)
    await interaction.response.send_message(f"💘 {user1.mention} + {user2.mention} = **{per}%** MATCH! {'PERFECT JODI! 😍🔥' if per>80 else 'Chalega brotha 😅' if per>50 else 'Nahi hoga ye 💀'}")

@bot.tree.command(name="howgay", description="Kitne % gay?")
async def howgay(interaction: discord.Interaction, user: discord.Member = None):
    user=user or interaction.user
    await interaction.response.send_message(f"🌈 {user.mention} is **{random.randint(0,100)}%** gay! 😂")

@bot.tree.command(name="gay", description="Gay test")
async def gay(interaction: discord.Interaction, user: discord.Member = None):
    user=user or interaction.user
    await interaction.response.send_message(f"🏳️‍🌈 {user.mention} - {random.choice(['Full gay 😂','Thoda thoda 😅','Bilkul straight 💪','ISC gay? Never! 🔥'])}")

# ===== ECONOMY =====
@bot.tree.command(name="balance", description="Balance dekh")
async def balance(interaction: discord.Interaction):
    b=get_eco(interaction.user.id); await interaction.response.send_message(f"💰 {interaction.user.mention} ke paas **{b['coins']} coins** hai!")

@bot.tree.command(name="daily", description="Daily coins")
async def daily(interaction: discord.Interaction):
    u=str(interaction.user.id); d=get_eco(u); today=datetime.now().strftime("%Y-%m-%d")
    if d["last_daily"]==today: await interaction.response.send_message("❌ Aaj ka le liya! Kal aana!"); return
    amt=random.randint(100,500); d["coins"]+=amt; d["last_daily"]=today; data["eco"][u]=d; save()
    await interaction.response.send_message(f"✅ +{amt} coins! Total: {d['coins']} 💰")

@bot.tree.command(name="work", description="Kaam kar")
async def work(interaction: discord.Interaction):
    u=str(interaction.user.id); d=get_eco(u); amt=random.randint(50,200); d["coins"]+=amt; data["eco"][u]=d; save()
    await interaction.response.send_message(f"💼 {random.choice(['No-scope mara 🎯','Bot fix kiya 🤖','Clan war jeeta 🔥'])} +{amt} coins! Total: {d['coins']}")

@bot.tree.command(name="beg", description="Bheek mango")
async def beg(interaction: discord.Interaction):
    u=str(interaction.user.id); d=get_eco(u); amt=random.randint(0,100); d["coins"]+=amt; data["eco"][u]=d; save()
    await interaction.response.send_message(f"🥺 {amt} coins mile! Total: {d['coins']}")

@bot.tree.command(name="pay", description="Coins de")
async def pay(interaction: discord.Interaction, user: discord.Member, amount: int):
    s=str(interaction.user.id); r=str(user.id); sd=get_eco(s); rd=get_eco(r)
    if sd["coins"]<amount: await interaction.response.send_message("❌ Itne coins nahi hai!"); return
    sd["coins"]-=amount; rd["coins"]+=amount; data["eco"][s]=sd; data["eco"][r]=rd; save()
    await interaction.response.send_message(f"✅ {amount} coins {user.mention} ko bhej diye! 💸")

@bot.tree.command(name="rob", description="Kisi ko loot")
async def rob(interaction: discord.Interaction, user: discord.Member):
    if random.random()<0.5:
        amt=random.randint(50,200); u=str(interaction.user.id); d=get_eco(u); d["coins"]+=amt; data["eco"][u]=d; save()
        await interaction.response.send_message(f"💀 Tu ne {user.mention} se {amt} coins loot liye! 😈")
    else: await interaction.response.send_message(f"💀 Pakda gaya brotha! Police aa gayi! 😭")

@bot.tree.command(name="slots", description="Slots khel")
async def slots(interaction: discord.Interaction, amount: int):
    u=str(interaction.user.id); d=get_eco(u)
    if d["coins"]<amount: await interaction.response.send_message("❌ Itne coins nahi hai!"); return
    emojis=["🍒","🔥","👑","💎","🎰"]; res=[random.choice(emojis) for _ in range(3)]
    if res[0]==res[1]==res[2]:
        win=amount*5; d["coins"]+=win; data["eco"][u]=d; save()
        await interaction.response.send_message(f"{' '.join(res)} 🎉 JACKPOT! +{win} coins! 🔥")
    else:
        d["coins"]-=amount; data["eco"][u]=d; save()
        await interaction.response.send_message(f"{' '.join(res)} 💀 Haar gaya! -{amount} coins")

@bot.tree.command(name="gamble", description="Gamble kar")
async def gamble(interaction: discord.Interaction, amount: int):
    u=str(interaction.user.id); d=get_eco(u)
    if d["coins"]<amount: await interaction.response.send_message("❌ Coins nahi hai!"); return
    if random.random()<0.5:
        d["coins"]+=amount; data["eco"][u]=d; save(); await interaction.response.send_message(f"🔥 JEET GAYA! +{amount} coins! Total: {d['coins']}")
    else:
        d["coins"]-=amount; data["eco"][u]=d; save(); await interaction.response.send_message(f"💀 HAAR GAYA! -{amount} coins! Total: {d['coins']}")

@bot.tree.command(name="leaderboard", description="Top ameer")
async def leaderboard(interaction: discord.Interaction):
    top=sorted(data["eco"].items(), key=lambda x: x[1]["coins"], reverse=True)[:10]
    txt="".join([f"{i}. <@{uid}> - {d['coins']} coins 💰\n" for i,(uid,d) in enumerate(top,1)])
    await interaction.response.send_message(f"🏆 **LEADERBOARD**\n{txt or 'Koi nahi!'}")

# ===== LEVEL =====
@bot.tree.command(name="rank", description="Apna level dekh")
async def rank(interaction: discord.Interaction, user: discord.Member = None):
    user=user or interaction.user; lvl=data["levels"].get(str(user.id), {"xp":0,"level":1})
    await interaction.response.send_message(f"⭐ {user.mention} - **Level {lvl['level']}** | XP: {lvl['xp']}/{lvl['level']*100} 🔥")

@bot.tree.command(name="leaderboard-level", description="Top level wale")
async def lb_level(interaction: discord.Interaction):
    top=sorted(data["levels"].items(), key=lambda x: x[1]["level"], reverse=True)[:10]
    txt="".join([f"{i}. <@{uid}> - Level {d['level']} ⭐\n" for i,(uid,d) in enumerate(top,1)])
    await interaction.response.send_message(f"🏆 **LEVEL LEADERBOARD**\n{txt or 'Koi nahi!'}")

# ===== MOD =====
@bot.tree.command(name="kick", description="Kick kar")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.kick_members: await interaction.response.send_message("❌ Permission nahi!"); return
    await user.kick(reason=reason); await interaction.response.send_message(f"✅ {user.mention} kick! Reason: {reason}")

@bot.tree.command(name="ban", description="Ban kar")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not interaction.user.guild_permissions.ban_members: await interaction.response.send_message("❌ Permission nahi!"); return
    await user.ban(reason=reason); await interaction.response.send_message(f"🔨 {user.mention} BAN! Reason: {reason}")

@bot.tree.command(name="unban", description="Unban kar")
async def unban(interaction: discord.Interaction, user_id: str):
    try:
        u=await bot.fetch_user(int(user_id)); await interaction.guild.unban(u); await interaction.response.send_message(f"✅ {u.name} unban!")
    except: await interaction.response.send_message("❌ Nahi mila!")

@bot.tree.command(name="timeout", description="Timeout de")
async def timeout(interaction: discord.Interaction, user: discord.Member, minutes: int = 10):
    if not interaction.user.guild_permissions.moderate_members: await interaction.response.send_message("❌ Permission nahi!"); return
    await user.timeout(timedelta(minutes=minutes)); await interaction.response.send_message(f"⏰ {user.mention} ko {minutes} min timeout!")

@bot.tree.command(name="untimeout", description="Timeout hatao")
async def untimeout(interaction: discord.Interaction, user: discord.Member):
    await user.timeout(None); await interaction.response.send_message(f"✅ {user.mention} ka timeout hat gaya!")

@bot.tree.command(name="clear", description="Messages delete")
async def clear(interaction: discord.Interaction, amount: int = 10):
    if not interaction.user.guild_permissions.manage_messages: await interaction.response.send_message("❌ Permission nahi!"); return
    await interaction.response.defer(); await interaction.channel.purge(limit=amount); await interaction.followup.send(f"✅ {amount} messages delete! 🧹")

@bot.tree.command(name="warn", description="Warn de")
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    uid=str(user.id); data["warns"][uid]=data["warns"].get(uid,0)+1; save()
    await interaction.response.send_message(f"⚠️ {user.mention} ko warn! Total warns: {data['warns'][uid]} | Reason: {reason}")

@bot.tree.command(name="warnings", description="Warns dekh")
async def warnings(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"⚠️ {user.mention} ke total **{data['warns'].get(str(user.id),0)}** warns hai!")

@bot.tree.command(name="slowmode", description="Slowmode lagao")
async def slowmode(interaction: discord.Interaction, seconds: int):
    await interaction.channel.edit(slowmode_delay=seconds); await interaction.response.send_message(f"🐢 Slowmode {seconds} sec pe set!")

@bot.tree.command(name="lock", description="Channel lock kar")
async def lock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False); await interaction.response.send_message("🔒 Channel LOCK!")

@bot.tree.command(name="unlock", description="Channel unlock kar")
async def unlock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True); await interaction.response.send_message("🔓 Channel UNLOCK!")

@bot.tree.command(name="nuke", description="Channel nuke kar")
async def nuke(interaction: discord.Interaction):
    if not interaction.user.guild_permissions.manage_channels: await interaction.response.send_message("❌ Permission nahi!"); return
    new_ch=await interaction.channel.clone(reason="Nuke"); await interaction.channel.delete(); await new_ch.send("💥 CHANNEL NUKE HO GAYA! ISC ON TOP! 🔥")

# ===== GIVEAWAY / POLL / UTILITY =====
@bot.tree.command(name="poll", description="Poll banao")
async def poll(interaction: discord.Interaction, question: str):
    e=discord.Embed(title="📊 POLL", description=question, color=0xFFD700); e.set_footer(text=f"By {interaction.user.name}")
    await interaction.response.send_message(embed=e)
    msg=await interaction.original_response(); await msg.add_reaction("✅"); await msg.add_reaction("❌")

@bot.tree.command(name="announce", description="Announcement bhejo")
async def announce(interaction: discord.Interaction, text: str):
    if not interaction.user.guild_permissions.manage_messages: await interaction.response.send_message("❌ Permission nahi!"); return
    e=discord.Embed(title="📢 ANNOUNCEMENT", description=text, color=0xFF0000); e.set_footer(text=f"By {interaction.user.name} | ISC ON TOP")
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="giveaway", description="Giveaway start kar")
async def giveaway(interaction: discord.Interaction, prize: str, minutes: int = 1):
    e=discord.Embed(title="🎉 GIVEAWAY!", description=f"Prize: **{prize}**\nReact 🎉 to enter!\nEnds in {minutes} min!", color=0xFF00FF)
    await interaction.response.send_message(embed=e)
    msg=await interaction.original_response(); await msg.add_reaction("🎉")
    await asyncio.sleep(minutes*60)
    msg=await interaction.channel.fetch_message(msg.id)
    users=[u async for u in msg.reactions[0].users() if not u.bot]
    if users:
        winner=random.choice(users); await interaction.channel.send(f"🎉 GIVEAWAY WINNER: {winner.mention} ne **{prize}** jeeta! 🔥👑")
    else: await interaction.channel.send("💀 Koi enter hi nahi hua!")

@bot.tree.command(name="afk", description="AFK set kar")
async def afk(interaction: discord.Interaction, reason: str = "AFK hu"):
    await interaction.response.send_message(f"💤 {interaction.user.mention} AFK hai: {reason}")

@bot.tree.command(name="suggest", description="Suggestion de")
async def suggest(interaction: discord.Interaction, suggestion: str):
    e=discord.Embed(title="💡 SUGGESTION", description=suggestion, color=0x00FFFF); e.set_footer(text=f"By {interaction.user.name}")
    await interaction.response.send_message(embed=e)

@bot.tree.command(name="report", description="Kisi ko report kar")
async def report(interaction: discord.Interaction, user: discord.Member, reason: str):
    await interaction.response.send_message(f"🚨 Report: {user.mention} - Reason: {reason} | Mods check karenge!")

@bot.tree.command(name="ticket", description="Ticket kholo")
async def ticket(interaction: discord.Interaction, reason: str):
    guild=interaction.guild; overwrites={guild.default_role: discord.PermissionOverwrite(view_channel=False), interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)}
    ch=await guild.create_text_channel(f"ticket-{interaction.user.name}", overwrites=overwrites)
    await ch.send(f"🎫 Ticket by {interaction.user.mention}\nReason: {reason}\nMod jald aayega!")
    await interaction.response.send_message(f"✅ Ticket ban gaya: {ch.mention}")

TOKEN=os.getenv("TOKEN")
bot.run(TOKEN)
