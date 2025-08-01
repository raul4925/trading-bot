def ejecutar_operacion(data):
    print("🔍 Ejecutar operación activado")
    print("Datos recibidos:", data)

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pickle
import requests

# 🔐 Telegram config

TELEGRAM_TOKEN = '7546682724:AAEoTx03eZcn7pWGu6GwbTyfUXOHM33Ctk'
CHAT_ID = '1625697501'

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("Error al enviar Telegram:", e)

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://pocketoption.com/es/login")

    # Cargar cookies
    try:
        with open("cookies.pkl", "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
    except Exception as e:
        print("No se pudieron cargar cookies:", e)

    return driver

def ejecutar_operacion(data):
    par = data.get('par', 'EURUSD')
    direccion = data.get('direccion', 'compra')
    tiempo = data.get('tiempo', 1)

    mensaje = f"Ejecutando operación: {direccion.upper()} en {par} por {tiempo} minuto(s)"
    print(mensaje)
    enviar_telegram(mensaje)

    driver = iniciar_driver()
    time.sleep(5)

    if direccion == 'compra':
        boton_xpath = '//*[@id="deal-btn-call"]'
    else:
        boton_xpath = '//*[@id="deal-btn-put"]'

    try:
        boton = driver.find_element(By.XPATH, boton_xpath)
        boton.click()
        print("Operación ejecutada correctamente.")
        enviar_telegram("✅ Operación ejecutada correctamente.")
    except Exception as e:
        print("Error al ejecutar operación:", e)
        enviar_telegram("❌ Error al ejecutar operación.")

    time.sleep(3)
    driver.quit()
