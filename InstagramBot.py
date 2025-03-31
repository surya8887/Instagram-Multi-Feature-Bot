import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class InstagramBot:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=930,820")
        self.driver = uc.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, email, password):
        self.driver.get("https://www.instagram.com/")
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        username_field.send_keys(email)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(5)

    def scrape_hashtag_posts(self, hashtag):
        self.driver.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(8)
        most_recent = self.driver.find_element(
            By.XPATH, '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/article/div[2]/div'
        )
        posts = most_recent.find_elements(By.TAG_NAME, "a")
        return [post.get_attribute("href") for post in posts]

    def scrape_usernames(self, links):
        usernames = set()
        for link in links:
            self.driver.get(link)
            time.sleep(3)
            username_element = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/div[1]/header/div[2]/div[1]/div[1]/div/div/span/div/div/a')
                )
            )
            usernames.add(username_element.text)
        return list(usernames)

    def send_dm(self, usernames, message, delay_time):
        self.driver.get("https://www.instagram.com/direct/inbox/")
        time.sleep(3)
        try:
            notification_popup = self.driver.find_element(
                By.XPATH, '//div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'
            )
            if notification_popup.is_displayed():
                notification_popup.click()
                time.sleep(2)
        except Exception:
            pass

        for username in usernames:
            new_message_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div/div')
                )
            )
            new_message_button.click()
            time.sleep(2)

            recipient_input = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/input')
                )
            )
            recipient_input.send_keys(username)
            time.sleep(1)
            recipient_input.send_keys(Keys.ENTER)
            time.sleep(1)

            select_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div')
                )
            )
            select_button.click()
            time.sleep(2)

            next_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div/div/div[3]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div[1]/div/div[4]/div')
                )
            )
            next_button.click()
            time.sleep(3)

            ActionChains(self.driver).send_keys(message).send_keys(Keys.RETURN).perform()
            time.sleep(delay_time)
        self.driver.quit()

    def comment_on_posts(self, links, comment, delay_time):
        for link in links:
            self.driver.get(link)
            time.sleep(2)
            comment_input = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'textarea[aria-label="Add a comment…"]'))
            )
            comment_input.click()
            time.sleep(1)
            ActionChains(self.driver).send_keys(comment).send_keys(Keys.RETURN).perform()
            time.sleep(delay_time)
        self.driver.quit()
