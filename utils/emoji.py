"""
Поддержка кастомных эмодзи Telegram Premium.

Кастомный эмодзи в HTML выглядит так:
    <tg-emoji emoji-id="5368324170671202286">⭐</tg-emoji>
где emoji-id — числовой ID конкретного premium-эмодзи, а символ внутри тега —
обычный emoji-фолбэк для тех, у кого нет Telegram Premium (или для ботов без
разрешения показывать custom emoji).

Как узнать emoji-id: перешли нужный кастомный эмодзи любому боту вроде
@like_id_bot / @EmojiIdBot (или можно получить через getCustomEmojiStickers /
разбор entities входящего сообщения с этим эмодзи).

ВАЖНО: сообщения с <tg-emoji> нужно отправлять с parse_mode="HTML".
Если id не задан (None или пустая строка) — используется обычный emoji без тега,
бот не сломается, просто без "премиум" вида.
"""

# Заполни реальными ID своих кастомных эмодзи (или оставь None — будет обычный emoji)
CUSTOM_EMOJI_IDS: dict[str, str | None] = {
    "welcome": "5222108309795908493",   #✨
    "star": "5951810621887484519",     # ⭐
    "gift_star": "5453969572354878595", #⭐
    "admin": "5219943216781995020",       # 🛠
    "stats": "5219943216781995020",       # 📊
    "money": "5219943216781995020",       # 💰
    "broadcast": "5219943216781995020",   # 💬
    "markup": "5219943216781995020",      # 💲
    "support": "5258023599419171861",     # 🆘
    "cross": "5219943216781995020",       # ❌
    "hourglass": "5219943216781995020",   # ⏳
    "sparkle": "5219943216781995020",     # 🎆
    "zap": "5219943216781995020",         # ⚡️
    "gift": "6032644646587338669",        # 🎁
    "back": "6039539366177541657",        # ⬅️
    "premium": "5773677501825945508",     # 💎
    "profile": "6032994772321309200",     # 👤
    "self": "6032693626394382504",  # 👤
    "schet": "5393302369024882368",
    "polychatel": "6033108709213736873",
    "check": "5769126056262898415",
    "dollar": "5283232570660634549",


}

_FALLBACK = {
    "welcome": "✨",
    "star": "⭐",
    "gift_star": "⭐", #⭐
    "admin": "🛠",
    "stats": "📊",
    "money": "💰",
    "broadcast": "💬",
    "markup": "💲",
    "support": "🆘",
    "cross": "❌",
    "hourglass": "⏳",
    "sparkle": "🎆",
    "zap": "⚡️",
    "gift": "🎁",
    "back": "⬅️",
    "premium": "💎",
    "profile": "👤",
    "self": "👤",
    "schet": "👤",
    "polychatel": "👤",
    "znak": "❗️",
    "check": "✅",
    "dollar": "✅",
}


def emoji(name: str) -> str:
    """Возвращает HTML-фрагмент с кастомным эмодзи (если задан id) или обычный emoji.
    Использовать ТОЛЬКО в тексте сообщений (parse_mode="HTML"), не в кнопках."""
    fallback = _FALLBACK.get(name, "")
    custom_id = CUSTOM_EMOJI_IDS.get(name)
    if custom_id:
        return f'<tg-emoji emoji-id="{custom_id}">{fallback}</tg-emoji>'
    return fallback


def plain(name: str) -> str:
    """Обычный emoji без HTML-тега — для текста кнопки (fallback, если icon_custom_emoji_id не поддержится)."""
    return _FALLBACK.get(name, "")


def emoji_id(name: str) -> str | None:
    """Сырой ID кастомного эмодзи для параметра icon_custom_emoji_id у кнопок (Bot API 9.4+).
    Требует, чтобы у владельца бота была активна Telegram Premium (либо бот купил
    доп. юзернеймы на Fragment) — иначе Telegram проигнорирует иконку и покажет только текст."""
    return CUSTOM_EMOJI_IDS.get(name)
