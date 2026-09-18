
import os
import json
import requests
from bs4 import BeautifulSoup

STATE = "state.json"
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URL = "https://www.e.leclerc/recherche?q=30%20anniversaire%20pokemon"

try:
    with open(STATE, "r") as f:
        sent = json.load(f)
except:
    sent = {}

r = requests.get(URL, headers=HEADERS, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")

cards = soup.select("article")

for card in cards:
    text = card.get_text(" ", strip=True)

    if "30" not in text or "pokémon" not in text.lower():
        continue

    title = card.select_one("h2,h3")
    title = title.get_text(strip=True) if title else "Pokémon 30 ans"

    price = "Prix inconnu"
    for span in card.select("span"):
        t = span.get_text(" ", strip=True)
        if "€" in t:
            price = t
            break

    img = ""
    image = card.select_one("img")
    if image and image.get("src"):
        img = image["src"]
        if img.startswith("//"):
            img = "https:" + img

    link = URL
    a = card.select_one("a[href]")
    if a:
        href = a["href"]
        if href.startswith("/"):
            link = "https://www.e.leclerc" + href
        elif href.startswith("http"):
            link = href

    if sent.get(link):
        continue

    requests.post(
        WEBHOOK,
        json={
            "username": "PokéDrop FR",
            "embeds": [{
                "title": "🔥 Réassort détecté",
                "description": f"**{title}**",
                "url": link,
                "color": 3066993,
                "thumbnail": {"url": img} if img else {},
                "fields": [
                    {"name": "💰 Prix", "value": price, "inline": True},
                    {"name": "🏪 Magasin", "value": "Leclerc", "inline": True},
                    {"name": "🟢 Statut", "value": "Disponible", "inline": True}
                ],
                "footer": {"text": "PokéDrop V7 • Lien direct vers le produit"}
            }]
        }
    )

    sent[link] = True

with open(STATE, "w") as f:
    json.dump(sent, f, indent=2)
