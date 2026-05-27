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

# ==================== СТРАНЫ: ключ -> [флаг, русское_название] ====================
COUNTRIES = {
    # Азия
    "россия": ["🇷🇺", "Россия"], "russia": ["🇷🇺", "Россия"],
    "китай": ["🇨🇳", "Китай"], "china": ["🇨🇳", "Китай"],
    "япония": ["🇯🇵", "Япония"], "japan": ["🇯🇵", "Япония"],
    "индия": ["🇮🇳", "Индия"], "india": ["🇮🇳", "Индия"],
    "турция": ["🇹🇷", "Турция"], "turkey": ["🇹🇷", "Турция"],
    "казахстан": ["🇰🇿", "Казахстан"], "kazakhstan": ["🇰🇿", "Казахстан"],
    "узбекистан": ["🇺🇿", "Узбекистан"], "uzbekistan": ["🇺🇿", "Узбекистан"],
    "израиль": ["🇮🇱", "Израиль"], "israel": ["🇮🇱", "Израиль"],
    "оаэ": ["🇦🇪", "ОАЭ"], "uae": ["🇦🇪", "ОАЭ"],
    "сингапур": ["🇸🇬", "Сингапур"], "singapore": ["🇸🇬", "Сингапур"],
    "южная корея": ["🇰🇷", "Южная Корея"], "korea": ["🇰🇷", "Южная Корея"], "south korea": ["🇰🇷", "Южная Корея"],
    
    # Европа
    "германия": ["🇩🇪", "Германия"], "germany": ["🇩🇪", "Германия"],
    "франция": ["🇫🇷", "Франция"], "france": ["🇫🇷", "Франция"],
    "италия": ["🇮🇹", "Италия"], "italy": ["🇮🇹", "Италия"],
    "испания": ["🇪🇸", "Испания"], "spain": ["🇪🇸", "Испания"],
    "нидерланды": ["🇳🇱", "Нидерланды"], "netherlands": ["🇳🇱", "Нидерланды"], "голландия": ["🇳🇱", "Нидерланды"],
    "великобритания": ["🇬🇧", "Великобритания"], "uk": ["🇬🇧", "Великобритания"], "britain": ["🇬🇧", "Великобритания"],
    "польша": ["🇵🇱", "Польша"], "poland": ["🇵🇱", "Польша"],
    "украина": ["🇺🇦", "Украина"], "ukraine": ["🇺🇦", "Украина"],
    "беларусь": ["🇧🇾", "Беларусь"], "belarus": ["🇧🇾", "Беларусь"],
    "чехия": ["🇨🇿", "Чехия"], "czech": ["🇨🇿", "Чехия"],
    "австрия": ["🇦🇹", "Австрия"], "austria": ["🇦🇹", "Австрия"],
    "швейцария": ["🇨🇭", "Швейцария"], "switzerland": ["🇨🇭", "Швейцария"],
    "швеция": ["🇸🇪", "Швеция"], "sweden": ["🇸🇪", "Швеция"],
    "норвегия": ["🇳🇴", "Норвегия"], "norway": ["🇳🇴", "Норвегия"],
    "финляндия": ["🇫🇮", "Финляндия"], "finland": ["🇫🇮", "Финляндия"],
    "дания": ["🇩🇰", "Дания"], "denmark": ["🇩🇰", "Дания"],
    "бельгия": ["🇧🇪", "Бельгия"], "belgium": ["🇧🇪", "Бельгия"],
    "португалия": ["🇵🇹", "Португалия"], "portugal": ["🇵🇹", "Португалия"],
    "греция": ["🇬🇷", "Греция"], "greece": ["🇬🇷", "Греция"],
    "венгрия": ["🇭🇺", "Венгрия"], "hungary": ["🇭🇺", "Венгрия"],
    "румыния": ["🇷🇴", "Румыния"], "romania": ["🇷🇴", "Румыния"],
    "болгария": ["🇧🇬", "Болгария"], "bulgaria": ["🇧🇬", "Болгария"],
    "сербия": ["🇷🇸", "Сербия"], "serbia": ["🇷🇸", "Сербия"],
    "хорватия": ["🇭🇷", "Хорватия"], "croatia": ["🇭🇷", "Хорватия"],
    "ирландия": ["🇮🇪", "Ирландия"], "ireland": ["🇮🇪", "Ирландия"],
    "исландия": ["🇮🇸", "Исландия"], "iceland": ["🇮🇸", "Исландия"],
    "эстония": ["🇪🇪", "Эстония"], "estonia": ["🇪🇪", "Эстония"],
    "латвия": ["🇱🇻", "Латвия"], "latvia": ["🇱🇻", "Латвия"],
    "литва": ["🇱🇹", "Литва"], "lithuania": ["🇱🇹", "Литва"],
    
    # Европейский союз
    "европа": ["🇪🇺", "Европа"], "europe": ["🇪🇺", "Европа"],
    
    # Северная Америка
    "сша": ["🇺🇸", "США"], "америка": ["🇺🇸", "США"], "usa": ["🇺🇸", "США"], "united states": ["🇺🇸", "США"],
    "канада": ["🇨🇦", "Канада"], "canada": ["🇨🇦", "Канада"],
    "мексика": ["🇲🇽", "Мексика"], "mexico": ["🇲🇽", "Мексика"],
    
    # Южная Америка
    "бразилия": ["🇧🇷", "Бразилия"], "brazil": ["🇧🇷", "Бразилия"],
    "аргентина": ["🇦🇷", "Аргентина"], "argentina": ["🇦🇷", "Аргентина"],
    
    # Австралия
    "австралия": ["🇦🇺", "Австралия"], "australia": ["🇦🇺", "Австралия"],
}

# Обратный словарь: флаг -> русское название
FLAG_TO_COUNTRY = {}
for key, (flag, name) in COUNTRIES.items():
    if flag not in FLAG_TO_COUNTRY:
        FLAG_TO_COUNTRY[flag] = name

def extract_flag_from_text(text: str) -> str | None:
    """Извлекает флаг (эмодзи страны) из текста"""
    flag_pattern = r"[\U0001F1E6-\U0001F1FF]{2}"
    match = re.search(flag_pattern, text)
    return match.group(0) if match else None

def extract_country_name_from_text(text: str) -> str | None:
    """Извлекает название страны из текста (рус/англ, любой регистр)"""
    words = re.findall(r'[a-zA-Zа-яА-ЯёЁ\-]+', text)
    for word in words:
        word_lower = word.lower()
        for key in COUNTRIES.keys():
            if word_lower == key.lower():
                return COUNTRIES[key][1]  # возвращаем русское название
    return None

def determine_country(annotation: str) -> tuple[str, str]:
    """
    Определяет страну по аннотации.
    Возвращает (флаг, русское_название)
    """
    flag = extract_flag_from_text(annotation)
    name = extract_country_name_from_text(annotation)
    
    # Если есть и флаг, и название — проверяем соответствие
    if flag and name:
        # Проверяем, соответствует ли флаг названию
        expected_flag = None
        for key, (f, n) in COUNTRIES.items():
            if n == name:
                expected_flag = f
                break
        if expected_flag and flag != expected_flag:
            # Флаг не соответствует названию — исправляем
            return expected_flag, name
        return flag, name
    
    # Если есть только флаг — определяем по флагу
    if flag and flag in FLAG_TO_COUNTRY:
        return flag, FLAG_TO_COUNTRY[flag]
    
    # Если есть только название — определяем по названию
    if name:
        for key, (f, n) in COUNTRIES.items():
            if n == name:
                return f, n
    
    # Если ничего нет
    return "🏳️", "На проверке"

def format_vless_link(vless_url: str, server_number: int) -> str:
    """Форматирует VLESS-ссылку: добавляет флаг, название и номер сервера"""
    if not vless_url.startswith("vless://"):
        return vless_url
    
    if "#" not in vless_url:
        new_annotation = f"🏳️ На проверке | {server_number} сервер"
        return f"{vless_url}#{quote(new_annotation, safe='')}"
    
    base_part, old_annotation_encoded = vless_url.split("#", 1)
    
    try:
        old_annotation = unquote(old_annotation_encoded)
    except:
        old_annotation = old_annotation_encoded
    
    # Определяем страну
    flag, country_name = determine_country(old_annotation)
    
    # Формируем новую аннотацию
    new_annotation = f"{flag} {country_name} | {server_number} сервер"
    new_annotation_encoded = quote(new_annotation, safe='')
    
    return f"{base_part}#{new_annotation_encoded}"

def process_vless_links(text: str) -> tuple[str, int]:
    """Находит все VLESS-ссылки в тексте и форматирует их"""
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
        "🌍 *Бот для форматирования VLESS-ссылок*\n\n"
        "📤 *Как работает:*\n"
        "• Определяет страну по флагу или названию\n"
        "• Если есть флаг и название — проверяет соответствие\n"
        "• Если есть только флаг — определяет страну\n"
        "• Если есть только название — добавляет флаг\n"
        "• Если нет ничего — ставит 🏳️ На проверке\n\n"
        "✅ *Примеры:*\n"
        "`vless://...#Russia` → `🇷🇺 Россия | 1 сервер`\n"
        "`vless://...#🇩🇪` → `🇩🇪 Германия | 1 сервер`\n"
        "`vless://...#🇫🇷 France` → `🇫🇷 Франция | 1 сервер`\n\n"
        "📎 Можно отправлять несколько ссылок сразу, файл `.txt` или просто текст.",
        parse_mode="Markdown"
    )

@dp.message()
async def handle_vless_links(message: types.Message):
    if message.document:
        file_info = await bot.get_file(message.document.file_id)
        downloaded_file = await bot.download_file(file_info.file_path)
        try:
            text = downloaded_file.read().decode('utf-8')
            await message.answer(f"📄 Получен файл: {message.document.file_name}\n🔄 Обрабатываю...")
        except Exception:
            await message.answer("❌ Не удалось прочитать файл. Убедись, что это текстовый файл (.txt) с кодировкой UTF-8.")
            return
    else:
        text = message.text
    
    if not text:
        await message.answer("❌ Отправь текст или файл с VLESS-ссылками.")
        return
    
    if "vless://" not in text:
        await message.answer(
            "❌ Не найдено VLESS-ссылок.\n\nУбедись, что ссылки начинаются с `vless://`",
            parse_mode="Markdown"
        )
        return
    
    result, count = process_vless_links(text)
    
    if result == text:
        await message.answer("⚠️ Ссылки обнаружены, но не удалось их обработать. Проверь формат.")
        return
    
    if len(result) > 4000:
        result_bytes = result.encode('utf-8')
        await message.answer_document(
            types.BufferedInputFile(result_bytes, filename="formatted_links.txt"),
            caption=f"✅ Обработано ссылок: {count}"
        )
    else:
        await message.answer(
            f"✅ *Готово!* (обработано {count} ссылок)\n\n"
            f"```\n{result}\n```",
            parse_mode="Markdown"
        )

async def main():
    print("🚀 Бот для форматирования VLESS-ссылок запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
