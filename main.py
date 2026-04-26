import requests
import os

# Obtiene las credenciales de GitHub Secrets
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Endpoint de Epic Games (configurado para tu región e idioma)
url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=es-ES&country=CO&allowCountries=CO"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(url, headers=headers)
    data = response.json()
    juegos = data["data"]["Catalog"]["searchStore"]["elements"]
    
    juegos_gratis = []
    
    # Navegar por el JSON para encontrar los juegos con descuento del 100%
    for juego in juegos:
        if juego.get("promotions"):
            promos = juego["promotions"]["promotionalOffers"]
            if promos:
                ofertas = promos[0]["promotionalOffers"]
                if ofertas and ofertas[0]["discountSetting"]["discountPercentage"] == 0:
                    titulo = juego["title"]
                    precio_original = juego["price"]["totalPrice"]["fmtPrice"]["originalPrice"]
                    juegos_gratis.append(f"🎮 **{titulo}**\n💰 Precio original: {precio_original}")
    
    # Si encuentra juegos, envía el mensaje por Telegram
    if juegos_gratis:
        mensaje = "🎁 **¡Juegos Gratis de la Semana en Epic!**\n\n" + "\n\n".join(juegos_gratis)
        telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(telegram_url, json={
            "chat_id": CHAT_ID, 
            "text": mensaje, 
            "parse_mode": "Markdown"
        })
        print("Mensaje enviado con éxito.")
    else:
        print("No se encontraron juegos gratis nuevos.")

except Exception as e:
    print(f"Error al ejecutar el script: {e}")