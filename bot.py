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

# ==================== СТРАНЫ ====================
COUNTRIES = {
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
    "европа": ["🇪🇺", "Европа"], "europe": ["🇪🇺", "Европа"],
    "сша": ["🇺🇸", "США"], "usa": ["🇺🇸", "США"], "united states": ["🇺🇸", "США"],
    "канада": ["🇨🇦", "Канада"], "canada": ["🇨🇦", "Канада"],
    "мексика": ["🇲🇽", "Мексика"], "mexico": ["🇲🇽", "Мексика"],
    "бразилия": ["🇧🇷", "Бразилия"], "brazil": ["🇧🇷", "Бразилия"],
    "аргентина": ["🇦🇷", "Аргентина"], "argentina": ["🇦🇷", "Аргентина"],
    "австралия": ["🇦🇺", "Австралия"], "australia": ["🇦🇺", "Австралия"],
}

# Обратный словарь: флаг -> страна
FLAG_TO_NAME = {}
for flag, name in [(f, n) for (_, (f, n)) in COUNTRIES.items()]:
    if flag not in FLAG_TO_NAME:
        FLAG_TO_NAME[flag] = name

def process_single_link(link: str, index: int) -> str:
    """Обрабатывает одну VLESS-ссылку"""
    if not link.startswith("vless://"):
        return link
    
    # Если нет аннотации
    if "#" not in link:
        return f"{link}#🏳️ На проверке | {index} сервер"
    
    # Разделяем ссылку
    base, encoded_ann = link.split("#", 1)
    
    # Декодируем аннотацию
    try:
        ann = unquote(encoded_ann)
    except:
        ann = encoded_ann
    
    # Ищем флаг в аннотации
    flag_match = re.search(r"[\U0001F1E6-\U0001F1FF]{2}", ann)
    flag = flag_match.group(0) if flag_match else None
    
    # Ищем название страны в аннотации
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
    
    # Определяем итоговый флаг и название
    if country_name:
        # Нашли название — берём правильный флаг для этой страны
        for key, (f, n) in COUNTRIES.items():
            if n == country_name:
                flag = f
                break
    elif flag and flag in FLAG_TO_NAME:
        # Нет названия, но есть флаг
        country_name = FLAG_TO_NAME[flag]
    else:
        # Ничего не нашли
        flag = "🏳️"
        country_name = "На проверке"
    
    # Собираем новую аннотацию
    new_ann = f"{flag} {country_name} | {index} сервер"
    encoded_new_ann = quote(new_ann, safe='')
    
    return f"{base}#{encoded_new_ann}"

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🌍 *Бот для форматирования VLESS-ссылок*\n\n"
        "📤 Отправь мне файл .txt с VLESS-ссылками (по одной на строку)\n"
        "📎 Бот обработает все ссылки и вернёт **один файл** с результатом\n\n"
        "✅ Поддерживаются флаги и названия стран на русском/английском\n"
        "✅ Если страна не найдена — ставит 🏳️ На проверке\n\n"
        "💡 Просто отправь файл и получи результат!",
        parse_mode="Markdown"
    )

@dp.message()
async def handle_file(message: types.Message):
    # Получаем файл
    if not message.document:
        await message.answer("❌ Отправь файл .txt с VLESS-ссылками")
        return
    
    # Скачиваем файл
    file_info = await bot.get_file(message.document.file_id)
    downloaded = await bot.download_file(file_info.file_path)
    
    try:
        text = downloaded.read().decode('utf-8')
    except Exception as e:
        await message.answer(f"❌ Ошибка чтения файла: {e}")
        return
    
    # Разбиваем на строки и обрабатываем
    lines = text.strip().split('\n')
    result_lines = []
    index = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "vless://" in line:
            # Извлекаем VLESS-ссылку из строки
            match = re.search(r"vless://[^\s]+", line)
            if match:
                vless = match.group(0)
                processed = process_single_link(vless, index)
                result_lines.append(processed)
                index += 1
            else:
                result_lines.append(line)
        else:
            result_lines.append(line)
    
    if not result_lines:
        await message.answer("❌ Не найдено VLESS-ссылок в файле")
        return
    
    # Формируем результат
    result_text = '\n'.join(result_lines)
    count = index - 1
    
    # Отправляем результат
    result_bytes = result_text.encode('utf-8')
    await message.answer_document(
        types.BufferedInputFile(result_bytes, filename="formatted_links.txt"),
        caption=f"✅ Обработано ссылок: {count}\n📎 Все ссылки в одном файле"
    )

async def main():
    print("🚀 Бот для форматирования VLESS-ссылок запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
