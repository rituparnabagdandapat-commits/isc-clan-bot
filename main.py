import discord
import re
import json
import os
import random

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

MODEL_NAME = "IndSnprKnfrClan"
MODEL_NO = "6A21ESW22"

MODELS = {
    "indsnprknfrclan": f"{MODEL_NAME} - {MODEL_NO}",
    "v3": "ISC V3 - Smart + Chill",
    "funny": "Funny Mode 😂",
    "serious": "Serious Mode 🫡"
}

def load_model():
    if os.path.exists("isc_model.json"):
        try:
            with open("isc_model.json", "r") as f:
                data = json.load(f)
                if data.get("model") in MODELS:
                    return data["model"]
        except:
            pass
    return "indsnprknfrclan"

def save_model(m):
    with open("isc_model.json", "w") as f:
        json.dump({"model": m, "name": MODEL_NAME, "no": MODEL_NO}, f)

current_model = load_model()

@client.event
async def on_ready():
    print(f"✅ {MODEL_NAME} [{MODEL_NO}] online as {client.user}")

@client.event
async def on_message(message):
    global current_model
    try:
        if message.author.bot:
            return
        if not client.user.mentioned_in(message):
            return

        clean = re.sub(r"<@!?\d+>", "", message.content).strip()
        low = clean.lower()

        if not clean:
            await message.reply(f"Yo? 👀 I am **{MODEL_NAME} [{MODEL_NO}]**\nUse `@ISC help`")
            return

        args = clean.split()
        cmd = args[0].lower()

        # ========== COMMANDS - KEPT ==========
        if cmd == "model":
            if len(args) == 1:
                list_text = "\n".join([f"• `{k}` - {v}" for k, v in MODELS.items()])
                await message.reply(f"**Model Name:** {MODEL_NAME}\n**Model No.:** {MODEL_NO}\n**Current:** `{MODELS[current_model]}`\n\n**Available:**\n{list_text}\n\nUse: `@ISC model funny`")
                return
            wanted = args[1].lower()
            if wanted in MODELS:
                current_model = wanted
                save_model(wanted)
                await message.reply(f"✅ Model set to: **{MODELS[wanted]}**\nSaved forever ♾️")
            else:
                await message.reply(f"❌ No model `{wanted}`. Try `@ISC model`")
            return

        if cmd == "help":
            await message.reply(f"**🤖 {MODEL_NAME} [{MODEL_NO}]**\n\n**COMMANDS:**\n`@ISC model` - See models\n`@ISC model funny` - Change model\n`@ISC ping` - Check online\n`@ISC info` - Bot info\n`@ISC help` - This list\n\n**CHAT:**\nJust mention me like `@ISC hello` and I will reply!")
            return

        if cmd == "ping":
            await message.reply(f"Pong! 🏓 **{MODEL_NAME} [{MODEL_NO}]** Online ✅\nModel: `{current_model}`")
            return

        if cmd == "info":
            await message.reply(f"**Model Name:** {MODEL_NAME}\n**Model No.:** {MODEL_NO}\n**Current Model:** {MODELS[current_model]}\n**Owner:** {message.author.display_name}\n**Status:** Online ✅")
            return

        if cmd == "hello" or cmd == "hi" or cmd == "hey":
            await message.reply(f"Hey {message.author.display_name}! 👋 I am **{MODEL_NAME}** - What's up?")
            return
        # ========== END COMMANDS ==========

        # ========== CHATBOT - KEPT ==========
        funny_replies = [
            f"Haha real 😂 Tell me more, {message.author.display_name}",
            f"Brooo 😂😂 that was good, {message.author.display_name}",
            f"LMAO 🤣 You are funny {message.author.display_name}",
            f"No way 😂 Tell me more!"
        ]
        serious_replies = [
            f"Understood, {message.author.display_name}. How can I help you?",
            f"Noted. Please explain more, {message.author.display_name}.",
            f"Got it. What do you need, {message.author.display_name}?"
        ]
        normal_replies = [
            f"Real 💯 I am **{MODEL_NAME} [{MODEL_NO}]** - Tell me more {message.author.display_name}",
            f"Yeah I feel you {message.author.display_name}, continue 👀",
            f"Interesting... Tell me more {message.author.display_name} 👀",
            f"Real talk 💯 What's next, {message.author.display_name}?"
        ]

        if "how are you" in low or "how r u" in low:
            await message.reply(f"I'm good {message.author.display_name}! 🔥 You? I am **{MODEL_NAME} [{MODEL_NO}]**")
        elif "who are you" in low or "your name" in low:
            await message.reply(f"I am **{MODEL_NAME}** - Model No. **{MODEL_NO}** 🤖")
        elif "bye" in low:
            await message.reply(f"Bye bye {message.author.display_name} 👋 See you soon!")
        elif current_model == "funny":
            await message.reply(random.choice(funny_replies))
        elif current_model == "serious":
            await message.reply(random.choice(serious_replies))
        else:
            await message.reply(random.choice(normal_replies))
        # ========== END CHATBOT ==========

    except Exception as e:
        print(f"❌ ERROR: {e}")

client.run("YOUR_TOKEN_HERE")
