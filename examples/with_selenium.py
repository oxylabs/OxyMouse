import random
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from oxymouse.mouse.bezier_mouse.bezier_mouse import BezierMouse


def generate_random_movements() -> list[tuple[int, int]]:
    # Mouse can be BezierMouse, PerlinMouse or GaussianMouse
    bezier_mouse = BezierMouse()
    movements = bezier_mouse.generate_coordinates()
    return movements


def move_mouse_smoothly(driver, movements: list[tuple[int, int]]):
    actions = ActionChains(driver)
    for x, y in movements:
        actions.move_by_offset(x, y)
        actions.pause(random.uniform(0.001, 0.003))  # Add small random delays
    actions.perform()


driver = webdriver.Chrome()

try:
    # Open example.com
    driver.get("https://oxylabs.io")

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    movements = generate_random_movements()

    move_mouse_smoothly(driver, movements)

    time.sleep(5)

finally:
    # Close the browser
    driver.quit()
