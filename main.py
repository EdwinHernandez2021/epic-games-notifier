import requests
import os

# Obtiene las credenciales de GitHub Secrets
# Obtiene las credenciales y elimina cualquier espacio en blanco invisible (.strip())
TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

# Endpoint de Epic Games
url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=CO&allowCountries=CO"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    juegos = data["data"]["Catalog"]["searchStore"]["elements"]
    
    juegos_gratis = []
    
    for juego in juegos:
        # Buscamos de forma más segura el precio
        precio_info = juego.get("price", {}).get("totalPrice", {})
        precio_original = precio_info.get("originalPrice", 0)
        precio_descuento = precio_info.get("discountPrice", -1)
        
        # Es gratis si el precio final es 0 pero originalmente costaba algo
        if precio_descuento == 0 and precio_original > 0:
            titulo = juego.get("title", "Juego desconocido")
            precio_fmt = precio_info.get("fmtPrice", {}).get("originalPrice", "N/A")
            juegos_gratis.append(f"🎮 {titulo}\n💰 Precio original: {precio_fmt}")
    
    if juegos_gratis:
        mensaje = "🎁 ¡Juegos Gratis de la Semana en Epic!\n\n" + "\n\n".join(juegos_gratis)
        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        
        # Quitamos el Markdown para evitar errores por caracteres especiales en los títulos
        res = requests.post(telegram_url, json={
            "chat_id": CHAT_ID, 
            "text": mensaje
        })
        
        # Esto nos dirá exactamente si Telegram aceptó o rechazó el mensaje
        if res.status_code == 200:
            print("Mensaje enviado con éxito a Telegram.")
        else:
            print(f"ERROR DE TELEGRAM: {res.text}")
            
    else:
        print("El script corrió bien, pero no detectó juegos gratis con la lógica actual.")

except Exception as e:
    print(f"Error fatal al ejecutar el script: {e}")