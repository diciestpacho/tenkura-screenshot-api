from fastapi import FastAPI
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright
import os
import base64

app = FastAPI()

# Health check
@app.get("/")
def root():
    return {"message": "hello"}

@app.get("/screenshot")
def screenshot(mountain_name: str, url: str):
    filename = f"{mountain_name}.png"
    output_path = os.path.join("screenshots", filename)
    os.makedirs("screenshots", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # 🔍 headful browser (not headless)
        context = browser.new_context(locale="ja-JP")  # 🌏 set Japanese locale

        # 🧠 Pretend to be a Japanese Chrome browser
        context.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Referer": "https://tenkura.n-kishou.co.jp/",
            "Accept-Language": "ja,en-US;q=0.9,en;q=0.8"
        })

        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(5000)  # ⏳ wait 5 seconds for JS to load

        try:
            page.wait_for_selector("img[src*='tozan']", timeout=30000)
        except:
            print("⚠️ Warning: 登山指数 image not found, capturing page anyway.")

        page.screenshot(path=output_path, full_page=True)
        browser.close()

    with open(output_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return JSONResponse(content={
        "status": "success",
        "mountain_name": mountain_name,
        "image_base64": encoded
    })
