from unicodedata import normalize
import requests
import os.path
import csv
from bs4 import BeautifulSoup

def trata_termo(termo):
    return remover_acentos(termo.replace(':', '').lower().replace('do ', '').replace('de ', '').replace(' ', '_'))

def trata_descricao(descricao):
    return descricao.replace(' portas', '')

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

#CONF
termos_opcionais = ['air_bag', 'alarme', 'ar_condicionado', 'trava_eletrica', 'vidro_eletrico', 'som', 'sensor_re', 'camera_re']
termos_essenciais = ['id_post', 'modelo', 'ano', 'cor', 'portas', 'potencia_motor', 'combustivel','quilometragem', 'direcao', 'cambio', 'preco']# 9 termos
termos_descartados = ['Categoria', 'Final de placa', 'Único dono', 'Aceita Trocas', 'Tipo de veículo']

num_paginas = int(input('Numero de páginas: '))
for i in range(0, num_paginas):
    print('>> Página {} <<'.format(i+1))
    parametros = {'q': 'carros', 'o': str(i+1)}
    file = requests.get("https://se.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios", params=parametros)
    #print(file.url)
    soup = BeautifulSoup(file.content, 'html.parser')
    cont = 0

    #CAPTURA DOS LINKS
    lista_links = []
    for ul in soup.find_all("ul", {"id": "main-ad-list"}):
        for li in ul.find_all('li'):
            if(li.has_attr('data-list_id')):
                lista_links.append(li.a['href'])

    #PERCORRENDO LINKS
    for link in lista_links:
        lista_atributos = {}
        lista_carros = []
        lista_termos = []
        lista_opcionais = []
        item = requests.get(link)
        soup = BeautifulSoup(item.content, 'html.parser')
        id_post = soup.find('div', {'class': 'OLXad-id'}).p.strong.text
        preco = soup.find('span', {'class': 'actual-price'})
        lista_atributos['id_post'] = id_post

        if(preco is not None):
            preco = preco.text.replace('R$ ', '')
            ul_detalhes = soup.find('div', {'class': 'OLXad-details'}).div.ul.find_all('li')
            for li_detalhes in ul_detalhes:
                if (li_detalhes.parent['class'][0] == 'OLXad-features-list'):
                    descricao = trata_termo(li_detalhes.text.strip())
                    lista_opcionais.append(descricao)
                else:
                    termo = trata_termo(li_detalhes.span.text.strip())
                    descricao = trata_descricao(li_detalhes.span.next_sibling.next_sibling.text.strip())

                if(termo in termos_essenciais):
                    lista_termos.append(termo)
                    lista_atributos[termo] = descricao

            for opcional in termos_opcionais:
                if(opcional in lista_opcionais):
                    lista_atributos[opcional] = 'SIM'
                else:
                    lista_atributos[opcional] = 'NAO'

            lista_atributos['preco'] = preco
            num_opcionais = len(termos_opcionais)
            print(lista_atributos)
            print("Essenciais: {}, Capturados: {}".format(len(termos_essenciais), len(lista_atributos)-num_opcionais))

            if(len(termos_essenciais) == (len(lista_atributos)-num_opcionais)):
               arquivo_existe = os.path.isfile('base_carros.csv')
               with open('base_carros.csv', mode='a') as csv_file:
                   fieldnames = ['id_post', 'modelo', 'ano', 'cor', 'portas', 'potencia_motor', 'combustivel', 'quilometragem', 'direcao', 'cambio', 'air_bag', 'alarme', 'ar_condicionado', 'trava_eletrica', 'vidro_eletrico', 'som', 'sensor_re', 'camera_re', 'preco']
                   writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                   if not arquivo_existe:
                       writer.writeheader()
                   writer.writerow(lista_atributos)
