PIZZA_NAME_MAPPING: dict[str, str] = {
    "margherita": "Маргарита",
    "pepperoni": "Пепперони",
    "quatro_stagioni": "Четыре сыра",
    "capricciosa": "Капричоза",
    "diavola": "Дьявола",
    "prosciutto": "Прошутто",
}

PIZZA_SIZE_MAPPING: dict[str, str] = {
    "small": "Маленькая (25см)",
    "medium": "Средняя (30см)",
    "large": "Большая (35см)",
    "xl": "Очень большая (40см)",
}

DRINKS_MAPPING: dict[str, str] = {
    "coca_cola": "Coca-Cola",
    "fanta": "Fanta",
    "pepsi": "Pepsi",
    "7-up": "7-Up",
    "water": "Вода",
    "none": "Без напитка",
}


PIZZA_BASE_PRICES: dict[str, int] = {
    "Маргарита": 1,
    "Пепперони": 1,
    "Четыре сыра": 1,
    "Дьявола": 1,
    "Прошутто": 1,
    "Капричоза": 1,
}

PIZZA_SIZE_PRICES: dict[str, int] = {
    "Маленькая (25см)": 1,
    "Средняя (30см)": 1,
    "Большая (35см)": 1,
    "Очень большая (40см)": 1,
}

# Фиксированная доплата за напиток
DRINK_FIXED_PRICE = 2
