import os
import json
import requests

WEBHOOK = os.getenv("DISCORD_WEBHOOK")
STATE = "state.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

PRODUCTS = [
    {"name":"ETB Pokémon 30 ans","store":"Amazon","url":"https://www.amazon.fr/s?k=Pokemon+30+ans+ETB"},
    {"name":"UPC Pokémon 30 ans","store":"Amazon","url":"https://www.amazon.fr/s?k=Pokemon+30+ans+UPC"},
    {"name":"ETB Pokémon 30 ans","store":"Leclerc","url":"https://www.e.leclerc/recherche?q=pokemon+30+ans"},
    {"name":"UPC Pokémon 30 ans","store":"Leclerc","url":"https://www.e.leclerc/recherche?q=pokemon+30+ans+upc"},
    {"name":"ETB Pokémon 30 ans","store":"Carrefour","url":"https://www.carrefour.fr/s?q=pokemon+30+ans"},
    {"name":"UPC Pokémon 30 ans","store":"Carrefour","url":"https://www.carrefour.fr/s?q=pokemon+30+ans+upc"},
    {"name":"ETB Pokémon 30 ans","store":"Cultura","url":"https://www.cultura.com/recherche?q=pokemon+30+ans"},
    {"name":"UPC Pokémon 30 ans","store":"Cultura","url":"https://www.cultura.com/recherche?q=pokemon+30+ans+upc"},
    {"name":"ETB Pokémon 30 ans","store":"Micromania","url":"https://www.micromania.fr/recherche/?q=pokemon+30+ans"},
    {"name":"UPC Pokémon 30 ans","store":"Micromania","url":"https://www.micromania.fr/recherche/?q=pokemon+30+ans+upc"}
]

KEYWORDS = [
    "ajouter au panier",
    "acheter maintenant",
    "en stock",
    "buy now",
    "add to cart",
    "disponible"
]

try:
    with open(STATE,"r") as f:
        sent=json.load(f)
except:
    sent={}

for p in PRODUCTS:
    try:
        r=requests.get(p["url"],headers=HEADERS,timeout=20)
        html=r.text.lower()

        stock=any(k in html for k in KEYWORDS)

        if stock and sent.get(p["url"])!="sent":
            requests.post(WEBHOOK,json={
                "username":"PokéDrop FR",
                "embeds":[{
                    "title":f"🎉 {p['name']} disponible !",
                    "description":"Stock détecté automatiquement.",
                    "color":3066993,
                    "fields":[
                        {"name":"🏪 Magasin","value":p["store"],"inline":True},
                        {"name":"🔗 Lien","value":p["url"],"inline":False}
                    ],
                    "footer":{"text":"PokéDrop FR • Surveillance 24/7"}
                }]
            })
            sent[p["url"]]="sent"

        elif not stock:
            sent[p["url"]]="waiting"

    except Exception:
        pass

with open(STATE,"w") as f:
    json.dump(sent,f)