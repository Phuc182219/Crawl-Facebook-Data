import configuration as cf
from time import time, sleep
import os
import json
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

PROGRESS_FILE = "progress.json"
MAX_RETRIES = 3
WAIT_TIMEOUT = 30

def load_progress(page_name):
    try:
        with open(f"data/{page_name}/{PROGRESS_FILE}", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"completed": [], "failed": []}

def save_progress(page_name, progress):
    with open(f"data/{page_name}/{PROGRESS_FILE}", "w") as f:
        json.dump(progress, f)

def crawl_post(browser, browser_mobile, url, folder, progress, page_name):
    id = cf.extract_facebook_post_id(url)
    if id in progress["completed"]:
        return

    for attempt in range(MAX_RETRIES):
        try:
            if "posts" in url:
                # Xử lý bài post thường
                browser.get(url)
                WebDriverWait(browser, WAIT_TIMEOUT).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@role="article"]'))
                )

                # Lấy caption
                captions = cf.get_captions_emojis(browser)
                cf.save_text(captions, f"{folder}/caption.txt")

                # Lấy comments
                comments = cf.get_comments(browser)
                cf.save_text(comments, f"{folder}/comments.txt")

                # Tải ảnh
                img_urls = cf.get_image_urls(browser)
                cf.download_images(img_urls, folder)

            elif "videos" in url or "reel" in url:
                # Xử lý video và reel
                browser.get(url)
                
                # Chờ element video load
                WebDriverWait(browser, WAIT_TIMEOUT).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@data-video-id]'))
                )

                # Xử lý caption
                captions = cf.get_captions_spe(browser) if "videos" in url else cf.get_captions_reel(browser)
                cf.save_text(captions, f"{folder}/caption.txt")

                # Xử lý comments với retry
                try:
                    if "reel" in url:
                        WebDriverWait(browser, WAIT_TIMEOUT).until(
                            EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Comment"]'))
                        ).click()
                    
                    # Load tất cả comments
                    while True:
                        try:
                            cf.click_view_more_comments(browser)
                            sleep(1)
                        except Exception:
                            break
                except TimeoutException:
                    pass

                comments = cf.get_comments(browser)
                cf.save_text(comments, f"{folder}/comments.txt")

                # Tải video từ mobile
                try:
                    browser_mobile.get(url)
                    WebDriverWait(browser_mobile, WAIT_TIMEOUT).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'video'))
                    )
                    video_urls = cf.get_video_urls(browser_mobile)
                    cf.download_videos(video_urls, folder)
                except Exception as e:
                    print(f"Error downloading video: {str(e)}")

            # Đánh dấu hoàn thành
            progress["completed"].append(id)
            save_progress(page_name, progress)
            return

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Attempt {attempt + 1} failed for {url}: {str(e)}")
            if attempt == MAX_RETRIES - 1:
                progress["failed"].append(id)
                save_progress(page_name, progress)
            browser.refresh()
            sleep(8)

def crawl(driver, cookies_path, page_link, page_name):
    # Khởi tạo trình duyệt
    browser = cf.login(driver, cookies_path)
    browser_mobile = cf.login_mobile(driver, cookies_path)

    # Tạo thư mục và load tiến trình
    os.makedirs(f"data/{page_name}", exist_ok=True)
    progress = load_progress(page_name)

    # Lấy danh sách post và lọc những post đã hoàn thành
    post_urls = [url for url in cf.get_post_links(browser, page_link) 
                if cf.extract_facebook_post_id(url) not in progress["completed"]]

    # Xử lý từng post
    for url in tqdm(post_urls, desc="Processing Posts"):
        id = cf.extract_facebook_post_id(url)
        folder = f"data/{page_name}/{id}"
        os.makedirs(folder, exist_ok=True)
        
        crawl_post(browser, browser_mobile, url, folder, progress, page_name)

    # In thống kê
    print(f"\nCompleted: {len(progress['completed'])} posts")
    print(f"Failed: {len(progress['failed'])} posts")

if __name__ == "__main__":
    driver_path = r"D:\Crawl_Facebook\Crawl-Facebook-Data\chromedriver.exe"
    cookies_path = "my_cookies.pkl"
    page_link = "https://www.facebook.com/VietCreditOfficial"
    page_name = "VietCredit"

    start_time = time()
    crawl(driver_path, cookies_path, page_link, page_name)
    print(f"Total time: {(time() - start_time)/60:.2f} minutes")