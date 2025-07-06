from selenium import webdriver
import pickle
import time

driver = webdriver.Chrome()
driver.get("https://pocketoption.com/es/")
print("🔐 Iniciá sesión manualmente...")
time.sleep(30)

with open("cookies.pkl", "wb") as f:
    pickle.dump(driver.get_cookies(), f)

print("✅ Cookies guardadas en cookies.pkl")
driver.quit()
