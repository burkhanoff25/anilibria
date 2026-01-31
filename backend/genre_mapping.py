"""
Genre name to filename mapping for custom genre images
"""

# Mapping from Russian genre names to image filenames
GENRE_IMAGE_MAP = {
    "Боевые искусства": "martial-arts",
    "Вампиры": "vampires",
    "Гарем": "harem",
    "Демоны": "demons",
    "Детектив": "detective",
    "Дзёсей": "josei",
    "Драма": "drama",
    "Игры": "games",
    "Исекай": "isekai",
    "Исторический": "historical",
    "Киберпанк": "cyberpunk",
    "Комедия": "comedy",
    "Магия": "magic",
    "Меха": "mecha",
    "Мистика": "mystery",
    "Музыка": "music",
    "Пародия": "parody",
    "Повседневность": "slice-of-life",
    "Приключения": "adventure",
    "Психологическое": "psychological",
    "Романтика": "romance",
    "Сверхъестественное": "supernatural",
    "Сёдзе": "shoujo",
    "Сёдзе-ай": "shoujo-ai",
    "Сейнен": "seinen",
    "Сёнен": "shonen",
    "Спорт": "sports",
    "Супер сила": "superpower",
    "Триллер": "thriller",
    "Ужасы": "horror",
    "Фантастика": "sci-fi",
    "Фэнтези": "fantasy",
    "Школа": "school",
    "Экшен": "action",
    "Этти": "ecchi",
}

# Mapping from genre IDs to Russian names
GENRE_ID_MAP = {
    15: "Боевые искусства",
    24: "Вампиры",
    32: "Гарем",
    16: "Демоны",
    25: "Детектив",
    33: "Дзёсей",
    8: "Драма",
    17: "Игры",
    34: "Исекай",
    26: "Исторический",
    30: "Киберпанк",
    1: "Комедия",
    18: "Магия",
    2: "Меха",
    9: "Мистика",
    19: "Музыка",
    36: "Пародия",
    10: "Повседневность",
    27: "Приключения",
    3: "Психологическое",
    11: "Романтика",
    28: "Сверхъестественное",
    20: "Сёдзе",
    31: "Сёдзе-ай",
    5: "Сейнен",
    4: "Сёнен",
    12: "Спорт",
    21: "Супер сила",
    6: "Триллер",
    13: "Ужасы",
    22: "Фантастика",
    29: "Фэнтези",
    7: "Школа",
    14: "Экшен",
    23: "Этти",
}

# Alternative genre name variations
GENRE_ALIASES = {
    "Боевые Искусства": "martial-arts",
    "боевые искусства": "martial-arts",
    "Вампир": "vampires",
    "вампиры": "vampires",
    "Детективы": "detective",
    "детектив": "detective",
    "Dзёсей": "josei",
    "джосей": "josei",
    "драма": "drama",
    "игра": "games",
    "игры": "games",
    "исекай": "isekai",
    "исторический": "historical",
    "История": "historical",
    "киберпанк": "cyberpunk",
    "комедия": "comedy",
    "Магическая": "magic",
    "магия": "magic",
    "меха": "mecha",
    "мистика": "mystery",
    "музыка": "music",
    "пародия": "parody",
    "повседневность": "slice-of-life",
    "Slice of Life": "slice-of-life",
    "приключения": "adventure",
    "психологическое": "psychological",
    "Психология": "psychological",
    "романтика": "romance",
    "Romance": "romance",
    "сверхъестественное": "supernatural",
    "сёдзе": "shoujo",
    "Shoujo": "shoujo",
    "сёдзе-ай": "shoujo-ai",
    "Shoujo-ai": "shoujo-ai",
    "Yuri": "shoujo-ai",
    "сейнен": "seinen",
    "Seinen": "seinen",
    "сёнен": "shonen",
    "Shonen": "shonen",
    "Shounen": "shonen",
    "спорт": "sports",
    "Sports": "sports",
    "супер сила": "superpower",
    "Суперсила": "superpower",
    "триллер": "thriller",
    "ужасы": "horror",
    "Horror": "horror",
    "фантастика": "sci-fi",
    "Sci-Fi": "sci-fi",
    "фэнтези": "fantasy",
    "Fantasy": "fantasy",
    "школа": "school",
    "School": "school",
    "экшен": "action",
    "Action": "action",
    "этти": "ecchi",
    "Ecchi": "ecchi",
}

def get_genre_image_filename(genre_name: str) -> str:
    """
    Get the image filename for a genre name
    
    Args:
        genre_name: Genre name in Russian or English
        
    Returns:
        Image filename without extension (e.g., "martial-arts")
    """
    # Try exact match first
    if genre_name in GENRE_IMAGE_MAP:
        return GENRE_IMAGE_MAP[genre_name]
    
    # Try aliases
    if genre_name in GENRE_ALIASES:
        return GENRE_ALIASES[genre_name]
    
    # Return lowercase slugified version as fallback
    return genre_name.lower().replace(" ", "-").replace("ё", "e")


def get_genre_name_by_id(genre_id: int) -> str:
    """
    Get Russian genre name by ID.

    Args:
        genre_id: Genre ID

    Returns:
        Russian genre name or empty string
    """
    return GENRE_ID_MAP.get(int(genre_id), "")
