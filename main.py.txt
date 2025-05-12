from fastapi import FastAPI
from playwright.sync_api import sync_playwright
import os
import uvicorn

app = FastAPI()

@app.get("/screenshot")
def screenshot(mountain_name: str, url: str):
    filename = f"{mountain_name}.png"
    output_path = os.path.join("screenshots", filename)
    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector("img[src*='tozan']", timeout=10000)
        page.screenshot(path=output_path, full_page=True)
        browser.close()

    return {"status": "success", "file_path": output_path}
