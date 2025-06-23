
import undetected_chromedriver as uc
import time, os, random
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from bs4 import BeautifulSoup
from create_profile import create_profile


# Persistent profile
PROFILE_PATH = os.path.abspath("chrome_profile")

@dataclass
class RealtorScrapperConfig:
    # Persistent profile
    PROFILE_PATH = os.path.abspath("chrome_profile")


class RealtorScrapper:
    
    def __init__(self,driver:uc.Chrome) -> None:
        self.config = RealtorScrapperConfig()
        self.driver = driver
    
    @staticmethod
    def humanLikeInput(text,field):
        for char in text:
            field.send_keys(char)
            time.sleep(random.uniform(0.2,0.5))    
    
    def search(self,search_area):
        search_box=self.driver.find_element(By.ID,'search-bar')
        search_box.click()
        search_box.send_keys(Keys.CONTROL, 'a') 
        search_box.send_keys(Keys.CONTROL, 't') # Select all text
        time.sleep(0.5)
        search_box.send_keys(Keys.BACKSPACE)     # Delete selected text
        time.sleep(1)

        self.humanLikeInput(search_area,search_box)
        search_box.send_keys(Keys.RETURN)
    
    def wait(self):
        try:
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # print("hi")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(3)
            self.driver.execute_script("window.scrollTo(document.body.scrollHeight,0);")
            time.sleep(3)
            # ⏳ Wait for main property cards or a key container to load
        except Exception:
            print("⚠️ Timeout: Listings may not be fully loaded.")
                 




        
        
    def Scrap(self,search_area,pages):
        # Open target site
        self.driver.get("https://www.realtor.com/")
        self.search(search_area)
        self.wait()
        data=[]
        
        for page in range(pages):
            try:
                print(f"Doing scraping at page {page}")
                # Store current URL to compare after click
                current_url = self.driver.current_url

                # Wait for a clickable next button (not disabled)
                next_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".next-link:not(.disable)"))
                )

                print("Yes Click")
                next_btn.click()
                time.sleep(2)  # Wait for page to update

                # Check if the URL has changed (page actually advanced)
                if self.driver.current_url == current_url:
                    print("Page did not change, assuming end of pagination.")
                    break

            except Exception as e:
                print("END (Button not clickable or not present)")
                print(str(e))
                break
        else:
            print(f"Scrapped total {pages} pages")
        print(data)
        print(len(data))
def main():
    
    try:   
        if not os.path.exists(PROFILE_PATH):
            create_profile(PROFILE_PATH)
                 
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={PROFILE_PATH}")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = uc.Chrome(
            service=Service("./chromedriver.exe"),
         options=options)

        scrapper_obj = RealtorScrapper(driver)
        scrapper_obj.Scrap("New York",2)
    except Exception:
        print("⚠️ error")


    # driver.save_screenshot("2_loaded.png")
    # print("[INFO] Page title:", driver.title)

if __name__=="__main__":
    main()