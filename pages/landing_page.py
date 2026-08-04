"""Page Object лендинга https://bid.gazprom-neft.ru/"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import BASE_URL, PAGE_TITLE


class LandingPage:
    URL = BASE_URL
    TITLE = PAGE_TITLE

    # Локаторы (публичная часть, без клика «Войти»)
    LOGIN_LINK = (By.XPATH, "//a[contains(@href, 'self-authentication')]")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(., 'Войти')]")
    GET_ID_LINK = (By.XPATH, "//a[contains(@href, 'registration')]")
    INN_INPUT = (By.XPATH, "//input[@placeholder='Введите ИНН' or @aria-label='Введите ИНН']")
    ADD_INN_BUTTON = (By.XPATH, "//button[contains(., 'Добавить')]")
    NON_RESIDENT_CHECKBOX = (By.XPATH, "//*[contains(text(), 'Нерезидент')]")
    BRANCH_CHECKBOX = (By.XPATH, "//*[contains(text(), 'Представительство/Филиал')]")

    NAV_TABS = {
        "Потребителям": (By.XPATH, "//*[contains(normalize-space(.), 'Потребителям')]"),
        "Поддержка бизнеса": (By.XPATH, "//*[contains(normalize-space(.), 'Поддержка бизнеса')]"),
        "Другие сервисы": (By.XPATH, "//*[contains(normalize-space(.), 'Другие сервисы')]"),
        "Отраслевые сервисы": (By.XPATH, "//*[contains(normalize-space(.), 'Отраслевые сервисы')]"),
        "Поставщикам": (By.XPATH, "//*[contains(normalize-space(.), 'Поставщикам')]"),
        "B2B Маркетплейс": (By.XPATH, "//*[contains(normalize-space(.), 'B2B Маркетплейс')]"),
    }

    CONTACT_NAME = (By.XPATH, "//input[@placeholder='Как к Вам обращаться?']")
    CONTACT_EMAIL = (By.XPATH, "//input[@placeholder='Ваш E-mail']")
    CONTACT_PHONE = (By.XPATH, "//input[@placeholder='+7 (999) 999-99-99']")
    CONTACT_INN = (By.XPATH, "//input[@placeholder='ИНН Контрагента']")
    CONTACT_QUESTION = (By.XPATH, "//input[@placeholder='Ваш вопрос' or @textarea]")
    SUBMIT_REQUEST = (By.XPATH, "//button[contains(., 'Отправить запрос')]")

    def __init__(self, driver: WebDriver, timeout: int = 30):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self) -> "LandingPage":
        self.driver.get(self.URL)
        self.wait.until(lambda d: d.title == self.TITLE)
        self.wait.until(EC.presence_of_element_located(self.LOGIN_LINK))
        # SPA подгружает блок сервисов асинхронно
        self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(., 'Потребителям')]")
            )
        )
        return self

    def wait_visible(self, locator: tuple[str, str]):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        return element

    def wait_present(self, locator: tuple[str, str]):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click_tab(self, tab_name: str) -> None:
        locator = self.NAV_TABS[tab_name]
        tab = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", tab
        )
        self.driver.execute_script("arguments[0].click();", tab)

    def get_static_asset_urls(self) -> list[str]:
        """JS/CSS с текущей страницы."""
        script = """
        const urls = new Set();
        document.querySelectorAll('script[src], link[rel=\"stylesheet\"]').forEach(el => {
            const src = el.src || el.href;
            if (src) urls.add(src);
        });
        return Array.from(urls);
        """
        return self.driver.execute_script(script)
