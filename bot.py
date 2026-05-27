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

# ==================== СТРАНЫ С ФЛАГАМИ И ПЕРЕВОДОМ ====================
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

def normalize_country_name(text: str) -> str:
    """
    Приводит название страны к нижнему регистру для поиска
    """
    return text.lower().strip()

def extract_country_from_annotation(annotation: str) -> tuple[str, bool, str]:
    """
    Извлекает название страны из аннотации.
    Работает с любым регистром: Россия, РОССИЯ, Russia, RUSSIA
    Возвращает (русское_название, найдена_ли_страна, флаг)
    """
    try:
        decoded = unquote(annotation)
    except:
        decoded = annotation
    
    # Удаляем эмодзи флагов (в том числе битые)
    flag_pattern = r"[\U0001F1E6-\U0001F1FF]{2}"
    cleaned = re.sub(flag_pattern, "", decoded)
    
    # Удаляем номера серверов (| 1 сервер, | 10 сервер и т.д.)
    cleaned = re.sub(r"\|\s*\d+\s*сервер", "", cleaned)
    cleaned = re.sub(r"\|\s*\d+\s*server", "", cleaned, flags=re.IGNORECASE)
    
    # Удаляем лишние символы
    cleaned = re.sub(r'[^\w\s\-]', ' ', cleaned)
    
    # Разбиваем на слова
    words = re.findall(r'[a-zA-Zа-яА-ЯёЁ\-]+', cleaned)
    
    # Ищем страну в словаре (сравниваем в нижнем регистре)
    for word in words:
        word_lower = word.lower()
        for key, (flag, russian_name) in COUNTRIES.items():
            if word_lower == key.lower():
                return russian_name, True, flag
    
    # Проверяем вхождение подстрок (для названий из двух слов)
    cleaned_lower = cleaned.lower()
    for key, (flag, russian_name) in COUNTRIES.items():
        if key.lower() in cleaned_lower:
            return russian_name, True, flag
    
    return None, False, None

def format_vless_link(vless_url: str, server_number: int) -> str:
    """Форматирует VLESS-ссылку: добавляет флаг, русское название и номер сервера"""
    if not vless_url.startswith("vless://"):
        return vless_url
    
    if "#" not in vless_url:
        new_annotation = f"🔍 На проверке | {server_number} сервер"
        return f"{vless_url}#{quote(new_annotation, safe='')}"
    
    base_part, old_annotation_encoded = vless_url.split("#", 1)
    
    country_name, found, flag = extract_country_from_annotation(old_annotation_encoded)
    
    if found and country_name:
        new_annotation = f"{flag} {country_name} | {server_number} сервер"
    else:
        new_annotation = f"🔍 На проверке | {server_number} сервер"
    
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
        "1. Отправь мне одну или несколько VLESS-ссылок\n"
        "2. Бот определит страну (Россия, Россия, RUSSIA, Russia — любой вариант)\n"
        "3. Переведёт в правильное русское название\n"
        "4. Добавит флаг страны и номер сервера\n\n"
        "✅ *Пример:*\n"
        "`vless://...#Russia` → `vless://...#🇷🇺 Россия | 1 сервер`\n"
        "`vless://...#RUSSIA` → `vless://...#🇷🇺 Россия | 1 сервер`\n\n"
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
