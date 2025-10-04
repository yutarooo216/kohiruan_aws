from fastapi import FastAPI
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 許可するオリジン（ReactのURL）
origins = [
    "http://localhost:3000",  # Reactのデフォルト開発サーバーURL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストボディの定義
class ReservationRequest(BaseModel):
    reserveDate: str
    reserveTime: str
    lastName: str
    firstName: str
    lastNameKn: str
    firstNameKn: str
    email: str
    tel: str  

@app.post("/test")
def access_airrsv(request: ReservationRequest):
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto("https://airrsv.net/kohiruan/calendar")
            page.wait_for_load_state("domcontentloaded")
            page.wait_for_timeout(1000)

            # ヘッダーから日付のindexを取得
            header_tds = page.query_selector_all("td.scheduleHeader--day")
            target_index = None
            dt = datetime.strptime(request.reserveDate, "%Y-%m-%d")
            request.reserveDate = f"{dt.month}/{dt.day}"
            for i, td in enumerate(header_tds):
                span = td.query_selector("span")
                if not span:
                    continue
                if span.inner_text().strip() == request.reserveDate:
                    target_index = i
                    break

            if target_index is None:
                browser.close()
                return {"error": f"{request.reserveDate} の日付が見つかりません"}

            # 監視ループ開始
            max_retry = 60
            interval_sec = 1

            for attempt in range(max_retry):
                body_tds = page.query_selector_all("td.scheduleBodyCell.tdCell")
                if target_index >= len(body_tds):
                    page.wait_for_timeout(interval_sec * 1000)
                    continue

                target_td = body_tds[target_index]
                lanes = target_td.query_selector_all("li.dataListItem.js-lane")
                found = False

                for lane in lanes:
                    time_span = lane.query_selector("dt.dataFromTime > span:last-child")
                    if time_span is None:
                        continue
                    if time_span.inner_text().strip() == request.reserveTime:
                        clickable = lane.query_selector("a.dataLinkBox.js-dataLinkBox")
                        if clickable:
                            clickable.click()
                            page.wait_for_load_state("domcontentloaded")
                            found = True
                            break

                if found:
                    reserve_button = page.query_selector("button.btn.is-primary")
                    if reserve_button:
                        try:
                            reserve_button.click()
                            page.wait_for_load_state("domcontentloaded")
                            break
                        except Exception as e:
                            print(f"クリック時に例外発生: {e}")
                            page.goto("https://airrsv.net/kohiruan/calendar")
                            page.wait_for_load_state("domcontentloaded")
                            page.wait_for_timeout(100)
                    else:
                        print("予約ボタンが見つかりませんでした")
                        page.goto("https://airrsv.net/kohiruan/calendar")
                        page.wait_for_load_state("domcontentloaded")
                        page.wait_for_timeout(100)

                else:
                    page.wait_for_timeout(interval_sec * 1000)

            if not found:
                browser.close()
                return {"error": f"{request.reserveDate} {request.reserveTime} の予約枠は見つかりませんでした"}

            # 入力部分
            page.fill('input[name="lastNm"]', request.lastName)
            page.fill('input[name="firstNm"]', request.firstName)
            page.fill('input[name="lastNmKn"]', request.lastNameKn)
            page.fill('input[name="firstNmKn"]', request.firstNameKn)
            page.fill('input[name="mailAddress1"]', request.email)
            page.fill('input[name="mailAddress1ForCnfrm"]', request.email)
            page.fill('input[name="tel1"]', request.tel)

            # クリック
            button = page.query_selector("button.btn.is-primary")
            if button:
                button.click()
                page.wait_for_load_state("domcontentloaded")
            else:
                print("確認へ進むボタンが見つかりませんでした")

            confirm_button = page.query_selector("button.btn.is-primary#btnBookingComplete")
            if confirm_button:
                try:
                    confirm_button.click()
                    page.wait_for_load_state("domcontentloaded")
                    print("予約確定ボタンをクリックしました")
                except Exception as e:
                    print(f"予約確定ボタンのクリック時に例外発生: {e}")
            else:
                print("予約確定ボタンが見つかりませんでした")

            current_url = page.url
            print(current_url)

            html_content = page.content()
            with open("page_content.html", "w", encoding="utf-8") as file:
                file.write(html_content)

            browser.close()
            return {"current_url": current_url}
    
        except Exception as e:
            logger.error(f"エラーが発生しました: {e}")
            return {"error": str(e)}
        
        finally:
            browser.close()
