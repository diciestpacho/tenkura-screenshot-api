from fastapi import FastAPI
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright
import os
import base64

app = FastAPI()

# ✅ Keeps the app alive by responding to "/"
@app.get("/")
def root():
    return {"message": "hello"}

# ✅ Takes a screenshot of the given TenKura page
@app.get("/screenshot")
def screenshot(mountain_name: str, url: str):
    filename = f"{mountain_name}.png"
    output_path = os.path.join("screenshots", filename)
    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_selector("img[src*='tozan']", timeout=30000)
        page.screenshot(path=output_path, full_page=True)
        browser.close()

    # Read and encode image to base64
    with open(output_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return JSONResponse(content={
        "status": "success",
        "mountain_name": mountain_name,
        "image_base64": encoded
    })
