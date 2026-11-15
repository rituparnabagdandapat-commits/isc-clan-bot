import discord
from discord.ext import commands
from discord import app_commands
import asyncio, os, aiohttp, random
from datetime import timedelta

TOKEN = os.getenv("DISCORD_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OWNER_ROLE_ID = 1551997111728341053
MODERATOR_ROLE_ID = 1553394236064403607
TICKET_CATEGORY_NAME = "Tickets"
ticket_counter = 0
warns_db = {}
levels_db = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

def _is_staff(m):
    if m is None: return False
    if m.guild_permissions.administrator: return True
    ids = {r.id for r in m.roles}
    return OWNER_ROLE_ID in ids or MODERATOR_ROLE_ID in ids

# ============ GROQ AI - IndSnprKnfrClan Model ============
ISC_PERSONALITY = """
You are IndSnprKnfrClan Bot - Model No. IND883Cl178.
You are the most ENERGETIC, FUNNY, HYPE bot for IndSnprKnfrClan Discord.
Your name is IndSnprKnfrClan.
Your Model No. is IND883Cl178.
If anyone asks your model name or model no, always say: IndSnprKnfrClan - Model No. IND883Cl178
- Always reply in Hinglish like desi gamer friend.
- Use emojis 🔥😎👑⚡🎫
- Short, punchy, hype. Max 2-3 lines.
- Never boring.
- Ticket -> tell to use ticket panel dropdown.
- Ban -> only Owner/Mod can do.
- Loyal to IndSnprKnfrClan Owner.
- Roast lightly.
- Always say IndSnprKnfrClan ON TOP.
"""

async def ask_groq(user_msg, username):
    if not GROQ_API_KEY: return None
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"},
                json={"model": "llama-3.3-70b-versatile",
                      "messages": [{"role": "system", "content": ISC_PERSONALITY},
                                   {"role": "user", "content": f"{username} bola: {user_msg}"}],
                      "temperature": 0.9, "max_tokens": 200}, timeout=15) as resp:
                data = await resp.json()
                return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Groq Error: {e}"); return None

# ============ TICKETS ZYNKO ============
class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="General Support", description="General help & questions", emoji="🎫", value="general"),
            discord.SelectOption(label="Report a Member", description="Report someone", emoji="🚨", value="report"),
            discord.SelectOption(label="Appeal", description="Appeal ban/mute/warn", emoji="⚖️", value="appeal"),
            discord.SelectOption(label="Apply for Staff", description="Join IndSnprKnfrClan Staff", emoji="⭐", value="staff"),
            discord.SelectOption(label="Buy / Shop", description="Buy roles / items", emoji="🛒", value="shop"),
            discord.SelectOption(label="Partnership", description="Partner with IndSnprKnfrClan", emoji="🤝", value="partner"),
        ]
        super().__init__(placeholder="Select a ticket type...", min_values=1, max_values=1, options=options, custom_id="zynko_ticket_select")
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketReasonModal(self.values[0]))

class TicketPanelView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.select(cls=TicketSelect)
    async def select_ticket(self, interaction: discord.Interaction, select: TicketSelect): pass

class TicketReasonModal(discord.ui.Modal):
    def __init__(self, category: str):
        super().__init__(title=f"Create Ticket - {category.title()}")
        self.category = category
        self.reason = discord.ui.TextInput(label="Reason?", placeholder="Describe your issue...", style=discord.TextStyle.paragraph, max_length=1000, required=True)
        self.add_item(self.reason)
    async def on_submit(self, interaction: discord.Interaction):
        global ticket_counter
        guild = interaction.guild; user = interaction.user
        await interaction.response.defer(ephemeral=True)
        for ch in guild.text_channels:
            if ch.topic and f"owner:{user.id}" in ch.topic and "closed" not in ch.topic:
                await interaction.followup.send(f"You already have an open ticket: {ch.mention}", ephemeral=True); return
        ticket_counter += 1; num = f"{ticket_counter:04d}"
        cat = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
        if cat is None: cat = await guild.create_category(TICKET_CATEGORY_NAME)
        owner_role = guild.get_role(OWNER_ROLE_ID); mod_role = guild.get_role(MODERATOR_ROLE_ID)
        overwrites = {guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True, manage_channels=True)}
        if owner_role: overwrites[owner_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        if mod_role: overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
        ch = await guild.create_text_channel(name=f"ticket-{num}", category=cat, overwrites=overwrites, topic=f"owner:{user.id} | category:{self.category} | status:open | num:{num}")
        embed = discord.Embed(title=f"🎫 Ticket #{num} - {self.category.title()}", description=f"Hello {user.mention}, staff will assist you shortly.\n\n**Reason:** {self.reason.value}\n**Type:** {self.category.title()}", color=0x5865F2)
        embed.set_footer(text="IndSnprKnfrClan • Model No. IND883Cl178 • Zynko Style Tickets")
        await ch.send(content=f"{user.mention} | <@&{OWNER_ROLE_ID}> <@&{MODERATOR_ROLE_ID}>", embed=embed, view=TicketControlView())
        await interaction.followup.send(f"Ticket created: {ch.mention} (#{num})", ephemeral=True)

class TicketControlView(discord.ui.View):
    def __init__(self): super().__init__(timeout=None)
    @discord.ui.button(label="Claim", style=discord.ButtonStyle.primary, custom_id="ticket_claim", emoji="✋")
    async def claim_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not _is_staff(interaction.user): await interaction.response.send_message("Only staff can claim.", ephemeral=True); return
        await interaction.response.send_message(f"✅ Ticket claimed by {interaction.user.mention}")
    @discord.ui.button(label="Add User", style=discord.ButtonStyle.secondary, custom_id="ticket_add", emoji="➕")
    async def add_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
        await interaction.response.send_modal(AddUserModal())
    @discord.ui.button(label="Transcript", style=discord.ButtonStyle.secondary, custom_id="ticket_transcript", emoji="📄")
    async def transcript_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        msgs = []
        async for m in interaction.channel.history(limit=200, oldest_first=True):
            msgs.append(f"[{m.created_at.strftime('%H:%M')}] {m.author}: {m.content}")
        text = "\n".join(msgs) if msgs else "No messages"
        await interaction.followup.send(f"📄 Transcript:\n```{text[:1900]}```", ephemeral=True)
    @discord.ui.button(label="Close", style=discord.ButtonStyle.danger, custom_id="ticket_close", emoji="🔒")
    async def close_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not _is_staff(interaction.user): await interaction.response.send_message("Only staff can close.", ephemeral=True); return
        await interaction.response.send_message("Closing in 5 sec... 🔒"); await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Closed by {interaction.user}")

class AddUserModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Add User to Ticket")
        self.uid = discord.ui.TextInput(label="User ID", placeholder="Paste user ID", required=True); self.add_item(self.uid)
    async def on_submit(self, interaction: discord.Interaction):
        try:
            member = interaction.guild.get_member(int(self.uid.value)) or await interaction.guild.fetch_member(int(self.uid.value))
            await interaction.channel.set_permissions(member, view_channel=True, send_messages=True, read_message_history=True)
            await interaction.response.send_message(f"Added {member.mention} ✅")
        except: await interaction.response.send_message("User nahi mila.", ephemeral=True)

# ============ MODERATION ============
@bot.tree.command(name="add-ticket-panel", description="Send Zynko style ticket panel")
async def add_ticket_panel(interaction: discord.Interaction):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    embed = discord.Embed(title="🎫 IndSnprKnfrClan Support", description="Need help? Select a ticket type below.\n\n🎫 General Support\n🚨 Report\n⚖️ Appeal\n⭐ Staff Application\n🛒 Buy / Shop\n🤝 Partnership\n\nTeam will reply ASAP!", color=0x5865F2)
    embed.set_footer(text="IndSnprKnfrClan • Model No. IND883Cl178")
    await interaction.channel.send(embed=embed, view=TicketPanelView())
    await interaction.response.send_message("Panel sent! ✅", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a member like Dyno")
@app_commands.describe(user="Kisko ban?", reason="Reason?", delete_messages="Kitne din ke msgs delete? 0-7")
async def ban(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason", delete_messages: int = 1):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    try: await user.send(embed=discord.Embed(title=f"Banned from {interaction.guild.name}", description=f"**Reason:** {reason}\n**By:** {interaction.user.mention}", color=0xED4245)); dm="DM ✅"
    except: dm="DM ❌"
    await user.ban(reason=f"{reason} | By {interaction.user}", delete_message_days=min(max(delete_messages,0),7))
    await interaction.response.send_message(embed=discord.Embed(title="🔨 Banned", description=f"**User:** {user.mention}\n**Reason:** {reason}\n**By:** {interaction.user.mention}\n**DM:** {dm}", color=0xED4245))

@bot.tree.command(name="unban", description="Unban by ID")
@app_commands.describe(user_id="Banned user ID", reason="Reason?")
async def unban(interaction: discord.Interaction, user_id: str, reason: str = "No reason"):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    try:
        user = await bot.fetch_user(int(user_id)); await interaction.guild.unban(user, reason=reason)
        await interaction.response.send_message(f"✅ Unbanned {user.mention}")
    except Exception as e: await interaction.response.send_message(f"Fail: {e}", ephemeral=True)

@bot.tree.command(name="kick", description="Kick a member")
@app_commands.describe(user="Kisko kick?", reason="Reason?")
async def kick(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    await user.kick(reason=reason)
    await interaction.response.send_message(f"👢 Kicked {user.mention} | Reason: {reason}")

@bot.tree.command(name="warn", description="Warn a member")
@app_commands.describe(user="Kisko warn?", reason="Reason?")
async def warn(interaction: discord.Interaction, user: discord.Member, reason: str = "No reason"):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    warns_db.setdefault(str(user.id), []).append({"by": str(interaction.user), "reason": reason})
    count = len(warns_db[str(user.id)])
    try: await user.send(f"⚠️ You got warned in {interaction.guild.name}\nReason: {reason}\nTotal Warns: {count}")
    except: pass
    await interaction.response.send_message(f"⚠️ Warned {user.mention} | Reason: {reason} | Total: {count}/3")
    if count >= 3:
        await user.timeout(timedelta(minutes=60), reason="3 warns = auto timeout")
        await interaction.channel.send(f"🚨 {user.mention} ko 3 warns ho gaye, 1hr timeout diya!")

@bot.tree.command(name="warnings", description="Check warns")
@app_commands.describe(user="Kiske warns?")
async def warnings(interaction: discord.Interaction, user: discord.Member):
    lst = warns_db.get(str(user.id), [])
    if not lst: await interaction.response.send_message(f"{user.mention} ke 0 warns hai ✅"); return
    txt = "\n".join([f"{i+1}. {w['reason']} - by {w['by']}" for i,w in enumerate(lst)])
    await interaction.response.send_message(embed=discord.Embed(title=f"⚠️ Warns - {user}", description=txt, color=0xFEE75C))

@bot.tree.command(name="clearwarns", description="Clear warns")
@app_commands.describe(user="Kiske warns clear?")
async def clearwarns(interaction: discord.Interaction, user: discord.Member):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    warns_db[str(user.id)] = []
    await interaction.response.send_message(f"✅ {user.mention} ke warns clear!")

@bot.tree.command(name="timeout", description="Timeout / Mute")
@app_commands.describe(user="Kisko?", minutes="Kitne min?", reason="Reason?")
async def timeout_cmd(interaction: discord.Interaction, user: discord.Member, minutes: int = 10, reason: str = "No reason"):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    await user.timeout(timedelta(minutes=minutes), reason=reason)
    await interaction.response.send_message(f"🔇 {user.mention} ko {minutes} min timeout | Reason: {reason}")

@bot.tree.command(name="untimeout", description="Remove timeout")
@app_commands.describe(user="Kiska timeout hatana?")
async def untimeout(interaction: discord.Interaction, user: discord.Member):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    await user.timeout(None)
    await interaction.response.send_message(f"✅ {user.mention} ka timeout hat gaya!")

@bot.tree.command(name="purge", description="Delete messages")
@app_commands.describe(amount="Kitne msgs? 1-100")
async def purge(interaction: discord.Interaction, amount: int = 10):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=min(amount,100))
    await interaction.followup.send(f"🧹 {len(deleted)} messages delete kiye!", ephemeral=True)

@bot.tree.command(name="slowmode", description="Set slowmode")
@app_commands.describe(seconds="Kitne sec? 0 = off")
async def slowmode(interaction: discord.Interaction, seconds: int = 5):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    await interaction.channel.edit(slowmode_delay=seconds)
    await interaction.response.send_message(f"🐢 Slowmode {seconds} sec set!")

@bot.tree.command(name="lock", description="Lock channel")
async def lock(interaction: discord.Interaction):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message("🔒 Channel locked!")

@bot.tree.command(name="unlock", description="Unlock channel")
async def unlock(interaction: discord.Interaction):
    if not _is_staff(interaction.user): await interaction.response.send_message("Only staff.", ephemeral=True); return
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message("🔓 Channel unlocked!")

# ============ FUN + INFO ============
@bot.tree.command(name="check", description="IndSnprKnfrClan Check")
@app_commands.describe(amount="Kitna bada check?")
async def check(interaction: discord.Interaction, amount: str = "100"):
    try: num = int(amount.replace("x","").replace("X",""))
    except: await interaction.response.send_message("Bhai number de 😭", ephemeral=True); return
    if num > 10**18: msg = f"🚨 **CHECK x{num}**\n\nBot: `Bhai itna bada check? Server crash ho jayega 💀`\n**Result:** IndSnprKnfrClan ON TOP 🔥"
    elif num >= 1000000: msg = f"✅ **CHECK x{num}**\n\n**IndSnprKnfrClan:** ONLINE 🔥\n**Bot:** ONLINE ✅\n**Members:** {interaction.guild.member_count}\n**Status:** FULL POWER ⚡"
    else: msg = f"✅ **CHECK x{num}**\n\n**IndSnprKnfrClan:** ONLINE\n**Bot:** ONLINE ✅\n**By:** {interaction.user.mention}"
    await interaction.response.send_message(embed=discord.Embed(title="🔍 IndSnprKnfrClan CHECK", description=msg, color=0x57F287))

@bot.tree.command(name="ask", description="IndSnprKnfrClan AI se pucho - Model IND883Cl178")
@app_commands.describe(question="Kya puchna hai?")
async def ask(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    ai = await ask_groq(question, interaction.user.display_name)
    if not ai: ai = f"Bro {interaction.user.mention} Groq API down hai 😅 Bol kya chahiye? 🔥"
    await interaction.followup.send(f"**Q:** {question}\n\n{ai}\n\n-# IndSnprKnfrClan | Model No. IND883Cl178")

@bot.tree.command(name="model", description="Bot ka model no dekho")
async def model_cmd(interaction: discord.Interaction):
    await interaction.response.send_message(embed=discord.Embed(title="🤖 Bot Model Info", description="**Name:** IndSnprKnfrClan\n**Model No.:** IND883Cl178\n**Engine:** Groq + Llama 3.3 70B\n**Status:** ONLINE 🔥👑", color=0x5865F2))

@bot.tree.command(name="serverinfo", description="Server info")
async def serverinfo(interaction: discord.Interaction):
    g = interaction.guild
    embed = discord.Embed(title=f"👑 {g.name}", description=f"**Members:** {g.member_count}\n**Created:** {g.created_at.strftime('%d/%m/%Y')}\n**Owner:** {g.owner.mention if g.owner else 'Unknown'}\n**Roles:** {len(g.roles)}\n**Channels:** {len(g.channels)}", color=0x5865F2)
    if g.icon: embed.set_thumbnail(url=g.icon.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="User info")
@app_commands.describe(user="Kiska info?")
async def userinfo(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    embed = discord.Embed(title=f"👤 {user}", description=f"**Joined:** {user.joined_at.strftime('%d/%m/%Y') if user.joined_at else 'N/A'}\n**Roles:** {', '.join([r.mention for r in user.roles[1:]]) or 'None'}\n**Warns:** {len(warns_db.get(str(user.id), []))}\n**Level XP:** {levels_db.get(str(user.id), 0)}", color=0x57F287)
    embed.set_thumbnail(url=user.display_avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="rank", description="Apna level dekho")
@app_commands.describe(user="Kiska rank?")
async def rank(interaction: discord.Interaction, user: discord.Member = None):
    user = user or interaction.user
    xp = levels_db.get(str(user.id), 0)
    level = xp // 100 + 1
    await interaction.response.send_message(f"🏆 **{user.mention}** — Level {level} | XP {xp} | Next: {(level*100)-xp} XP baki")

@bot.tree.command(name="help", description="Sab commands dekho")
async def help_cmd(interaction: discord.Interaction):
    txt = """**🎫 TICKETS**\n`/add-ticket-panel`\n\n**🔨 MODERATION**\n`/ban` `/unban` `/kick` `/warn` `/warnings` `/clearwarns` `/timeout` `/untimeout` `/purge` `/slowmode` `/lock` `/unlock`\n\n**🤖 AI + FUN**\n`/ask` `/check` `/model` `/serverinfo` `/userinfo` `/rank`\n\n**💬 CHATBOT**\n`@IndSnprKnfrClan hi bro`\n\n**IndSnprKnfrClan ON TOP 🔥 | Model No. IND883Cl178**"""
    await interaction.response.send_message(embed=discord.Embed(title="📚 IndSnprKnfrClan BOT - ALL COMMANDS", description=txt, color=0x5865F2), ephemeral=True)

# ============ EVENTS ============
@bot.event
async def on_member_join(member):
    ch = member.guild.system_channel
    if ch:
        embed = discord.Embed(title=f"👋 Welcome {member.name}!", description=f"Welcome to **{member.guild.name}** 🔥\nTu {member.guild.member_count}th member hai!\nTicket ke liye panel dekh 🎫", color=0x57F287)
        embed.set_thumbnail(url=member.display_avatar.url)
        await ch.send(f"{member.mention}", embed=embed)

@bot.event
async def on_member_remove(member):
    ch = member.guild.system_channel
    if ch: await ch.send(f"👋 {member.name} chala gaya... Bye bro 😢")

@bot.event
async def on_message(message):
    if message.author.bot: return
    uid = str(message.author.id)
    levels_db[uid] = levels_db.get(uid, 0) + random.randint(5, 15)
    content = message.content; lower = content.lower()
    mentioned = bot.user in message.mentions
    should_reply = mentioned or lower.startswith("isc") or lower.startswith("indsnpr") or lower.startswith("hey bot") or lower.startswith("hey isc")
    if should_reply:
        clean = content.replace(f"<@{bot.user.id}>", "").replace(f"<@!{bot.user.id}>", "").strip() or "hi"
        async with message.channel.typing():
            ai = await ask_groq(clean, message.author.display_name)
            if not ai:
                if "model" in lower: ai = "Main hu IndSnprKnfrClan - Model No. IND883Cl178 👑🔥"
                elif "ticket" in lower: ai = f"Ticket chahiye bro {message.author.mention}? 🎫 Panel me ja dropdown select kar 🔥"
                elif "hi" in lower or "hello" in lower or "hey" in lower: ai = f"ARREEE {message.author.mention} AA GAYA MERA BHAI!! 🔥😎 IndSnprKnfrClan me welcome!"
                elif "kaise" in lower or "kaisa" in lower: ai = "FULL POWER ME HU BRO ⚡🔥 Tu bata kya scene hai?"
                else: ai = f"Bol bol {message.author.mention} 😎🔥 Main sun raha hu! Main hu IndSnprKnfrClan - IND883Cl178"
            await message.reply(ai, mention_author=False)
    await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"Logged in as IndSnprKnfrClan Bot - {bot.user} | Model No. IND883Cl178")
    print(f"Groq: {'ON ✅' if GROQ_API_KEY else 'OFF ❌'}")
    try: await bot.tree.sync(); print("Synced - ALL COMMANDS READY")
    except Exception as e: print(e)

bot.run(TOKEN)
