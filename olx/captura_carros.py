import requests
from bs4 import BeautifulSoup

termos_essenciais = ['Modelo:', 'Ano:', 'Cor:', 'Portas:', 'Potência do motor:', 'Combustível:',
                     'Quilometragem:', 'Direção:', 'Câmbio:']# 9 termos
termos_descartados = ['Categoria:', 'Final de placa:', 'Único dono:', 'Aceita Trocas:', 'Tipo de veículo:']

parametros = {'q': 'carros'}
file = requests.get("https://se.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios", params=parametros)
#print(file.url)
soup = BeautifulSoup(file.content, 'html.parser')
#soup = soup.find_all("ul", {"id": "main-ad-list"})
#print()
cont = 0

##CAPTURA DOS LINKS
lista_links = []
for ul in soup.find_all("ul", {"id": "main-ad-list"}):
    for li in ul.find_all('li'):
        if(li.has_attr('data-list_id')):
            lista_links.append(li.a['href'])
            cont+= 1
        if cont == 1:
            break;
#print(cont)
#print(lista_links)
##


lista_atributos = []
lista_carros = []
lista_termos = []
lista_opcionais = []
for link in lista_links:
    item = requests.get(link)
    soup = BeautifulSoup(item.content, 'html.parser')
    id_carro = soup.find('div', {'class': 'OLXad-id'}).p.strong.text
    preco = soup.find('span', {'class': 'actual-price'})
    #modelo = soup.find('span', string='Modelo:').next_sibling.next_sibling.a.text.strip()
    print("Modelooo")
    #print(modelo)
    ano = ''
    if(preco is not None):
        print("ID: "+id_carro)
        print("Preço: "+preco.contents[0])

        ul_detalhes = soup.find('div', {'class': 'OLXad-details'}).div.ul.find_all('li')
        #print(ul_detalhes
        for li_detalhes in ul_detalhes:
            if (li_detalhes.parent['class'][0] == 'OLXad-features-list'):
                termo = 'Opcional: '
                descricao = li_detalhes.text.strip()
                lista_opcionais.append(descricao)
            else:
                termo = li_detalhes.span.text.strip()
                descricao = li_detalhes.span.next_sibling.next_sibling.text.strip()


            if(termo in termos_essenciais):
                lista_termos.append(termo)
                lista_atributos.append((termo, descricao))
                print(termo + descricao)



        print(lista_termos)
        print(lista_atributos)
        print(lista_opcionais)
        if(len(lista_termos) == len(termos_essenciais)):
           pass