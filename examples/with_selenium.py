import random
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from oxymouse import OxyMouse


def generate_random_movements() -> list[tuple[int, int]]:
    mouse = OxyMouse(algorithm="perlin")
    movements = mouse.generate_coordinates()
    return movements


def move_mouse_smoothly(driver, movements: list[tuple[int, int]]):
    actions = ActionChains(driver)
    prev_x, prev_y = movements[0]
    for x, y in movements[1:]:
        dx = x - prev_x
        dy = y - prev_y
        actions.move_by_offset(dx, dy)
        actions.pause(random.uniform(0.0001, 0.0003))
        prev_x, prev_y = x, y
    actions.perform()


driver = webdriver.Chrome()

try:
    driver.get("https://oxylabs.io")

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    movements = generate_random_movements()

    move_mouse_smoothly(driver, movements)

    time.sleep(5)

finally:
    driver.quit()
