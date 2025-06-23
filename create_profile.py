import undetected_chromedriver as uc
import time,os

def create_profile(profile_path):
    PROFILE_PATH = profile_path

    for i in range(2):
        options = uc.ChromeOptions()
        options.add_argument(f"--user-data-dir={os.path.abspath(PROFILE_PATH)}")
        driver = uc.Chrome(options=options, headless=False)

        # Step 1: Open Google (neutral site)
        driver.get("https://www.google.com")
        time.sleep(3)

        # Step 2: Inject a clickable button to simulate user interaction
        driver.execute_script("""
            let btn = document.createElement('button');
            btn.innerText = 'Click Me';
            btn.id = 'myBtn';
            btn.onclick = function() {
                window.open('https://www.realtor.com', '_blank');
            };
            document.body.appendChild(btn);
        """)

        time.sleep(1)

        # Step 3: Find the button and click it
        from selenium.webdriver.common.by import By
        driver.find_element(By.ID, "myBtn").click()

        # Step 4: Switch to the new tab
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[1])

        # Done — you're now on Realtor.com
        time.sleep(5)
        print("Title:", driver.title)
        input("Press Enter to quit...")
        driver.quit()
