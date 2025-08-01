from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
import requests

app = Flask(__name__)

# 🔧 Configuración de Telegram
TELEGRAM_TOKEN = '7546680274:AAfeXoJ3eZn7YpGuGGwbTyFUXOH33Ctk'
TELEGRAM_CHAT_ID = '162597501'

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("❌ Error al enviar Telegram:", e)

def iniciar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--headless")  # Opcional para VPS
    driver = webdriver.Chrome(options=options)
    driver.get("https://pocketoption.com/es/trading/")
    return driver

def estructura_operacion(direccion, par, tiempo, monto, tipo_operacion):
    mensaje = f"🚀 Alerta recibida: {direccion.upper()} en {par} por {tiempo}m con ${monto} [{tipo_operacion}]"
    print(mensaje)
    enviar_telegram(mensaje)

    xpath_compra = "//div[@id='deal-btn-call']"
    xpath_venta = "//div[@id='deal-btn-put']"
    boton_xpath = xpath_compra if direccion == 'compra' else xpath_venta

    par_xpath = f"//div[contains(text(), '{par}')]"
    tiempo_xpath = f"//button[contains(text(), '{tiempo}m')]"
    monto_input_xpath = "//input[@name='amount']"
    tipo_operacion_xpath = f"//div[contains(text(), '{tipo_operacion}')]"

    driver = iniciar_driver()

    try:
        driver.switch_to.default_content()

        # Tipo de operación
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, tipo_operacion_xpath))
            ).click()
            print(f"✅ Tipo: {tipo_operacion}")
        except:
            print(f"⚠️ No se pudo seleccionar tipo: {tipo_operacion}")

        # Par
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, par_xpath))
            ).click()
            print(f"✅ Par: {par}")
        except:
            print(f"⚠️ No se pudo seleccionar par: {par}")

        # Tiempo
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, tiempo_xpath))
            ).click()
            print(f"✅ Tiempo: {tiempo}m")
        except:
            print(f"⚠️ No se pudo seleccionar tiempo: {tiempo}m")

        # Monto
        try:
            monto_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, monto_input_xpath))
            )
            monto_input.clear()
            monto_input.send_keys(monto)
            print(f"✅ Monto: ${monto}")
        except:
            print(f"⚠️ No se pudo ingresar monto: ${monto}")

        # Botón en iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        boton_encontrado = False

        for iframe in iframes:
            driver.switch_to.frame(iframe)
            try:
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, boton_xpath))
                ).click()
                print("✅ Operación ejecutada")
                enviar_telegram("✅ Operación ejecutada correctamente.")
                boton_encontrado = True
                break
            except:
                driver.switch_to.default_content()

        if not boton_encontrado:
            print("❌ Botón no encontrado")
            enviar_telegram("❌ No se encontró el botón para ejecutar la operación.")

    except Exception as e:
        print("❌ Error general:", e)
        enviar_telegram(f"❌ Error general: {str(e)}")

    time.sleep(3)
    driver.quit()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    direccion = data.get('direccion', 'compra')
    par = data.get('par', 'EURUSD')
    tiempo = int(data.get('tiempo', 1))
    monto = str(data.get('monto', '5'))
    tipo_operacion = data.get('tipo', 'Turbo')

    threading.Thread(target=estructura_operacion, args=(direccion, par, tiempo, monto, tipo_operacion)).start()
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(port=5000)
