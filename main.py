import asyncio
import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Ambil token dari Railway
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROK_KEY = os.getenv("GROK_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Bot Grok aktif!\nKirim pesan apa saja.")

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer("Kirim pesan apa saja, aku akan balas pakai Grok.")

@dp.message()
async def chat(message: types.Message):
    if not GROK_KEY:
        return await message.answer("❌ API Key Grok belum diatur di Railway.")

    try:
        resp = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROK_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "grok-beta",      # Model yang paling stabil
                "messages": [{"role": "user", "content": message.text}],
                "temperature": 0.7,
                "max_tokens": 1500
            },
            timeout=60
        )
        
        resp.raise_for_status()
        data = resp.json()
        answer = data["choices"][0]["message"]["content"]
        
        await message.answer(answer)

    except Exception as e:
        print(f"ERROR: {str(e)}")   # Muncul di Railway Logs
        await message.answer("❌ Error, coba lagi nanti.")

async def main():
    print("✅ Bot Grok berhasil dijalankan!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
