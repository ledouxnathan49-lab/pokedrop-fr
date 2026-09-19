import os
import json
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.getenv("DISCORD_WEBHOOK")
STATE = "state.json"
URL = "https://www.e.leclerc/recherche?q=pokemon"

# Uniquement les produits les plus intéressants à la revente
KEYWORDS = [
    "etb",
    "coffret dresseur d'élite",
    "elite trainer box",
    "upc",
    "ultra premium",
    "booster bundle",
    "display",
    "pokemon 30 ans",
    "évolutions prismatiques",
    "evolutions prismatiques"
]

# Produits à ignorer pour éviter le spam
EXCLUDE = [
    "jap",
    "scellé jap",
    "peluche",
    "porte-clés",
    "figurine",
    "mini tin",
    "poster"
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

try:
    with open(STATE, "r") as f:
        sent = json.load(f)
except:
    sent = {}

r = requests.get(URL, headers=HEADERS, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")

for card in soup.select("a[href*='/fp/']"):
    title = card.get_text(" ", strip=True)
    title_lower = title.lower()

    if any(x in title_lower for x in EXCLUDE):
        continue

    if not any(k in title_lower for k in KEYWORDS):
        continue

    href = card.get("href")
    if not href:
        continue

    link = "https://www.e.leclerc" + href if href.startswith("/") else href
    if sent.get(link):
        continue

    img = ""
    image = card.select_one("img")
    if image and image.get("src"):
        img = image["src"]
        if img.startswith("//"):
            img = "https:" + img

    requests.post(WEBHOOK, json={
        "username": "PokéDrop FR",
        "embeds": [{
            "title": f"🚨 {title}",
            "description": "**Produit à fort potentiel de revente détecté**",
            "url": link,
            "color": 0xE53935,
            "thumbnail": {"url": img} if img else {},
            "fields": [
                {"name": "🏪 Magasin", "value": "Leclerc", "inline": True},
                {"name": "🟢 Statut", "value": "En stock", "inline": True},
                {"name": "🔗 Lien", "value": f"[Ouvrir le produit]({link})", "inline": False}
            ],
            "footer": {"text": "PokéDrop FR • Alerte filtrée"}
        }]
    })

    sent[link] = "sent"

with open(STATE, "w") as f:
    json.dump(sent, f, indent=2)