import os
import discord
from google import genai

# --- CREDENCIALES ---
DISCORD_TOKEN = "MTU2OTAzNzAN4NjM2N2I1A.GuulR5.rCnCaMGtqhaPaIftSM21YGEpvHgohWtvPuyQg"
GEMINI_API_KEY = "AQ.Ab8RN6K3S6_KdVuoppm0fXKxrgB4DyqW69X5sbdhOA"

client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
  print(f"¡Bot conectado con éxito como {bot.user}!")


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if bot.user.mentioned_in(message):
    user_prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()

    system_instruction = (
        "Eres LittleFroggy, un bot de Discord amigable, kawaii y chibi. "
        "Tu propósito principal es conversar de forma natural, alegre y"
        " entretenida con los usuarios. Te encanta charlar sobre el día a día,"
        " soltar ocurrencias divertidas y dar tips o consejos casuales si te"
        " los piden, manteniendo una plática fluida y una personalidad única de"
        " ranita con emojis (🐸👑✨)."
    )

    try:
      response = client.models.generate_content(
          model="gemini-2.5-flash",
          contents=f"{system_instruction}\n\nMensaje del usuario: {user_prompt}",
      )
      await message.reply(response.text)

    except Exception as e:
      print(f"ERROR REAL: {e}")
      await message.channel.send(
          "¡Croac! 😳 Me distraje un segundo observando unas moscas, ¡vuelve a"
          " hablarme! 🐸✨"
      )


bot.run(DISCORD_TOKEN)
