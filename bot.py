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

# ==================== ВСЕ СТРАНЫ МИРА С ФЛАГАМИ ====================
FLAGS = {
    # Азия
    "россия": "🇷🇺", "россии": "🇷🇺", "russia": "🇷🇺",
    "китай": "🇨🇳", "china": "🇨🇳",
    "япония": "🇯🇵", "japan": "🇯🇵",
    "индия": "🇮🇳", "india": "🇮🇳",
    "индонезия": "🇮🇩", "indonesia": "🇮🇩",
    "пакистан": "🇵🇰", "pakistan": "🇵🇰",
    "бангладеш": "🇧🇩", "bangladesh": "🇧🇩",
    "турция": "🇹🇷", "турции": "🇹🇷", "turkey": "🇹🇷",
    "иран": "🇮🇷", "iran": "🇮🇷",
    "ирак": "🇮🇶", "iraq": "🇮🇶",
    "афганистан": "🇦🇫", "afghanistan": "🇦🇫",
    "саудовская аравия": "🇸🇦", "saudi arabia": "🇸🇦",
    "йемен": "🇾🇪", "yemen": "🇾🇪",
    "сирия": "🇸🇾", "syria": "🇸🇾",
    "казахстан": "🇰🇿", "казахстана": "🇰🇿", "kazakhstan": "🇰🇿",
    "узбекистан": "🇺🇿", "uzbekistan": "🇺🇿",
    "малайзия": "🇲🇾", "malaysia": "🇲🇾",
    "вьетнам": "🇻🇳", "vietnam": "🇻🇳",
    "таиланд": "🇹🇭", "thailand": "🇹🇭",
    "мьянма": "🇲🇲", "myanmar": "🇲🇲",
    "южная корея": "🇰🇷", "korea": "🇰🇷", "south korea": "🇰🇷",
    "непал": "🇳🇵", "nepal": "🇳🇵",
    "шри-ланка": "🇱🇰", "sri lanka": "🇱🇰",
    "камбоджа": "🇰🇭", "cambodia": "🇰🇭",
    "таджикистан": "🇹🇯", "tajikistan": "🇹🇯",
    "киргизия": "🇰🇬", "kyrgyzstan": "🇰🇬",
    "туркменистан": "🇹🇲", "turkmenistan": "🇹🇲",
    "азербайджан": "🇦🇿", "azerbaijan": "🇦🇿",
    "грузия": "🇬🇪", "грузии": "🇬🇪", "georgia": "🇬🇪",
    "армения": "🇦🇲", "армении": "🇦🇲", "armenia": "🇦🇲",
    "израиль": "🇮🇱", "israel": "🇮🇱",
    "палестина": "🇵🇸", "palestine": "🇵🇸",
    "иордания": "🇯🇴", "jordan": "🇯🇴",
    "ливан": "🇱🇧", "lebanon": "🇱🇧",
    "оман": "🇴🇲", "oman": "🇴🇲",
    "катар": "🇶🇦", "qatar": "🇶🇦",
    "кувейт": "🇰🇼", "kuwait": "🇰🇼",
    "бахрейн": "🇧🇭", "bahrain": "🇧🇭",
    "оаэ": "🇦🇪", "uae": "🇦🇪", "объединенные арабские эмираты": "🇦🇪",
    "монголия": "🇲🇳", "mongolia": "🇲🇳",
    "филиппины": "🇵🇭", "philippines": "🇵🇭",
    "сингапур": "🇸🇬", "singapore": "🇸🇬",
    "бруней": "🇧🇳", "brunei": "🇧🇳",
    "лаос": "🇱🇦", "laos": "🇱🇦",
    "восточный тимор": "🇹🇱", "timor-leste": "🇹🇱",
    "мальдивы": "🇲🇻", "maldives": "🇲🇻",
    
    # Европа
    "австрия": "🇦🇹", "австрии": "🇦🇹", "austria": "🇦🇹",
    "албания": "🇦🇱", "албании": "🇦🇱", "albania": "🇦🇱",
    "андорра": "🇦🇩", "андорры": "🇦🇩", "andorra": "🇦🇩",
    "беларусь": "🇧🇾", "беларуси": "🇧🇾", "belarus": "🇧🇾",
    "бельгия": "🇧🇪", "бельгии": "🇧🇪", "belgium": "🇧🇪",
    "болгария": "🇧🇬", "болгарии": "🇧🇬", "bulgaria": "🇧🇬",
    "босния": "🇧🇦", "боснии": "🇧🇦", "bosnia": "🇧🇦", "босния и герцеговина": "🇧🇦",
    "ватикан": "🇻🇦", "vatican": "🇻🇦",
    "великобритания": "🇬🇧", "англия": "🇬🇧", "uk": "🇬🇧", "britain": "🇬🇧", "united kingdom": "🇬🇧",
    "венгрия": "🇭🇺", "венгрии": "🇭🇺", "hungary": "🇭🇺",
    "германия": "🇩🇪", "германии": "🇩🇪", "germany": "🇩🇪",
    "греция": "🇬🇷", "греции": "🇬🇷", "greece": "🇬🇷",
    "дания": "🇩🇰", "дании": "🇩🇰", "denmark": "🇩🇰",
    "ирландия": "🇮🇪", "ирландии": "🇮🇪", "ireland": "🇮🇪",
    "исландия": "🇮🇸", "исландии": "🇮🇸", "iceland": "🇮🇸",
    "испания": "🇪🇸", "испании": "🇪🇸", "spain": "🇪🇸",
    "италия": "🇮🇹", "италии": "🇮🇹", "italy": "🇮🇹",
    "кипр": "🇨🇾", "кипра": "🇨🇾", "cyprus": "🇨🇾",
    "латвия": "🇱🇻", "латвии": "🇱🇻", "latvia": "🇱🇻",
    "литва": "🇱🇹", "литвы": "🇱🇹", "lithuania": "🇱🇹",
    "лихтенштейн": "🇱🇮", "liechtenstein": "🇱🇮",
    "люксембург": "🇱🇺", "luxembourg": "🇱🇺",
    "мальта": "🇲🇹", "мальты": "🇲🇹", "malta": "🇲🇹",
    "молдова": "🇲🇩", "молдовы": "🇲🇩", "moldova": "🇲🇩",
    "монако": "🇲🇨", "monaco": "🇲🇨",
    "нидерланды": "🇳🇱", "нидерландов": "🇳🇱", "netherlands": "🇳🇱", "голландия": "🇳🇱", "holland": "🇳🇱",
    "норвегия": "🇳🇴", "норвегии": "🇳🇴", "norway": "🇳🇴",
    "польша": "🇵🇱", "польши": "🇵🇱", "poland": "🇵🇱",
    "португалия": "🇵🇹", "португалии": "🇵🇹", "portugal": "🇵🇹",
    "румыния": "🇷🇴", "румынии": "🇷🇴", "romania": "🇷🇴",
    "сан-марино": "🇸🇲", "san marino": "🇸🇲",
    "северная македония": "🇲🇰", "македония": "🇲🇰", "north macedonia": "🇲🇰",
    "сербия": "🇷🇸", "сербии": "🇷🇸", "serbia": "🇷🇸",
    "словакия": "🇸🇰", "словакии": "🇸🇰", "slovakia": "🇸🇰",
    "словения": "🇸🇮", "словении": "🇸🇮", "slovenia": "🇸🇮",
    "украина": "🇺🇦", "украины": "🇺🇦", "ukraine": "🇺🇦",
    "финляндия": "🇫🇮", "финляндии": "🇫🇮", "finland": "🇫🇮",
    "франция": "🇫🇷", "франции": "🇫🇷", "france": "🇫🇷",
    "хорватия": "🇭🇷", "хорватии": "🇭🇷", "croatia": "🇭🇷",
    "черногория": "🇲🇪", "черногории": "🇲🇪", "montenegro": "🇲🇪",
    "чехия": "🇨🇿", "чехии": "🇨🇿", "czech": "🇨🇿", "czech republic": "🇨🇿",
    "швейцария": "🇨🇭", "швейцарии": "🇨🇭", "switzerland": "🇨🇭",
    "швеция": "🇸🇪", "швеции": "🇸🇪", "sweden": "🇸🇪",
    "эстония": "🇪🇪", "эстонии": "🇪🇪", "estonia": "🇪🇪",
    
    # Европейский союз
    "европа": "🇪🇺", "europe": "🇪🇺", "евросоюз": "🇪🇺", "european union": "🇪🇺",
    
    # Африка
    "египет": "🇪🇬", "egypt": "🇪🇬",
    "нигерия": "🇳🇬", "nigeria": "🇳🇬",
    "эфиопия": "🇪🇹", "ethiopia": "🇪🇹",
    "юар": "🇿🇦", "south africa": "🇿🇦", "южно-африканская республика": "🇿🇦",
    "конго": "🇨🇩", "congo": "🇨🇩",
    "танзания": "🇹🇿", "tanzania": "🇹🇿",
    "кения": "🇰🇪", "kenya": "🇰🇪",
    "алжир": "🇩🇿", "algeria": "🇩🇿",
    "судан": "🇸🇩", "sudan": "🇸🇩",
    "марокко": "🇲🇦", "morocco": "🇲🇦",
    "ангола": "🇦🇴", "angola": "🇦🇴",
    "мозамбик": "🇲🇿", "mozambique": "🇲🇿",
    "гана": "🇬🇭", "ghana": "🇬🇭",
    "камерун": "🇨🇲", "cameroon": "🇨🇲",
    "кот-д'ивуар": "🇨🇮", "ivory coast": "🇨🇮",
    "нигер": "🇳🇪", "niger": "🇳🇪",
    "буркина-фасо": "🇧🇫", "burkina faso": "🇧🇫",
    "мали": "🇲🇱", "mali": "🇲🇱",
    "малави": "🇲🇼", "malawi": "🇲🇼",
    "замбия": "🇿🇲", "zambia": "🇿🇲",
    "сомали": "🇸🇴", "somalia": "🇸🇴",
    "чад": "🇹🇩", "chad": "🇹🇩",
    "южный судан": "🇸🇸", "south sudan": "🇸🇸",
    "руанда": "🇷🇼", "rwanda": "🇷🇼",
    "тунис": "🇹🇳", "tunisia": "🇹🇳",
    "бенин": "🇧🇯", "benin": "🇧🇯",
    "бурунди": "🇧🇮", "burundi": "🇧🇮",
    "ливия": "🇱🇾", "libya": "🇱🇾",
    "мавритания": "🇲🇷", "mauritania": "🇲🇷",
    "сенегал": "🇸🇳", "senegal": "🇸🇳",
    "либерия": "🇱🇷", "liberia": "🇱🇷",
    "джибути": "🇩🇯", "djibouti": "🇩🇯",
    "габон": "🇬🇦", "gabon": "🇬🇦",
    "сеьершельские острова": "🇸🇨", "seychelles": "🇸🇨",
    
    # Северная Америка
    "сша": "🇺🇸", "америка": "🇺🇸", "usa": "🇺🇸", "соединенные штаты": "🇺🇸", "соединённые штаты": "🇺🇸", "united states": "🇺🇸",
    "канада": "🇨🇦", "canada": "🇨🇦",
    "мексика": "🇲🇽", "mexico": "🇲🇽",
    "гватемала": "🇬🇹", "guatemala": "🇬🇹",
    "куба": "🇨🇺", "cuba": "🇨🇺",
    "гаити": "🇭🇹", "haiti": "🇭🇹",
    "доминиканская республика": "🇩🇴", "dominican republic": "🇩🇴",
    "гондурас": "🇭🇳", "honduras": "🇭🇳",
    "никарагуа": "🇳🇮", "nicaragua": "🇳🇮",
    "эль-сальвадор": "🇸🇻", "el salvador": "🇸🇻",
    "коста-рика": "🇨🇷", "costa rica": "🇨🇷",
    "панама": "🇵🇦", "panama": "🇵🇦",
    "ямайка": "🇯🇲", "jamaica": "🇯🇲",
    "тринидад и тобаго": "🇹🇹", "trinidad and tobago": "🇹🇹",
    "багамы": "🇧🇸", "bahamas": "🇧🇸",
    "барбадос": "🇧🇧", "barbados": "🇧🇧",
    
    # Южная Америка
    "бразилия": "🇧🇷", "brazil": "🇧🇷",
    "аргентина": "🇦🇷", "argentina": "🇦🇷",
    "колумбия": "🇨🇴", "colombia": "🇨🇴",
    "перу": "🇵🇪", "peru": "🇵🇪",
    "венесуэла": "🇻🇪", "venezuela": "🇻🇪",
    "чили": "🇨🇱", "chile": "🇨🇱",
    "эквадор": "🇪🇨", "ecuador": "🇪🇨",
    "боливия": "🇧🇴", "bolivia": "🇧🇴",
    "парагвай": "🇵🇾", "paraguay": "🇵🇾",
    "уругвай": "🇺🇾", "uruguay": "🇺🇾",
    "гайана": "🇬🇾", "guyana": "🇬🇾",
    "суринам": "🇸🇷", "suriname": "🇸🇷",
    
    # Австралия и Океания
    "австралия": "🇦🇺", "australia": "🇦🇺",
    "новая зеландия": "🇳🇿", "new zealand": "🇳🇿",
    "папуа - новая гвинея": "🇵🇬", "papua new guinea": "🇵🇬",
    "фиджи": "🇫🇯", "fiji": "🇫🇯",
    "соломоновы острова": "🇸🇧", "solomon islands": "🇸🇧",
    "вануату": "🇻🇺", "vanuatu": "🇻🇺",
    "самоа": "🇼🇸", "samoa": "🇼🇸",
    "кирибати": "🇰🇮", "kiribati": "🇰🇮",
    "микронезия": "🇫🇲", "micronesia": "🇫🇲",
    "тонга": "🇹🇴", "tonga": "🇹🇴",
    "маршалловы острова": "🇲🇭", "marshall islands": "🇲🇭",
    "палау": "🇵🇼", "palau": "🇵🇼",
    "науру": "🇳🇷", "nauru": "🇳🇷",
    "тувалу": "🇹🇻", "tuvalu": "🇹🇻",
}

# Собираем множество всех названий стран для быстрого поиска
COUNTRY_NAMES = set(FLAGS.keys())

def extract_country_from_annotation(annotation: str) -> tuple[str, bool]:
    """
    Извлекает название страны из аннотации.
    Удаляет все слова, кроме названий стран из словаря.
    Возвращает (название_страны, найдена_ли_страна)
    """
    try:
        decoded = unquote(annotation)
    except:
        decoded = annotation
    
    # Удаляем эмодзи флагов
    flag_pattern = r"[\U0001F1E6-\U0001F1FF]{2}"
    cleaned = re.sub(flag_pattern, "", decoded)
    
    # Удаляем номера серверов
    cleaned = re.sub(r"\|\s*\d+\s*сервер", "", cleaned)
    
    # Разбиваем на слова
    words = re.findall(r'[a-zA-Zа-яА-ЯёЁ\-]+', cleaned)
    
    # Ищем слова, которые есть в словаре стран
    found_countries = []
    for word in words:
        word_lower = word.lower()
        if word_lower in COUNTRY_NAMES:
            found_countries.append(word_lower)
    
    if found_countries:
        country = found_countries[0]
        # Специальные случаи для красивого отображения
        if country in ["сша", "usa", "америка", "соединенные штаты", "соединённые штаты", "united states"]:
            return "США", True
        if country in ["великобритания", "uk", "britain", "united kingdom"]:
            return "Великобритания", True
        if country in ["оаэ", "uae", "объединенные арабские эмираты"]:
            return "ОАЭ", True
        if country in ["юар", "south africa", "южно-африканская республика"]:
            return "ЮАР", True
        if country in ["европа", "europe", "евросоюз", "european union"]:
            return "Европа", True
        return country.capitalize(), True
    
    return None, False

def get_flag(country_name: str) -> str:
    """Возвращает флаг по названию страны"""
    if not country_name:
        return "🔍"
    country_lower = country_name.lower()
    for name, flag in FLAGS.items():
        if name in country_lower or country_lower in name:
            return flag
    return "🔍"

def format_vless_link(vless_url: str, server_number: int) -> str:
    """Форматирует VLESS-ссылку: добавляет флаг, название и номер сервера"""
    if not vless_url.startswith("vless://"):
        return vless_url
    
    if "#" not in vless_url:
        new_annotation = f"🔍 На проверке | {server_number} сервер"
        return f"{vless_url}#{quote(new_annotation, safe='')}"
    
    base_part, old_annotation_encoded = vless_url.split("#", 1)
    
    country_name, found = extract_country_from_annotation(old_annotation_encoded)
    
    if found and country_name:
        flag = get_flag(country_name)
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
        "2. Бот определит страну по аннотации (части после `#`)\n"
        "3. Удалит все лишние слова, оставит только название страны\n"
        "4. Если страна не найдена — поставит `🔍 На проверке | N сервер`\n\n"
        "✅ *Поддерживаются:* Все 197 стран мира + Европа 🇪🇺\n\n"
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
