import os
import json
import re
import requests
from bs4 import BeautifulSoup

WEBHOOK=os.getenv('DISCORD_WEBHOOK')
STATE='state.json'
URL='https://www.e.leclerc/fr/recherche?q=pokemon'
KEYWORDS=['etb','coffret dresseur','elite trainer','upc','ultra premium','booster bundle','lot de 6 boosters','display','pokemon 30 ans','evolutions prismatiques']
BLOCK=['jap','japon','peluche','figurine']
HEADERS={'User-Agent':'Mozilla/5.0'}
try:
 sent=json.load(open(STATE))
except:
 sent={}
soup=BeautifulSoup(requests.get(URL,headers=HEADERS,timeout=20).text,'html.parser')
for card in soup.select("a[href*='/fp/']"):
 title=card.get_text(' ',strip=True)
 low=title.lower()
 if not any(k in low for k in KEYWORDS): continue
 if any(b in low for b in BLOCK): continue
 href=card.get('href')
 if not href: continue
 link='https://www.e.leclerc'+href if href.startswith('/') else href
 if link in sent: continue
 img=''; im=card.select_one('img')
 if im and im.get('src'): img='https:'+im['src'] if im['src'].startswith('//') else im['src']
 m=re.search(r'(\d+[,.]?\d*)\s*€',title); price=m.group(0) if m else 'Prix à vérifier'
 requests.post(WEBHOOK,json={'username':'PokéDrop FR','embeds':[{'title':'🛒 Réassort détecté','description':f'**{title}**','url':link,'color':5763719,'thumbnail':{'url':img} if img else {},'fields':[{'name':'🏪 Magasin','value':'Leclerc','inline':True},{'name':'💰 Prix','value':price,'inline':True},{'name':'🟢 Statut','value':'En stock','inline':True},{'name':'🔗 Lien','value':f'[Ouvrir le produit]({link})','inline':False}],'footer':{'text':'PokéDrop FR • Temps réel'}}]})
 sent[link]=True
json.dump(sent,open(STATE,'w'),indent=2)