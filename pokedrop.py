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
    {"name":"ETB Pokémon 30 ans","store":"Amazon","url":"https://www.amazon.fr/s?k=pokemon+30+ans+etb"},
    {"name":"UPC Pokémon 30 ans","store":"Amazon","url":"https://www.amazon.fr/s?k=pokemon+30+ans+upc"},
    {"name":"Pokémon 30 ans","store":"Leclerc","url":"https://www.e.leclerc/recherche?q=pokemon+30+ans"},
    {"name":"Pokémon 30 ans","store":"Carrefour","url":"https://www.carrefour.fr/s?q=pokemon+30+ans"},
    {"name":"Pokémon","store":"Fnac","url":"https://www.fnac.com/SearchResult/ResultList.aspx?Search=pokemon"},
    {"name":"Pokémon","store":"Cultura","url":"https://www.cultura.com/recherche/pokemon"},
    {"name":"Pokémon","store":"Micromania","url":"https://www.micromania.fr/recherche/?q=pokemon"},
    {"name":"Pokémon","store":"King Jouet","url":"https://www.king-jouet.com/recherche.aspx?search=pokemon"},
    {"name":"Pokémon","store":"Smyths","url":"https://www.smythstoys.com/fr/fr-fr/search/?text=pokemon"},
    {"name":"Pokémon","store":"JouéClub","url":"https://www.joueclub.fr/catalogsearch/result/?q=pokemon"},
    {"name":"Pokémon Center","store":"Pokémon Center","url":"https://www.pokemoncenter.com/en-gb/search/pokemon"},
]

KEYWORDS = [
    "ajouter au panier",
    "acheter maintenant",
    "buy now",
    "add to cart",
    "en stock",
    "précommande",
    "pre-order"
]

try:
    with open(STATE, "r") as f:
        sent = json.load(f)
except:
    sent = {}

for p in PRODUCTS:
    try:
        r = requests.get(p["url"], headers=HEADERS, timeout=20)
        if r.status_code != 200:
            continue

        html = r.text.lower()

        if any(k in html for k in KEYWORDS):
            if sent.get(p["url"]) != "sent":
                requests.post(
                    WEBHOOK,
                        json={
            "username":"PokéDrop FR",
            "avatar_url":"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png",
            "content":"## 🚨 Nouveau réassort détecté !",
            "embeds":[{
                "title":f"🔥 {p['name']}",
                "description":f"**Disponible chez {p['store']}**",
                "url":p["url"],
                "color":3066993,
                "thumbnail":{
                    "url":"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/master-ball.png"
                },
                "fields":[
                    {"name":"🟢 Statut","value":"**EN STOCK**","inline":True},
                    {"name":"🏪 Magasin","value":p["store"],"inline":True},
                    {"name":"⏰ Détecté","value":"À l'instant","inline":True},
                    {"name":"🛒 Acheter","value":f"[Voir le produit]({p['url']})","inline":False}
                ],
                "footer":{
                    "text":"PokéDrop Pro • Réassorts | Sorties | Bons plans"
                }
            }]
        },