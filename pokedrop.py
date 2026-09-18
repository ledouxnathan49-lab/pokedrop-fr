
import os
import json
import requests

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

PRODUCTS = [
    {
        "name": "ETB Pokémon 30 ans",
        "url": "https://www.amazon.fr/s?k=Pokemon+30+ans+ETB",
        "store": "Amazon"
    },
    {
        "name": "UPC Pokémon 30 ans",
        "url": "https://www.amazon.fr/s?k=Pokemon+30+ans+UPC",
        "store": "Amazon"
    }
]

STATE = "state.json"

try:
    with open(STATE) as f:
        sent = json.load(f)
except:
    sent = {}

for p in PRODUCTS:
    r = requests.get(p["url"], headers={"User-Agent": "Mozilla/5.0"})

    html = r.text.lower()

    stock = any(mot in html for mot in [
        "ajouter au panier",
        "buy now",
        "en stock",
        "acheter maintenant"
    ])

    if stock:
        if sent.get(p["url"]) != "sent":
            requests.post(WEBHOOK, json={
                "username":"PokéDrop FR",
                "embeds":[{
                    "title":"🎉 Stock détecté",
                    "description":f"**{p['name']}**",
                    "color":3066993,
                    "fields":[
                        {"name":"🏪 Magasin","value":p["store"]},
                        {"name":"🔗 Lien","value":p["url"]}
                    ],
                    "footer":{"text":"PokéDrop V6 • Surveillance 24/7"}
                }]
            })
            sent[p["url"]] = "sent"

with open(STATE,"w") as f:
    json.dump(sent,f)
