import os
import asyncio
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# 1. خادم الويب (للحفاظ على استضافة Render ومنع نوم السيرفر عبر UptimeRobot)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"977 Voice Bots Keeper is Online!")

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

Thread(target=run_server, daemon=True).start()

# 2. قراءة التوكنات والرومات من متغيرات البيئة (Environment Variables)
BOT_CONFIGS = []

# يبحث عن المتغيرات BOT_TOKEN_1 إلى BOT_TOKEN_10 ومقابلها VOICE_CHANNEL_1 إلى VOICE_CHANNEL_10
for i in range(1, 11):
    token = os.environ.get(f"BOT_TOKEN_{i}")
    channel_id = os.environ.get(f"VOICE_CHANNEL_{i}")
    
    if token and channel_id:
        try:
            BOT_CONFIGS.append({
                "token": token.strip(),
                "channel_id": int(channel_id.strip())
            })
        except ValueError:
            print(f"[خطأ] ID الروم الصوتي رقم {i} غير صالح.")

# 3. دالة تشغيل بوت واحد والربط بالروم الصوتي
async def run_single_bot(config, bot_index):
    token = config["token"]
    channel_id = config["channel_id"]
    
    intents = discord.Intents.default()
    intents.voice_states = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"[{bot_index}] تم تسجيل الدخول: {bot.user}")
        try:
            channel = bot.get_channel(channel_id)
            if channel and isinstance(channel, discord.VoiceChannel):
                await channel.connect(reconnect=True, self_deaf=True)
                print(f"[{bot_index}] دخل الروم ({channel.name}) بنجاح.")
            else:
                print(f"[{bot_index}] خطأ: لم يتم العثور على الروم الصوتي {channel_id}")
        except Exception as e:
            print(f"[{bot_index}] فشل التوصيل بالروم: {e}")

    @bot.event
    async def on_voice_state_update(member, before, after):
        # إعادة الاتصال تلقائياً عند الطرد أو انقطاع الاتصال
        if member.id == bot.user.id and after.channel is None:
            await asyncio.sleep(5)
            try:
                channel = bot.get_channel(channel_id)
                if channel:
                    await channel.connect(reconnect=True, self_deaf=True)
                    print(f"[{bot_index}] تمت إعادة الاتصال بالروم تلقائياً.")
            except Exception as e:
                print(f"[{bot_index}] فشل إعادة الاتصال تلقائياً: {e}")

    try:
        await bot.start(token)
    except Exception as e:
        print(f"[{bot_index}] خطأ في التوكن: {e}")

# 4. تشغيل جميع البوتات المكتشفة معاً
async def main():
    if not BOT_CONFIGS:
        print("[تحذير] لم يتم العثور على أي توكنات في Environment Variables! يرجى إضافتها في Render.")
        return

    tasks = [run_single_bot(cfg, idx) for idx, cfg in enumerate(BOT_CONFIGS, start=1)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
