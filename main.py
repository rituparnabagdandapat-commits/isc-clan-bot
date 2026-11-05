import discord
import re
import json
import os

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

# INFINITE FIX: Load saved model, don't reset on restart
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
    print(f"✅ {MODEL_NAME} [{MODEL_NO}] online as {client.user} | Model: {current_model} | INFINITE READY")

@client.event
async def on_message(message):
    global current_model
    try:
        if message.author.bot:
            return
        if not client.user.mentioned_in(message):
            return

        clean = re.sub(r"<@!?\d+>", "", message.content).strip()
        if not clean:
            await message.reply(f"Yo? 👀 I am **{MODEL_NAME} [{MODEL_NO}]**\nUse `@ISC model`")
            return

        args = clean.split()

        if args[0].lower() == "model":
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

        if current_model == "funny":
            await message.reply(f"Haha real 😂 Tell me more, {message.author.display_name}")
        elif current_model == "serious":
            await message.reply(f"Understood. How can I help, {message.author.display_name}?")
        else:
            await message.reply(f"Real 💯 I am **{MODEL_NAME} [{MODEL_NO}]** - Tell me more {message.author.display_name}")

    except Exception as e:
        print(f"❌ ERROR: {e}")

client.run("YOUR_TOKEN_HERE")
