import os
import time
import re
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CONFIGURATION ---
TARGET_URL_OR_ID = os.environ.get('STREAM_ID', 'https://www.youtube.com/live/WoUkZu-m7iY')
WATCH_TIME_SECONDS = 20400 # 5 Hours 40 Minutes
# ---------------------

def get_clean_id(input_val):
    video_id_match = re.search(r"(?:v=|\/|live\/)([0-9A-Za-z_-]{11})", input_val)
    if video_id_match:
        return video_id_match.group(1)
    return input_val

def get_free_proxies():
    """Internet se free HTTPS proxies ki list nikalta hai."""
    print("Fetching free proxies...")
    url = "https://free-proxy-list.net/"
    try:
        response = requests.get(url)
        proxies = re.findall(r"\d+\.\d+\.\d+\.\d+:\d+", response.text)
        return proxies
    except Exception as e:
        print(f"Error fetching proxies: {e}")
        return []

def test_proxy(proxy, video_id):
    """Proxy ko check karta hai ki wo YouTube load kar pa rahi hai ya nahi."""
    print(f"Testing proxy: {proxy}...", end=" ")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f'--proxy-server=http://{proxy}')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(30) # 30s timeout agar proxy slow ho

    try:
        # Pura URL banane ke liye sirf ID use karein taaki parsing error na ho
        driver.get(f"https://www.youtube.com/watch?v={video_id}")
        # Check karein agar page title mein YouTube hai (yani load ho gaya)
        if "YouTube" in driver.title:
            print("WORKING!")
            return True
        else:
            print("Failed (No YouTube title).")
            return False
    except Exception as e:
        print(f"Failed (Timeout/Error).")
        return False
    finally:
        driver.quit()

def start_watching(proxy, video_id):
    """Mukhya watching function working proxy ke saath."""
    stream_url = f"https://www.youtube.com/watch?v={video_id}"
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--mute-audio")
    options.add_argument(f'--proxy-server=http://{proxy}')
    # Real user browser lagne ke liye User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 20)

    print(f"[{os.environ.get('VIEWER_ID', 'Viewer')}] Opening Stream with Proxy {proxy}: {stream_url}")
    
    try:
        driver.get(stream_url)
        time.sleep(5) # Page load hone dein

        # --- TRICKS FOR HIGH RETENTION ---

        # 1. Play Button Click (Headless auto-play bypass)
        try:
            play_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-large-play-button")))
            play_button.click()
            print("Clicking Play Button...")
        except:
            print("Play Button not found (Maybe already playing).")

        # 2. Set Quality to Lowest (Data Saver + No buffering)
        driver.execute_script("document.getElementsByTagName('video')[0].playbackRate = 1.0;")
        try:
             # Settings gear icon par click
            settings_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".ytp-settings-button")))
            settings_button.click()
            time.sleep(1)
            # Quality option select (Last element standard YouTube menu mein)
            quality_option = driver.find_elements(By.CSS_SELECTOR, ".ytp-panel-menu .ytp-menuitem")[-1]
            quality_option.click()
            time.sleep(1)
            # Sabse lowest quality (144p) select
            lowest_quality = driver.find_elements(By.CSS_SELECTOR, ".ytp-quality-menu .ytp-menuitem")[0]
            lowest_quality.click()
            print("Set video quality to lowest.")
        except Exception as e:
            print(f"Could not set low quality: {e}")

        # 3. Random Human Interactions (Scroll)
        driver.execute_script("window.scrollTo(0, 400);")
        print("Human Interaction simulated (Scrolling).")

        # --- FINAL WATCH LOOP ---
        print(f"Watching started for {WATCH_TIME_SECONDS / 60} minutes.")
        start_time = time.time()
        while time.time() - start_time < WATCH_TIME_SECONDS:
             # Har 30 min mein thoda scroll karke activity dikhayein
            time.sleep(1800)
            driver.execute_script(f"window.scrollTo(0, {random.randint(100, 700)});")
            print("Periodic scroll interaction.")
            
    except Exception as e:
        print(f"Error during watching: {e}")
    finally:
        print("Closing browser.")
        driver.quit()

if __name__ == "__main__":
    video_id = get_clean_id(TARGET_URL_OR_ID)
    
    proxies = get_free_proxies()
    # Randomize list taaki har job alag proxy check kare
    random.shuffle(proxies) 

    working_proxy = None
    # Pehli working proxy dhundhein (Top 10 proxies check karein speed ke liye)
    for p in proxies[:10]:
        if test_proxy(p, video_id):
            working_proxy = p
            break
    
    if working_proxy:
        start_watching(working_proxy, video_id)
    else:
        print("No working free proxies found from the list.")
    
