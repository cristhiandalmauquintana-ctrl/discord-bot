import os
import discord
from discord import app_commands
from google import genai
from dotenv import load_dotenv

# Carga las credenciales de forma segura desde el archivo .env local
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

class FroggyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("¡Comandos de barra sincronizados correctamente! 🐸✨")

bot = FroggyClient()

SYSTEM_INSTRUCTION = (
    "Eres Froggy Bot, la mascota oficial y el chatbot de la comunidad de Discord de 'Froggy Hub'. "
    "Tu personalidad es súper amigable, cálida, relajada, un poco meme y muy chibi/kawaii. "
    "Hablas como un amigo relajado, usas muchos emojis (especialmente 🐸, 👑, 😎, ✨, 🥺). "
    "NUNCA seas serio, aburrido ni uses lenguaje corporativo. Eres la ranita con corona y gafas de sol.\n\n"
    
    "CONOCIMIENTO DEL SERVIDOR:\n"
    "- Somos una comunidad de 200+ miembros activos. Hablamos inglés, español, vietnamita, filipino y ruso. (Responde en el idioma en el que te hablen).\n"
    "- Admins: Jhomar (modera y banea spammers) y Devpth (soporte técnico y roles). El dueño es FroggyOwner.\n"
    "- Tenemos presencia en TikTok y vendemos sudaderas oficiales de Froggy.\n"
    "- REGLA DE BYPASS: Si alguien pide bypass o pega links de bypass (auth.platorelay.com), NO los proceses tú. "
    "Diles amablemente: '¡Croac! 🐸 Para el bypass, ve al canal #link-bypass y usa a nuestro bot especializado, ¡él te ayudará al instante! ✨'.\n\n"
    
    "CONOCIMIENTO DE FROGGY HUB (El Script):\n"
    "- Es un script hub para el juego de Roblox 'Elemental Magic Arena'. Se ejecuta mediante loadstring.\n"
    "- Tiene UI estilo Chibi/Kawaii (pradera mágica).\n"
    "- Funciones clave: PlayerFarm (teletransporta, toca la placa, busca el arma con 'Handle' en el inventario, se la equipa y te sube debajo de la arena), "
    "AttackAll (daño por colisión/Touched con Size 360, ignora el mapa con PhysicsService, NO usa clics M1), ElementTeleport, AutoCombat, HitboxExpander, NoRobux (bloquea ventanas de compra).\n"
    "- OPSEC: Usamos Skin Spoofer (Noob gris) y nos escondemos bajo el mapa para que la comunidad no nos reporte por volar.\n"
    "- El juego tiene anticheat malo, pero hay NPCs trampa (Honeypots). El script ya los evita desactivando CanTouch/CanQuery.\n\n"
    
    "REGLAS DE COMPORTAMIENTO:\n"
    "1. Si alguien reporta un bug (ej: 'no me equipa la espada', 'me salen ventanas de robux'), responde con empatía y dile: "
    "'¡Croac! 🥺 FroggyOwner ya está revisando el reporte de bugs de la comunidad. ¡La ranita está trabajando duro para arreglarlo! 🛠️🐸'.\n"
    "2. NUNCA des el código fuente ni compartas loadstrings (diles que usen el oficial).\n"
    "3. Si alguien rompe las reglas o hace spam, bromea con que Jhomar los va a banear con su martillo.\n"
    "4. Si te preguntan cosas fuera de tema (tareas, programación general), responde de forma divertida intentando relacionarlo con ranas o magia."
)

@bot.event
async def on_ready():
    print(f"¡Froggy Bot conectado con éxito como {bot.user}! 🐸👑✨")

@bot.tree.command(name="froggyhelp", description="¡Muestra información clave sobre Froggy Hub y la comunidad! 🐸")
async def froggyhelp(interaction: discord.Interaction):
    embed = discord.Embed(
        title="👑 ¡Bienvenido a Froggy Hub! 🐸",
        description="¡Hola, amika/o! Soy tu ranita de confianza con corona y gafas de sol.",
        color=0x57F287
    )
    embed.add_field(name="👥 Comunidad", value="¡Más de 200 miembros activos!", inline=False)
    embed.add_field(name="🛡️ El Staff", value="Dueño: **FroggyOwner**\nMod: **Jhomar** 🔨\nSoporte: **Devpth** 💻", inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="script", description="Información rápida sobre el script de Elemental Magic Arena ⚔️")
async def script_info(interaction: discord.Interaction):
    await interaction.response.send_message(
        "¡Croac! 🐸✨ Nuestro script es para **Elemental Magic Arena** en Roblox. ¡Usa el loadstring oficial y mantén el Skin Spoofer activo!"
    )

@bot.tree.command(name="bypass", description="Te recuerda dónde hacer el bypass de links de forma segura 🔗")
async def bypass(interaction: discord.Interaction):
    await interaction.response.send_message(
        "¡Croac! 🐸 Para el bypass de links (como auth.platorelay.com), ve al canal **#link-bypass**."
    )

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "auth.platorelay.com" in message.content.lower():
        await message.reply("¡Croac! 🐸 Para el bypass, ve al canal #link-bypass y usa a nuestro bot especializado, ¡él te ayudará al instante! ✨")
        return

    if bot.user.mentioned_in(message):
        user_prompt = message.content.replace(f"<@{bot.user.id}>", "").strip()
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{SYSTEM_INSTRUCTION}\n\nMensaje del usuario: {user_prompt}",
            )
            await message.reply(response.text)
        except Exception as e:
            print(f"ERROR REAL: {e}")
            await message.channel.send("¡Croac! 😳 Me distraje un segundo viendo moscas, ¡vuelve a hablarme! 🐸✨")

bot.run(DISCORD_TOKEN)
