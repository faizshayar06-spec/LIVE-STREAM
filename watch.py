import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def start_watching():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--mute-audio")
    # Real user dikhne ke liye User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Yahan apni Live Stream ka URL dalein
    stream_url = "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
    
    print("Watcher started. Stream watching for 5 hours 40 minutes...")
    try:
        driver.get(stream_url)
        # 5 hours 40 minutes = 20400 seconds
        time.sleep(20400) 
    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    start_watching()
  
