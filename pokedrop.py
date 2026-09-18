import os, json, requests

WEBHOOK=os.getenv('DISCORD_WEBHOOK')
STATE='state.json'
HEADERS={'User-Agent':'Mozilla/5.0'}

STORES={
 'Amazon':'https://www.amazon.fr/s?k={}',
 'Leclerc':'https://www.e.leclerc/recherche?q={}',
 'Carrefour':'https://www.carrefour.fr/s?q={}',
 'Cultura':'https://www.cultura.com/recherche?q={}',
 'Micromania':'https://www.micromania.fr/recherche/?q={}'
}

SEARCHES=['pokemon 30 ans ETB','pokemon 30 ans UPC','pokemon 30 ans','pokemon ETB','pokemon UPC','pokemon coffret','pokemon booster bundle','pokemon elite trainer box','pokemon display','pokemon coffret premium','pokemon booster','pokemon précommande','pokemon restock']
KEYWORDS=['ajouter au panier','acheter maintenant','en stock','buy now','add to cart','disponible','précommander']

PRODUCTS=[{'name':q,'store':s,'url':u.format(q.replace(' ','+'))} for s,u in STORES.items() for q in SEARCHES]

try: sent=json.load(open(STATE))
except: sent={}

for p in PRODUCTS:
  try:
    html=requests.get(p['url'],headers=HEADERS,timeout=20).text.lower(); stock=any(k in html for k in KEYWORDS)
    if stock and sent.get(p['url'])!='sent':
      requests.post(WEBHOOK,json={'username':'PokéDrop FR','embeds':[{'title':f"🚨 {p['name']}",'description':'Stock ou précommande détecté automatiquement.','color':3066993,'fields':[{'name':'🏪 Magasin','value':p['store'],'inline':True},{'name':'🔗 Lien','value':p['url'],'inline':False}],'footer':{'text':'PokéDrop FR • Ultimate 24/7'}}]}); sent[p['url']]='sent'
    elif not stock: sent[p['url']]='waiting'
  except: pass
json.dump(sent,open(STATE,'w'))