import os
import asyncio
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# 1. خادم الويب (يدعم GET و HEAD لإرضاء UptimeRobot)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"977 Auto-Line Bot is Alive!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

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

TARGET_CHANNELS = [
    1540429474405818468, 1540429517506478090, 1540429563660599356, 1540429583902580826,
    1540429188077453433, 1540429149284606092, 1540429233409630258, 1540429110680092772,
    1540428845193101503, 1540428777362956308, 1538886366069629100, 1538886597158772847,
    1538886660492755035, 1539450874785693716, 1538886761990594650, 1538886721272549446,
    1538886981692424253, 1538886884082589787
]

@bot.event
async def on_ready():
    print(f"تم تشغيل البوت بنجاح: {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id in TARGET_CHANNELS:
        if os.path.exists("line.png"):
            await message.channel.send(file=discord.File("line.png"))

    await bot.process_commands(message)

bot.run(os.environ.get("BOT_TOKEN"))
