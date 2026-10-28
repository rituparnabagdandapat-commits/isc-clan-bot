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
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

# DB INIT
for f, d in [("levels.json", {}), ("economy.json", {}), ("wars.json", {}), ("invites.json", {})]:
    if not os.path.exists(f):
        with open(f, "w") as x: json.dump(d, x)

def load(f): 
    try:
        with open(f, "r") as x: return json.load(x)
    except: return {}
def save(f, d):
    with open(f, "w") as x: json.dump(d, x)

# --- VIEWS ---
class TicketView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="🎫 Create Ticket", style=discord.ButtonStyle.green, custom_id="ticket_v3")
    async def create(self, interaction, button):
        if discord.utils.get(interaction.guild.text_channels, name=f"ticket-{interaction.user.name.lower()}"):
            return await interaction.response.send_message("Ticket exists!", ephemeral=True)
        overwrites = {interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False), interaction.user: discord.PermissionOverwrite(view_channel=True), interaction.guild.me: discord.PermissionOverwrite(view_channel=True)}
        ch = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.name}", overwrites=overwrites)
        await ch.send(embed=discord.Embed(title="ISC SUPPORT", description=f"{interaction.user.mention} Support here!", color=0x00ff00), view=CloseView())
        await interaction.response.send_message(f"Created {ch.mention}", ephemeral=True)

class CloseView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="🔒 Close", style=discord.ButtonStyle.red, custom_id="close_v3")
    async def close(self, interaction, button):
        await interaction.response.send_message("Closing 3s..."); await asyncio.sleep(3); await interaction.channel.delete()

class VerifyView(View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="✅ Verify - Join ISC", style=discord.ButtonStyle.green, custom_id="verify_v3")
    async def verify(self, interaction, button):
        role = discord.utils.get(interaction.guild.roles, name="ISC Member")
        if not role:
            role = await interaction.guild.create_role(name="ISC Member", color=discord.Color.green())
        await interaction.user.add_roles(role)
        await interaction.response.send_message("✅ Verified! You are now ISC Member!", ephemeral=True)

# --- WELCOME IMAGE GENERATOR ---
async def make_welcome_image(member):
    try:
        img = Image.new('RGB', (1000, 300), color=(30, 30, 50))
        draw = ImageDraw.Draw(img)
        async with aiohttp.ClientSession() as session:
            async with session.get(member.display_avatar.url) as resp:
                data = await resp.read()
                avatar = Image.open(io.BytesIO(data)).resize((200,200))
                mask = Image.new('L', (200,200), 0); ImageDraw.Draw(mask).ellipse((0,0,200,200), fill=255)
                img.paste(avatar, (50,50), mask)
        draw.text((300, 50), f"WELCOME TO ISC CLAN", fill=(255,255,255), font=ImageFont.load_default())
        draw.text((300, 120), f"{member.name}", fill=(0,255,0), font=ImageFont.load_default())
        draw.text((300, 180), f"Member #{member.guild.member_count}", fill=(200,200,200), font=ImageFont.load_default())
        buf = io.BytesIO(); img.save(buf, format='PNG'); buf.seek(0)
        return buf
    except Exception as e:
        print(f"Welcome img error: {e}")
        return None

@bot.event
async def setup_hook():
    await bot.load_extension("extra")

@bot.event
async def on_ready():
    bot.add_view(TicketView()); bot.add_view(CloseView()); bot.add_view(VerifyView())
    try:
        synced = await bot.tree.sync()
        print(f"🔥 ISC ULTRA GOD MODE {bot.user} - Synced {len(synced)} commands!")
    except Exception as e:
        print(f"Failed to sync: {e}")

@bot.event
async def on_member_join(member):
    ch = discord.utils.get(member.guild.text_channels, name="welcome") or member.guild.system_channel
    if ch:
        buf = await make_welcome_image(member)
        if buf:
            file = discord.File(buf, filename="welcome.png")
            embed = discord.Embed(title=f"Welcome {member.name}!", color=0x5865F2)
            embed.set_image(url="attachment://welcome.png")
            await ch.send(embed=embed, file=file, view=VerifyView())
        else:
            await ch.send(f"Welcome {member.mention} to ISC Clan! #{member.guild.member_count}", view=VerifyView())
    invites = await member.guild.invites()
    for inv in invites:
        if inv.uses > load("invites.json").get(str(inv.code), 0):
            data = load("invites.json"); data[str(inv.code)] = inv.uses; data[f"inviter_{member.id}"] = inv.inviter.id; save("invites.json", data)
            break

@bot.event
async def on_message(message):
    if message.author.bot: return
    if not message.author.guild_permissions.manage_messages:
        if "discord.gg" in message.content or "http://" in message.content and "tenor" not in message.content:
            await message.delete()
            return await message.channel.send(f"{message.author.mention} No links!", delete_after=5)
    data = load("levels.json"); uid=str(message.author.id)
    if uid not in data: data[uid]={"xp":0,"level":1}
    data[uid]["xp"]+=random.randint(5,15)
    if data[uid]["xp"] >= data[uid]["level"]*100:
        data[uid]["level"]+=1; await message.channel.send(f"GG {message.author.mention} Level {data[uid]['level']}!")
    save("levels.json", data)
    if bot.user in message.mentions:
        replies = ["ISC Clan OP 🔥", f"Yo {message.author.name} what up?", "Need help? Create ticket!", "ISC on top!", "War time? !createwar"]
        await message.reply(random.choice(replies))
    await bot.process_commands(message)

# --- MOD ULTRA ---
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, m: discord.Member, *, r="No reason"): await m.kick(reason=r); await ctx.send(f"Kicked {m}")
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, m: discord.Member, *, r="No reason"): await m.ban(reason=r); await ctx.send(f"Banned {m}")
@bot.command()
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, m: discord.Member, min: int=10): await m.timeout(discord.utils.utcnow()+timedelta(minutes=min)); await ctx.send(f"Timeout {m} {min}m")
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, a: int=10): await ctx.channel.purge(limit=a+1)
@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx): await ctx.channel.clone(); await ctx.channel.delete()

# --- ECONOMY ---
@bot.command()
async def balance(ctx): eco=load("economy.json"); await ctx.send(f"💰 {ctx.author.mention} ${eco.get(str(ctx.author.id),0)}")
@bot.command()
async def daily(ctx): eco=load("economy.json"); eco[str(ctx.author.id)]=eco.get(str(ctx.author.id),0)+500; save("economy.json", eco); await ctx.send(f"Daily $500 claimed! Bal: ${eco[str(ctx.author.id)]}")
@bot.command()
async def work(ctx): earn=random.randint(100,400); eco=load("economy.json"); eco[str(ctx.author.id)]=eco.get(str(ctx.author.id),0)+earn; save("economy.json", eco); await ctx.send(f"Worked +${earn}")
@bot.command()
async def rob(ctx, m: discord.Member): eco=load("economy.json"); stolen=random.randint(50,200); eco[str(ctx.author.id)]=eco.get(str(ctx.author.id),0)+stolen; eco[str(m.id)]=eco.get(str(m.id),0)-stolen; save("economy.json", eco); await ctx.send(f"Robbed ${stolen} from {m}")
@bot.command()
async def leaderboard(ctx): eco=load("economy.json"); top=sorted(eco.items(), key=lambda x:x[1], reverse=True)[:10]; desc="\n".join([f"<@{uid}> ${b}" for uid,b in top]); await ctx.send(embed=discord.Embed(title="Richest ISC", description=desc, color=0xFFD700))

# --- CLAN WAR ---
@bot.command()
async def createwar(ctx, *, enemy): wars=load("wars.json"); wars[enemy]={"players":[ctx.author.id]}; save("wars.json", wars); await ctx.send(f"⚔️ War vs {enemy} created! !joinwar {enemy}")
@bot.command()
async def joinwar(ctx, *, enemy): wars=load("wars.json"); wars[enemy]["players"].append(ctx.author.id); save("wars.json", wars); await ctx.send(f"{ctx.author.mention} joined war vs {enemy}")
@bot.command()
async def warlist(ctx): wars=load("wars.json"); await ctx.send(f"Wars: {', '.join(wars.keys()) or 'None'}")

# --- MUSIC ---
@bot.command()
async def join(ctx): 
    if ctx.author.voice: await ctx.author.voice.channel.connect()
    else: await ctx.send("Join VC first!")
@bot.command()
async def leave(ctx): 
    if ctx.voice_client: await ctx.voice_client.disconnect()
@bot.command()
async def play(ctx, *, url):
    await ctx.send(f"🎵 Playing: {url} (Add ffmpeg in bothosting if not working)")

# --- FUN + UTILITY ---
@bot.command()
async def avatar(ctx, m: discord.Member=None): m=m or ctx.author; await ctx.send(m.display_avatar.url)
@bot.command()
async def say(ctx, *, t): await ctx.message.delete(); await ctx.send(t)
@bot.command()
async def _8ball(ctx, *, q): await ctx.send(random.choice(["Yes","No","ISC OP","Maybe","Definitely"]))
@bot.command()
async def serverinfo(ctx): g=ctx.guild; await ctx.send(embed=discord.Embed(title=g.name, description=f"Members: {g.member_count}", color=0x5865F2))
@bot.command()
async def poll(ctx, *, q): m=await ctx.send(embed=discord.Embed(title="📊 Poll", description=q)); await m.add_reaction("✅"); await m.add_reaction("❌")
@bot.command()
async def giveaway(ctx, min: int, *, prize):
    msg=await ctx.send(embed=discord.Embed(title="🎉 GIVEAWAY", description=f"{prize}\nReact 🎉", color=0xFF69B4)); await msg.add_reaction("🎉")
    await asyncio.sleep(min*60)
    new=await ctx.channel.fetch_message(msg.id); users=[u async for u in new.reactions[0].users() if not u.bot]
    if users: await ctx.send(f"Winner {prize}: {random.choice(users).mention}")
@bot.command()
async def invites(ctx, m: discord.Member=None):
    m=m or ctx.author; total=sum(1 for k,v in load("invites.json").items() if k.startswith("inviter_") and v==m.id); await ctx.send(f"{m.mention} invited {total} members")

@bot.command()
@commands.has_permissions(administrator=True)
async def ticketpanel(ctx): await ctx.send(embed=discord.Embed(title="🎫 ISC SUPPORT", description="Click to create ticket!", color=0x5865F2), view=TicketView())
@bot.command()
@commands.has_permissions(administrator=True)
async def verifypanel(ctx): await ctx.send(embed=discord.Embed(title="Verify", description="Click to join ISC Clan", color=0x00FF00), view=VerifyView())
@bot.command()
@commands.has_permissions(administrator=True)
async def rules(ctx): await ctx.send(embed=discord.Embed(title="📜 ISC Rules", description="1. No spam\n2. Respect\n3. No NSFW\n4. No links\n5. ISC OP", color=0xFF0000))

@bot.command()
async def helpisc(ctx):
    embed = discord.Embed(
        title="🔥 ISC ULTRA - COMMAND CENTER",
        description="Prefix: `!` | Mention bot for AI chat",
        color=0x00ff88
    )
    embed.add_field(name="🛡️ MOD GOD", value="`!kick` `!ban` `!timeout` `!clear` `!nuke`", inline=False)
    embed.add_field(name="💰 ECONOMY", value="`!balance` `!daily` `!work` `!rob` `!leaderboard`", inline=False)
    embed.add_field(name="⚔️ CLAN WAR", value="`!createwar` `!joinwar` `!warlist`", inline=False)
    embed.add_field(name="🎵 VC & FUN", value="`!join` `!leave` `!play` `!avatar` `!8ball` `!poll` `!giveaway` `!invites`", inline=False)
    embed.add_field(name="🎫 PANELS", value="`!ticketpanel` `!verifypanel` `!rules` `!serverinfo` `!say`", inline=False)
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.set_footer(text="ISC Clan OP 🔥")
    await ctx.send(embed=embed)

@bot.command(name="help")
async def help_cmd(ctx):
    await helpisc(ctx)

bot.run(os.getenv("DISCORD_TOKEN"))
