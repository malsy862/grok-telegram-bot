import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROK_KEY = os.getenv("GROK_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Bot Grok aktif!\nKirim pesan apa saja.")

@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer("/start - Mulai\n/help - Bantuan")

@dp.message()
async def chat(message: types.Message):
    try:
        resp = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROK_KEY}", "Content-Type": "application/json"},
            json={
                "model": "grok-4",
                "messages": [{"role": "user", "content": message.text}],
                "temperature": 0.7
            },
            timeout=60
        )
        answer = resp.json()["choices"][0]["message"]["content"]
        await message.answer(answer)
    except:
        await message.answer("❌ Error, coba lagi.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
