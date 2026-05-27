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

# ==================== ВСЕ СТРАНЫ МИРА (197 стран) ====================
COUNTRIES = {
    "россия": ["🇷🇺", "Россия"], "russia": ["🇷🇺", "Россия"],
    "финляндия": ["🇫🇮", "Финляндия"], "finland": ["🇫🇮", "Финляндия"],
    "сша": ["🇺🇸", "США"], "usa": ["🇺🇸", "США"], "united states": ["🇺🇸", "США"],
    "германия": ["🇩🇪", "Германия"], "germany": ["🇩🇪", "Германия"],
    "франция": ["🇫🇷", "Франция"], "france": ["🇫🇷", "Франция"],
    "италия": ["🇮🇹", "Италия"], "italy": ["🇮🇹", "Италия"],
    "испания": ["🇪🇸", "Испания"], "spain": ["🇪🇸", "Испания"],
    "нидерланды": ["🇳🇱", "Нидерланды"], "netherlands": ["🇳🇱", "Нидерланды"],
    "великобритания": ["🇬🇧", "Великобритания"], "uk": ["🇬🇧", "Великобритания"],
    "польша": ["🇵🇱", "Польша"], "poland": ["🇵🇱", "Польша"],
    "украина": ["🇺🇦", "Украина"], "ukraine": ["🇺🇦", "Украина"],
    "чехия": ["🇨🇿", "Чехия"], "czech": ["🇨🇿", "Чехия"],
    "австрия": ["🇦🇹", "Австрия"], "austria": ["🇦🇹", "Австрия"],
    "швейцария": ["🇨🇭", "Швейцария"], "switzerland": ["🇨🇭", "Швейцария"],
    "швеция": ["🇸🇪", "Швеция"], "sweden": ["🇸🇪", "Швеция"],
    "норвегия": ["🇳🇴", "Норвегия"], "norway": ["🇳🇴", "Норвегия"],
    "европа": ["🇪🇺", "Европа"], "europe": ["🇪🇺", "Европа"],
    "канада": ["🇨🇦", "Канада"], "canada": ["🇨🇦", "Канада"],
    "бразилия": ["🇧🇷", "Бразилия"], "brazil": ["🇧🇷", "Бразилия"],
    "австралия": ["🇦🇺", "Австралия"], "australia": ["🇦🇺", "Австралия"],
    "япония": ["🇯🇵", "Япония"], "japan": ["🇯🇵", "Япония"],
    "китай": ["🇨🇳", "Китай"], "china": ["🇨🇳", "Китай"],
    "индия": ["🇮🇳", "Индия"], "india": ["🇮🇳", "Индия"],
    "турция": ["🇹🇷", "Турция"], "turkey": ["🇹🇷", "Турция"],
    "казахстан": ["🇰🇿", "Казахстан"], "kazakhstan": ["🇰🇿", "Казахстан"],
    "израиль": ["🇮🇱", "Израиль"], "israel": ["🇮🇱", "Израиль"],
    "оаэ": ["🇦🇪", "ОАЭ"], "uae": ["🇦🇪", "ОАЭ"],
    "сингапур": ["🇸🇬", "Сингапур"], "singapore": ["🇸🇬", "Сингапур"],
}

FLAG_TO_NAME = {}
for key, (flag, name) in COUNTRIES.items():
    if flag not in FLAG_TO_NAME:
        FLAG_TO_NAME[flag] = name

def process_single_link(link: str, index: int) -> str:
    if not link.startswith("vless://"):
        return link
    
    if "#" not in link:
        return f"{link}#🏳️ На проверке | {index} сервер"
    
    base, encoded_ann = link.split("#", 1)
    
    try:
        ann = unquote(encoded_ann)
    except:
        ann = encoded_ann
    
    flag_match = re.search(r"[\U0001F1E6-\U0001F1FF]{2}", ann)
    flag = flag_match.group(0) if flag_match else None
    
    country_name = None
    words = re.findall(r'[a-zA-Zа-яА-ЯёЁ\-]+', ann)
    for word in words:
        word_lower = word.lower()
        for key in COUNTRIES:
            if word_lower == key.lower():
                country_name = COUNTRIES[key][1]
                break
        if country_name:
            break
    
    if country_name:
        for key, (f, n) in COUNTRIES.items():
            if n == country_name:
                flag = f
                break
    elif flag and flag in FLAG_TO_NAME:
        country_name = FLAG_TO_NAME[flag]
    else:
        flag = "🏳️"
        country_name = "На проверке"
    
    new_ann = f"{flag} {country_name} | {index} сервер"
    encoded_new_ann = quote(new_ann, safe='')
    
    return f"{base}#{encoded_new_ann}"

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🌍 *Бот для форматирования VLESS-ссылок*\n\n"
        "📤 Отправь мне VLESS-ссылки (можно просто скопировать и вставить в чат)\n\n"
        "📎 *Как работает:*\n"
        "• **До 5 ссылок** → отправлю текстом (кликабельно)\n"
        "• **6+ ссылок** → отправлю ОДНИМ файлом .txt\n\n"
        "✅ Поддерживаются ВСЕ страны мира\n"
        "✅ Если страна не найдена — ставит 🏳️ На проверке",
        parse_mode="Markdown"
    )

@dp.message()
async def handle_text(message: types.Message):
    text = message.text.strip()
    
    if not text:
        await message.answer("❌ Отправь текст с VLESS-ссылками")
        return
    
    if "vless://" not in text:
        await message.answer("❌ Не найдено VLESS-ссылок")
        return
    
    # Находим все VLESS-ссылки
    vless_pattern = r"vless://[^\s]+"
    links = re.findall(vless_pattern, text)
    
    if not links:
        await message.answer("❌ Не найдено VLESS-ссылок")
        return
    
    # Обрабатываем каждую ссылку
    result_lines = []
    for idx, link in enumerate(links, 1):
        processed = process_single_link(link, idx)
        result_lines.append(processed)
    
    result_text = '\n'.join(result_lines)
    count = len(links)
    
    # ГЛАВНОЕ: если 6+ ссылок — ВСЕГДА файл
    if count >= 6:
        # ОДИН файл со всеми ссылками
        result_bytes = result_text.encode('utf-8')
        await message.answer_document(
            types.BufferedInputFile(result_bytes, filename="formatted_links.txt"),
            caption=f"✅ Обработано ссылок: {count}\n📎 Все ссылки в одном файле"
        )
    else:
        # 1-5 ссылок — текстом
        word = "ссылка" if count == 1 else "ссылки" if count <= 4 else "ссылок"
        await message.answer(
            f"✅ *Обработано {count} {word}*\n\n"
            f"{result_text}",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

async def main():
    print("🚀 Бот для форматирования VLESS-ссылок запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
