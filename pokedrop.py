import os
import json
import requests
from bs4 import BeautifulSoup

WEBHOOK = os.getenv("DISCORD_WEBHOOK")
STATE = "state.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PRODUCTS = [
    {"name":"ETB Pokémon","store":"Amazon","url":"https://www.amazon.fr/s?k=pokemon+elite+trainer+box"},
    {"name":"UPC Pokémon","store":"Amazon","url":"https://www.amazon.fr/s?k=pokemon+ultra+premium+collection"},
    {"name":"Booster Bundle","store":"Amazon","url":"https://www.amazon.fr/s?k=pokemon+booster+bundle"},
    {"name":"ETB Pokémon","store":"Leclerc","url":"https://www.e.leclerc/recherche?q=pokemon"},
    {"name":"UPC Pokémon","store":"Leclerc","url":"https://www.e.leclerc/recherche?q=pokemon"},
    {"name":"Pokémon","store":"Carrefour","url":"https://www.carrefour.fr/s?q=pokemon"},
    {"name":"Pokémon","store":"Cultura","url":"https://www.cultura.com/recherche/pokemon"},
    {"name":"Pokémon","store":"Fnac","url":"https://www.fnac.com/SearchResult/ResultList.aspx?Search=pokemon"},
    {"name":"Pokémon","store":"Micromania","url":"https://www.micromania.fr/recherche?text=pokemon"},
    {"name":"Pokémon","store":"JouéClub","url":"https://www.joueclub.fr/recherche?text=pokemon"},
    {"name":"Pokémon","store":"King Jouet","url":"https://www.king-jouet.com/recherche.aspx?search=pokemon"},
    {"name":"Pokémon","store":"Smyths","url":"https://www.smythstoys.com/fr/fr-fr/search/?text=pokemon"},
    {"name":"Pokémon","store":"Auchan","url":"https://www.auchan.fr/recherche?text=pokemon"}
]

WORDS = [
    "ajouter au panier",
    "acheter maintenant",
    "buy now",
    "add to cart",
    "en stock",
    "livraison"
]

try:
    with open(STATE) as f:
        sent = json.load(f)
except:
    sent = {}

for p in PRODUCTS:
    try:
        r = requests.get(p["url"], headers=HEADERS, timeout=20)
        html = r.text.lower()

        stock = any(word in html for word in WORDS)

        key = p["store"] + p["name"]

        if stock and not sent.get(key):
            requests.post(WEBHOOK, json={
                "username":"PokéDrop Pro",
                "embeds":[{
                    "title":"🚨 Réassort détecté",
                    "description":f"**{p['name']}** disponible chez **{p['store']}**",
                    "url":p["url"],
                    "color":3066993,
                    "footer":{"text":"PokéDrop Pro • Surveillance 24/7"}
                }]
            })
            sent[key] = True

    except:
        pass

with open(STATE,"w") as f:
    json.dump(sent,f)