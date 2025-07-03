from flask import Flask, request
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# === CONFIGURACIÓN ===
TELEGRAM_TOKEN = '7382546499:AAFuVG7ZKoahhksxxTIjbh59hR56jlv_tnY'
TELEGRAM_CHAT_ID = '1625697501'
POCKET_URL = "https://pocketoption.com/es/"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# === INICIAR SELENIUM CON COOKIES PERSISTENTES ===
def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=selenium")  # Guarda sesión
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(POCKET_URL)
    time.sleep(5)
    return driver

# === EJECUTAR OPERACIÓN EN POCKET OPTION ===
def ejecutar_operacion(driver, tipo):
    try:
        if tipo.upper() == "CALL":
            boton = driver.find_element(By.XPATH, '//button[contains(text(), "COMPRAR")]')
            boton.click()
            bot.send_message(TELEGRAM_CHAT_ID, "✅ Operación ejecutada: CALL")
        elif tipo.upper() == "PUT":
            boton = driver.find_element(By.XPATH, '//button[contains(text(), "VENDER")]')
            boton.click()
            bot.send_message(TELEGRAM_CHAT_ID, "✅ Operación ejecutada: PUT")
        else:
            bot.send_message(TELEGRAM_CHAT_ID, f"⚠️ Tipo de operación desconocido: {tipo}")
    except Exception as e:
        bot.send_message(TELEGRAM_CHAT_ID, f"❌ Error al ejecutar operación: {e}")

# === WEBHOOK PARA RECIBIR SEÑALES ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    activo = data.get("activo")
    tipo = data.get("tipo")
    tiempo = data.get("tiempo")

    mensaje = f"📩 Señal recibida:\nActivo: {activo}\nTipo: {tipo}\nTiempo: {tiempo}"
    bot.send_message(TELEGRAM_CHAT_ID, mensaje)

    driver = iniciar_driver()
    ejecutar_operacion(driver, tipo)
    driver.quit()

    return "OK", 200

# === INICIO DEL SERVIDOR ===
if __name__ == '__main__':
    bot.send_message(TELEGRAM_CHAT_ID, "🚀 Bot iniciado y esperando señales...")
    app.run(host='0.0.0.0', port=5000)
