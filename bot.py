import os
import asyncio
import re
from urllib.parse import unquote, quote
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN не установлен!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Все страны Европы + США
FLAGS = {
    "россия": "🇷🇺", "russia": "🇷🇺",
    "нидерланды": "🇳🇱", "netherlands": "🇳🇱", "голландия": "🇳🇱", "holland": "🇳🇱",
    "сша": "🇺🇸", "америка": "🇺🇸", "usa": "🇺🇸",
    "германия": "🇩🇪", "germany": "🇩🇪",
    "франция": "🇫🇷", "france": "🇫🇷",
    "великобритания": "🇬🇧", "англия": "🇬🇧", "uk": "🇬🇧", "britain": "🇬🇧",
    "италия": "🇮🇹", "italy": "🇮🇹",
    "испания": "🇪🇸", "spain": "🇪🇸",
    "польша": "🇵🇱", "poland": "🇵🇱",
    "украина": "🇺🇦", "ukraine": "🇺🇦",
    "беларусь": "🇧🇾", "belarus": "🇧🇾",
    "казахстан": "🇰🇿", "kazakhstan": "🇰🇿",
    "турция": "🇹🇷", "turkey": "🇹🇷",
    "швеция": "🇸🇪", "sweden": "🇸🇪",
    "норвегия": "🇳🇴", "norway": "🇳🇴",
    "финляндия": "🇫🇮", "finland": "🇫🇮",
    "дания": "🇩🇰", "denmark": "🇩🇰",
    "бельгия": "🇧🇪", "belgium": "🇧🇪",
    "швейцария": "🇨🇭", "switzerland": "🇨🇭",
    "австрия": "🇦🇹", "austria": "🇦🇹",
    "чехия": "🇨🇿", "czech": "🇨🇿",
    "словакия": "🇸🇰", "slovakia": "🇸🇰",
    "венгрия": "🇭🇺", "hungary": "🇭🇺",
    "румыния": "🇷🇴", "romania": "🇷🇴",
    "болгария": "🇧🇬", "bulgaria": "🇧🇬",
    "греция": "🇬🇷", "greece": "🇬🇷",
    "португалия": "🇵🇹", "portugal": "🇵🇹",
    "ирландия": "🇮🇪", "ireland": "🇮🇪",
    "исландия": "🇮🇸", "iceland": "🇮🇸",
    "эстония": "🇪🇪", "estonia": "🇪🇪",
    "латвия": "🇱🇻", "latvia": "🇱🇻",
    "литва": "🇱🇹", "lithuania": "🇱🇹",
    "сербия": "🇷🇸", "serbia": "🇷🇸",
    "хорватия": "🇭🇷", "croatia": "🇭🇷",
    "словения": "🇸🇮", "slovenia": "🇸🇮",
    "япония": "🇯🇵", "japan": "🇯🇵",
    "китай": "🇨🇳", "china": "🇨🇳",
    "сингапур": "🇸🇬", "singapore": "🇸🇬",
    "канада": "🇨🇦", "canada": "🇨🇦",
    "австралия": "🇦🇺", "australia": "🇦🇺",
}

def get_flag(country_name: str) -> str:
    country_lower = country_name.lower().strip()
    for name, flag in FLAGS.items():
        if name in country_lower or country_lower in name:
            return flag
    return "🏳️"

def extract_country_from_annotation(annotation: str) -> str:
    try:
        decoded = unquote(annotation)
    except:
        decoded = annotation
    flag_pattern = r"[\U0001F1E6-\U0001F1FF]{2}"
    cleaned = re.sub(flag_pattern, "", decoded)
    cleaned = re.sub(r"\|\s*\d+\s*сервер", "", cleaned)
    cleaned = re.sub(r"[^\w\s\-]", "", cleaned)
    return cleaned.strip()

def format_vless_link(vless_url: str, server_number: int) -> str:
    if not vless_url.startswith("vless://"):
        return vless_url
    if "#" not in vless_url:
        country_name = "сервер"
        flag = "🖥️"
        return f"{vless_url}#{quote(f'{flag} {country_name} | {server_number} сервер', safe='')}"
    base_part, old_annotation_encoded = vless_url.split("#", 1)
    country_name = extract_country_from_annotation(old_annotation_encoded)
    if not country_name:
        country_name = "сервер"
    flag = get_flag(country_name)
    new_annotation = f"{flag} {country_name} | {server_number} сервер"
    return f"{base_part}#{quote(new_annotation, safe='')}"

def process_vless_links(text: str) -> tuple[str, int]:
    vless_pattern = r"vless://[^\s]+"
    links = re.findall(vless_pattern, text)
    if not links:
        return text, 0
    result = text
    for idx, link in enumerate(links, 1):
        new_link = format_vless_link(link, idx)
        result = result.replace(link, new_link, 1)
    return result, len(links)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🔧 *Бот для форматирования VLESS-ссылок*\n\n"
        "📤 Отправь VLESS-ссылку, а бот добавит флаг страны и нумерацию.\n\n"
        "✅ Поддерживаются все страны Европы + США, Япония, Китай и др.",
        parse_mode="Markdown"
    )

@dp.message()
async def handle_vless_links(message: types.Message):
    if message.document:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        try:
            text = downloaded_file.read().decode('utf-8')
            await message.answer(f"📄 Файл получен, обрабатываю...")
        except Exception:
            await message.answer("❌ Не удалось прочитать файл.")
            return
    else:
        text = message.text
    
    if not text or "vless://" not in text:
        await message.answer("❌ Отправь VLESS-ссылку (начинается с `vless://`)", parse_mode="Markdown")
        return
    
    result, count = process_vless_links(text)
    if len(result) > 4000:
        result_bytes = result.encode('utf-8')
        await message.answer_document(
            types.BufferedInputFile(result_bytes, filename="formatted_links.txt"),
            caption=f"✅ Обработано {count} ссылок"
        )
    else:
        await message.answer(f"✅ *Готово!* ({count} ссылок)\n\n`{result}`", parse_mode="Markdown")

async def main():
    print("🚀 Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
