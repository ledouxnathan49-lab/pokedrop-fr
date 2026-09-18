import json
import os
import requests

STATE = "state.json"
WEBHOOK = os.getenv("DISCORD_WEBHOOK")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PRODUCTS = [
    {
        "name": "ETB Pokémon 30 ans",
        "store": "Leclerc",
    "url": "https://www.e.leclerc/recherche?q=30%20anniversaire%20pokemon"
    },
    {
        "name": "UPC Pokémon 30 ans",
        "store": "Leclerc",
        "url": "https://www.e.leclerc/recherche?q=pokemon+30+ans"
    },
    {
    "name": "Pokémon 30 ans",
    "store": "Carrefour",
    "url": "https://www.carrefour.fr/s?q=30%20anniversaire%20pokemon"
},
    {
        "name": "Pokémon",
        "store": "Fnac",
        "url": "https://www.fnac.com/SearchResult/ResultList.aspx?Search=pokemon"
    },
    {
        "name": "Pokémon",
        "store": "Cultura",
        "url": "https://www.cultura.com/recherche/pokemon"
    },
    {
        "name": "Pokémon",
        "store": "Micromania",
        "url": "https://www.micromania.fr/recherche/?q=pokemon"
    },
    {
        "name": "Pokémon",
        "store": "King Jouet",
        "url": "https://www.king-jouet.com/recherche?text=pokemon"
    },
    {
        "name": "Pokémon",
        "store": "Smyths",
        "url": "https://www.smythstoys.com/fr/fr-fr/search/?text=pokemon"
    },
    {
        "name": "Pokémon",
        "store": "JouéClub",
        "url": "https://www.joueclub.fr/recherche?text=pokemon"
    },
    {
        "name": "Pokémon Center",
        "store": "Pokémon Center",
        "url": "https://www.pokemoncenter.com/"
    }
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
        r = requests.get(p["url"], headers=HEADERS, timeout=15)

        if r.status_code != 200:
            continue

        html = r.text.lower()

        if any(k in html for k in KEYWORDS):

            if sent.get(p["url"]) != "sent":

                requests.post(
                    WEBHOOK,
                    json={
                        "username": "PokéDrop FR",
                        "embeds": [{
                            "title": "🚨 Réassort détecté",
                            "description": f"**{p['name']}** est disponible !",
                            "url": p["url"],
                            "color": 3066993,
                            "thumbnail": {
                                "url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"
                            },
                            "fields": [
                                {
                                    "name": "🟢 Statut",
                                    "value": "En stock",
                                    "inline": True
                                },
                                {
                                    "name": "🏪 Magasin",
                                    "value": p["store"],
                                    "inline": True
                                },
                                {
                                    "name": "🛒 Acheter",
                                    "value": f"[Ouvrir le produit]({p['url']})",
                                    "inline": False
                                }
                            ],
                            "footer": {
                                "text": "PokéDrop Pro • Réassort automatique"
                            }
                        }]
                    }
                )

                sent[p["url"]] = "sent"

        else:
            sent[p["url"]] = "waiting"

    except Exception:
        pass

with open(STATE, "w") as f:
    json.dump(sent, f, indent=2)