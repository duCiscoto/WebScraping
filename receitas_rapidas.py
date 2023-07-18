from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import pandas as pd

cards = []

url_base = 'https://pt.petitchef.com'
url = url_base + '/receitas/rapida'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
}

try:
    req = Request(url, headers = headers)
    response = urlopen(req)
    html = response.read().decode('utf-8')
    
except HTTPError as e:
    print(e.status, e.reason)
    
except URLError as e:
    print(e.reason)

soup = BeautifulSoup(html, 'html.parser')
pages = int(soup.find('div', class_="pages").get_text().split()[-1])

for i in range(pages):
    url_page = url_base + '/receitas/rapida-page-' + str(i + 1)

    try:
        req = Request(url_page, headers = headers)
        response = urlopen(req)
        html = response.read().decode('utf-8')
        
    except HTTPError as e:
        print(e.status, e.reason)
        
    except URLError as e:
        print(e.reason)

    soup = BeautifulSoup(html, 'html.parser')
    
    # receitas = soup.find('div', {"id": "recipe-list"}).findAll('div', class_="item clearfix")
    receitas = soup.findAll('div', class_="ingredients")

    for item in receitas:
        card = {}
        receita = item.findPrevious('div', {'class': 'item clearfix'})

        card['nome'] = receita.find('h2', {'class': 'ir-title'}).find('a').getText()
        card['link_receita'] = url_base + receita.find('h2', {'class': 'ir-title'}).find('a')['href']

        try:
            card['url_imagem'] = url_base + receita.find('div', {'class': 'i-left'}).find('img')['src']
            # urlretrieve(card['url_imagem'], './output/img/' + imagem_url.split('/')[-1])
        except:
            card['url_imagem'] = 'Indisponível'

        try:
            card['avaliacao'] = receita.find('div', {'class': 'ir-vote'}).find('i')['title']
        except:
            card['avaliacao'] = 'Indisponível'
        
        try:
            card['comentarios'] = receita.find('div', {'class': 'ir-vote'}).find('i', {'class': 'fal fa-comments fa-fw'}).getText().strip()
        except:
            card['comentarios'] = 'Indisponível'
        
        try:
            card['marcacoes'] = receita.find('div', {'class': 'ir-vote'}).find('i', {'class': 'fal fa-bookmark fa-fw'}).getText().strip()
        except:
            card['marcacoes'] = 'Indisponível'

        try:
            card['tipo'] = receita.find('div', {'class': 'prop'}).find('i', {'class': 'fas fa-utensils'}).findPrevious().getText().strip()
        except:
            card['tipo'] = 'Indisponível'

        try:
            card['dificuldade'] = receita.find('div', {'class': 'prop'}).find('i', {'class': 'fas fa-signal'}).findPrevious().getText().strip()
        except:
            card['dificuldade'] = 'Indisponível'

        try:
            card['tempo_preparo'] = receita.find('div', {'class': 'prop'}).find('i', {'class': 'fas fa-clock'}).findPrevious().getText().strip()
        except:
            card['tempo_preparo'] = 'Indisponível'

        try:
            card['calorias'] = receita.find('div', {'class': 'prop'}).find('i', {'class': 'fas fa-fire'}).findPrevious().getText().strip()
        except:
            card['calorias'] = 'Indisponível'

        try:
            card['tempo_cozedura'] = receita.find('div', {'class': 'prop'}).find('i', {'class': 'fas fa-scale-balanced'}).findPrevious().getText().strip()
        except:
            card['tempo_cozedura'] = 'Indisponível'

        try:
            card['resumo_ingredientes'] = receita.find('div', {'class': 'ingredients'}).getText()
        except:
            card['resumo_ingredientes'] = 'Indisponível'

        cards.append(card)

dataset = pd.DataFrame(cards)
dataset.to_csv('./output/data/dataset.csv', sep=';', index=False, encoding='utf-8-sig')
dataset.to_csv('./output/data/dataset.csv', sep=';', index = False, encoding = 'utf-8-sig')