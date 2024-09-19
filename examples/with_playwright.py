import asyncio
import random

from playwright.async_api import async_playwright

from oxymouse.mouse.bezier_mouse.bezier_mouse import BezierMouse


async def generate_random_movements() -> list[tuple[int, int]]:
    # Mouse can be BezierMouse, PerlinMouse or GaussianMouse
    bezier_mouse = BezierMouse()
    movements = bezier_mouse.generate_coordinates()
    return movements


async def move_mouse_smoothly(page, movements: list[tuple[int, int]]):
    for x, y in movements:
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.001, 0.003))  # Add small random delays


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # Open example.com
            await page.goto("https://oxylabs.io", wait_until="domcontentloaded")

            movements = await generate_random_movements()

            await move_mouse_smoothly(page, movements)

            await asyncio.sleep(5)

        finally:
            await browser.close()


asyncio.run(main())
