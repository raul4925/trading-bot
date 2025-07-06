import requests

url = "http://localhost:5000/webhook"
data = { "accion": "COMPRAR" }  # Cambiá a "VENDER" si querés

response = requests.post(url, json=data)
print("📩 Respuesta del bot:", response.text)
