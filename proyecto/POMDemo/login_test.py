import pytest
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from POMDemo.login_page import LoginPage


@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(15)
    yield driver
    driver.close()
    driver.quit()


def test_login(driver):
    login_page = LoginPage(driver)
    login_page.open_page("https://trytestingthis.netlify.app/")
    time.sleep(5)
    login_page.enter_username("test")
    time.sleep(5)
    login_page.enter_password("test")
    time.sleep(5)
    login_page.click_login()
    #
    # driver.get("https://trytestingthis.netlify.app/")
    # username_field = driver.find_element(By.ID, "uname")
    # password_field = driver.find_element(By.ID, "pwd")
    # submit_button = driver.find_element(By.XPATH, "//input[@value='Login']")
    #
    # username_field.send_keys('test')
    # password_field.send_keys('test')
    # time.sleep(10)
    # submit_button.click()
    assert "Successful" in driver.page_source
    time.sleep(5)
