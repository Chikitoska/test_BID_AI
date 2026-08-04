"""Общие локаторы лендинга BID для Selenium и Playwright."""

BASE_URL = "https://bid.gazprom-neft.ru/"
PAGE_TITLE = "Газпром Бизнес ID"

# XPath / CSS — используются в Selenium и как fallback в Playwright
LOGIN_LINK = "//a[contains(@href, 'self-authentication')]"
LOGIN_BUTTON = "//button[contains(., 'Войти')]"
GET_ID_LINK = "//a[contains(@href, 'registration')]"
INN_INPUT = "//input[@placeholder='Введите ИНН' or @aria-label='Введите ИНН']"
ADD_INN_BUTTON = "//button[contains(., 'Добавить')]"
SUBMIT_REQUEST = "//button[contains(., 'Отправить запрос')]"

NAV_TABS = [
    "Потребителям",
    "Поддержка бизнеса",
    "Другие сервисы",
    "Отраслевые сервисы",
    "Поставщикам",
    "B2B Маркетплейс",
]

CONTACT_FIELDS = {
    "name": "Как к Вам обращаться?",
    "email": "Ваш E-mail",
    "phone": "+7 (999) 999-99-99",
    "inn": "ИНН Контрагента",
}

TEST_INN = "7707083893"
