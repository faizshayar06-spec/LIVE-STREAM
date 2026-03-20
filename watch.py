import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_clean_url(input_val):
    # Ye function aapke bade link se 11-digit ID nikal lega
    video_id_match = re.search(r"(?:v=|\/|live\/)([0-9A-Za-z_-]{11})", input_val)
    if video_id_match:
        return f"https://www.youtube.com/watch?v={video_id_match.group(1)}"
    return input_val

def start_watching():
    # GitHub Secret se Link uthayega
    raw_input = os.environ.get('STREAM_ID', 'https://www.youtube.com/live/WoUkZu-m7iY')
    stream_url = get_clean_url(raw_input)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--mute-audio")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    print(f"Opening Stream: {stream_url}")
    try:
        driver.get(stream_url)
        # 5 Ghante 40 Minute = 20400 seconds
        time.sleep(20400) 
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_watching()
    
