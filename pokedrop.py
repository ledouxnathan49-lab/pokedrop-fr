import os
import json
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.getenv("DISCORD_WEBHOOK")
STATE = "state.json"

URL = "https://www.e.leclerc/recherche?q=pokemon%2030%20ans"

KEYWORDS = [
    "etb",
    "coffret dresseur d'élite",
    "elite trainer box",
    "upc",
    "ultra premium",
    "booster bundle",
    "lot de 6 boosters",
    "display",
    "pokemon 30 ans",
    "evolutions prismatiques",
    "nymphali",
    "amphinobi"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


try:
    with open(STATE, "r") as f:
        sent = json.load(f)
except:
    sent = {}

r = requests.get(URL, headers=HEADERS, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")

cards = soup.select("a[href*='/fp/']")

for card in cards:
    title = card.get_text(" ", strip=True)
    href = card.get("href")

    if not href:
        continue

    if href.startswith("/"):
        link = "https://www.e.leclerc" + href
    else:
        link = href

    if sent.get(link):
        continue

    img = ""
    image = card.select_one("img")
    if image and image.get("src"):
        img = image["src"]
        if img.startswith("//"):
            img = "https:" + img

    price = "Non indiqué"

    requests.post(
        WEBHOOK,
        json={
            "username": "PokéDrop FR",
            "embeds": [{
                "title": f"🛒 {title}",
                "description": "**Disponible chez Leclerc**",
                "url": link,
                "color": 15158332,
                "thumbnail": {"url": img} if img else {},
                "fields": [
                    {"name": "🏪 Store", "value": "Leclerc", "inline": True},
                    {"name": "💰 Prix", "value": price, "inline": True},
                    {"name": "🟢 Statut", "value": "En stock", "inline": True},
                    {"name": "🔗 Lien", "value": f"[Ouvrir le produit]({link})", "inline": False}
                ],
                "footer": {
                    "text": "PokéDrop FR • Temps réel"
                }
            }]
        }
    )

    sent[link] = "sent"

with open(STATE, "w") as f:
    json.dump(sent, f, indent=2)