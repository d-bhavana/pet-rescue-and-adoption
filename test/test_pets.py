import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    options = Options()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=options
    )

    yield driver
    driver.quit()


def test_home_page_loads_with_stats(driver):
    driver.get("http://localhost:5001/")

    assert "Pet Rescue" in driver.page_source

    page = driver.page_source

    assert "Total" in page
    assert "Available" in page
    assert "Adopted" in page


def test_add_pet_and_view(driver):
    driver.get("http://localhost:5001/add")

    driver.find_element(By.NAME, "name").send_keys(
        "Selenium Test Pet"
    )
    driver.find_element(By.NAME, "type").send_keys(
        "Dog"
    )

    driver.find_element(By.TAG_NAME, "button").click()

    time.sleep(1)

    assert "/pets" in driver.current_url
    assert "Selenium Test Pet" in driver.page_source
    assert "Dog" in driver.page_source
