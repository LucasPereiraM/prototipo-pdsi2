# webscrapping.py
import requests
from bs4 import BeautifulSoup

def coletar_dados_do_site():
    url = "https://ufu.br/graduacao"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        section = soup.find('nav', id='block-ufu-rodape-2')

        if section:
            items = section.find_all('a')
            dados_coletados = []

            for item in items:
                text = item.get_text(strip=True)
                link = item.get('href')
                dados_coletados.append({"menuNav": text, "link": link})

            return dados_coletados
        else:
            raise Exception("Seção 'block-ufu-rodape-2' não encontrada.")
    else:
        raise Exception(f"Erro ao acessar a página: {response.status_code}")
