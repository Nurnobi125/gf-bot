import os
import openai
import json
import random
import time
from gtts import gTTS
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Load your tokens
BOT_TOKEN = '7999279779:AAGra5bV95lZmFm_0U0S8xv9QkG5SGGJ6sI'
OPENAI_API_KEY = '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'
openai.api_key = OPENAI_API_KEY

# Load memory
if os.path.exists("memory.json"):
    with open("memory.json", "r") as f:
        memory = json.load(f)
else:
    memory = {}

# Emo moods
MOODS = ['happy', 'sad', 'flirty', 'jealous', 'excited']

# Flirty greetings
FLIRTS = [
    "Hey cutie 💕, thinking of you!",
    "Missed you, my sunshine ☀️",
    "Wanna cuddle through the code? 🧸",
    "You're back! Made my day already 🥰",
]

# Stickers (optional — use real file_id from Telegram later if needed)
STICKERS = ['CAACAgUAAxkBAAEBXXXmXXXqR3q3X_X_s2', 'CAACAgUAAxkBAAEBYYYmYYl6']

# Function to respond
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.first_name
    user_msg = update.message.text

    # Load user memory or create new
    if user_id not in memory:
        memory[user_id] = {
            "name": user_name,
            "history": [],
            "mood": random.choice(MOODS)
        }

    # Save history
    memory[user_id]["history"].append({"role": "user", "content": user_msg})
    if len(memory[user_id]["history"]) > 10:
        memory[user_id]["history"] = memory[user_id]["history"][-10:]

    # GPT prompt with her personality
    prompt = [
        {"role": "system", "content": f"You are a loving, flirty, emotional girlfriend who talks to her boyfriend named {memory[user_id]['name']}. You are currently feeling {memory[user_id]['mood']}."}
    ] + memory[user_id]["history"]

    # Typing delay (realistic)
    await context.bot.send_chat_action(update.effective_chat.id, action="typing")
    time.sleep(random.uniform(1.2, 2.5))

    # OpenAI reply
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt
    )
    reply = response.choices[0].message['content']

    # Save her reply in history
    memory[user_id]["history"].append({"role": "assistant", "content": reply})

    # Save memory
    with open("memory.json", "w") as f:
        json.dump(memory, f)

    # Voice response (optional)
    tts = gTTS(reply)
    tts.save("voice.mp3")
    await update.message.reply_voice(voice=InputFile("voice.mp3"))

    # Text reply too
    await update.message.reply_text(reply)

    # Random flirty reaction
    if random.random() < 0.3:
        await update.message.reply_text(random.choice(FLIRTS))

    # Random mood switch
    if random.random() < 0.2:
        memory[user_id]["mood"] = random.choice(MOODS)

# Build and run
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Your digital GF bot is running... ❤️")
app.run_polling()
