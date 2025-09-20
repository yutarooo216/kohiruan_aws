from fastapi import FastAPI
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from mangum import Mangum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS設定
origins = [
    "http://localhost:3000",  # Reactの開発用
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエスト定義
class ReservationRequest(BaseModel):
    reserveDate: str
    reserveTime: str
    lastName: str
    firstName: str
    lastNameKn: str
    firstNameKn: str
    email: str
    tel: str  

# グローバルでブラウザ再利用
playwright = None
browser = None

@app.on_event("startup")
def startup_event():
    global playwright, browser
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=True)
    logger.info("ブラウザ起動済み")

@app.on_event("shutdown")
def shutdown_event():
    global browser, playwright
    if browser:
        browser.close()
    if playwright:
        playwright.stop()
    logger.info("ブラウザをシャットダウンしました")

@app.post("/test")
def access_airrsv(request: ReservationRequest):
    page = browser.new_page()
    try:
        # ページロード
        page.goto("https://airrsv.net/kohiruan/calendar", wait_until="domcontentloaded")

        # 日付ヘッダーが出るまで待つ
        page.locator("td.scheduleHeader--day").wait_for(timeout=5000)

        # 日付の形式変換
        dt = datetime.strptime(request.reserveDate, "%Y-%m-%d")
        formatted_date = f"{dt.month}/{dt.day}"

        # 日付インデックス検索
        header_tds = page.query_selector_all("td.scheduleHeader--day")
        target_index = None
        for i, td in enumerate(header_tds):
            span = td.query_selector("span")
            if span and span.inner_text().strip() == formatted_date:
                target_index = i
                break

        if target_index is None:
            return {"error": f"{formatted_date} の日付が見つかりません"}

        # スロット探索
        found = False
        max_retry = 20
        for attempt in range(max_retry):
            body_tds = page.query_selector_all("td.scheduleBodyCell.tdCell")
            if target_index >= len(body_tds):
                page.wait_for_timeout(500)
                continue

            target_td = body_tds[target_index]
            lanes = target_td.query_selector_all("li.dataListItem.js-lane")

            for lane in lanes:
                time_span = lane.query_selector("dt.dataFromTime > span:last-child")
                if time_span and time_span.inner_text().strip() == request.reserveTime:
                    clickable = lane.query_selector("a.dataLinkBox.js-dataLinkBox")
                    if clickable:
                        clickable.click()
                        page.locator("button.btn.is-primary").wait_for(timeout=5000)
                        found = True
                        break
            if found:
                break
            page.wait_for_timeout(500)

        if not found:
            return {"error": f"{formatted_date} {request.reserveTime} の予約枠は見つかりませんでした"}

        # 入力処理
        page.fill('input[name="lastNm"]', request.lastName)
        page.fill('input[name="firstNm"]', request.firstName)
        page.fill('input[name="lastNmKn"]', request.lastNameKn)
        page.fill('input[name="firstNmKn"]', request.firstNameKn)
        page.fill('input[name="mailAddress1"]', request.email)
        page.fill('input[name="mailAddress1ForCnfrm"]', request.email)
        page.fill('input[name="tel1"]', request.tel)

        # 確認へ進む
        page.click("button.btn.is-primary")
        page.locator("button.btn.is-primary#btnBookingComplete").wait_for(timeout=5000)

        # 予約確定
        page.click("button.btn.is-primary#btnBookingComplete")
        page.wait_for_timeout(1000)

        current_url = page.url
        return {"current_url": current_url}

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        return {"error": str(e)}

    finally:
        page.close()

# Lambda用のハンドラー
handler = Mangum(app)