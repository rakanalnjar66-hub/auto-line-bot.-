import os
import asyncio
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# 1. خادم الويب لإبقاء البوت شغال في Render
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"977 Auto-Line Bot is Alive!")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

Thread(target=run_server, daemon=True).start()

# 2. إعدادات البوت
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قائمة الرومات المحددة (18 روم)
TARGET_CHANNELS = [
    1540429474405818468,
    1540429517506478090,
    1540429563660599356,
    1540429583902580826,
    1540429188077453433,
    1540429149284606092,
    1540429233409630258,
    1540429110680092772,
    1540428845193101503,
    1540428777362956308,
    1540428366069629100,
    1538886597158772847,
    1538886660492755035,
    1539450874785693716,
    1538886761990594650,
    1538886721272549446,
    1538886981692424253,
    1538886884082589787
]

# رابط صورة الخط الفاصل
LINE_IMAGE_URL = "https://cdn.discordapp.com/attachments/1539654724880433153/1540826636310814810/Gemini_Generated_Image_2wgatm2wgatm2wga.jfif?ex=6a8b5e21&is=6a8a0ca1&hm=21d267730f0ba96cc418f1324643c31fdb33c399cb5a7fb2c22d48807e3ae638&"

@bot.event
async def on_ready():
    print(f"تم تشغيل بوت الخط الفاصل بنجاح باسم: {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id in TARGET_CHANNELS:
        await message.channel.send(LINE_IMAGE_URL)

    await bot.process_commands(message)

# التوكين
BOT_TOKEN = "MTU0MDgyODcxNzAyMDg4MDkwNg.GAhKwx.2r4LVj7ZMzUKDVjy3mO1kj60hOE1NKuYVeKXd0"
bot.run(BOT_TOKEN)
