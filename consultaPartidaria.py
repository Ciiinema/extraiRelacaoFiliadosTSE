import requests
import json
import csv

estados = [
    {
        "uf": "AC",
        "id": 24
    }, 
    {
        "uf": "AL",
        "id": 17  
    },
    {
        "uf": "AP",
        "id": 25
    },
    {
        "uf": "AM",
        "id": 22
    },
    {
        "uf": "BA",
        "id": 5
    },
    {
        "uf": "CE",
        "id": 7
    },
    {
        "uf": "DF",
        "id": 20
    },
    {
        "uf": "ES",
        "id": 14
    },
    {
        "uf": "GO",
        "id": 10
    },
    {
        "uf": "MA",
        "id": 11
    },
    {
        "uf": "MT",
        "id": 18
    },
    {
        "uf": "MS",
        "id": 19
    },
    {
        "uf": "MG",
        "id": 2
    },
    {
        "uf": "PA",
        "id": 13
    },
    {
        "uf": "PB",
        "id": 12
    },
    {
        "uf": "PR",
        "id": 6
    },
    {
        "uf": "PE",
        "id": 8
    },
    {
        "uf": "PI",
        "id": 15
    },
    {
        "uf": "RJ",
        "id": 3
    },
    {
        "uf": "RN",
        "id": 16
    },
    {
        "uf": "RS",
        "id": 4
    },
    {
        "uf": "RO",
        "id": 23
    },
    {
        "uf": "RR",
        "id": 26
    },
    {
        "uf": "SC",
        "id": 9
    },
    {
        "uf": "SP",
        "id": 1
    },
    {
        "uf": "SE",
        "id": 21
    },
    {
        "uf": "TO",
        "id": 27
    },
    {
        "uf": "ZZ",
        "id": 28
    }
]

def requisitar(url):
    resposta = requests.get(url)
    return json.loads(resposta.content)

def consultaPartidos():
    url = 'https://filia2-consulta.tse.jus.br/filia-consulta/rest/v1/partidos'
    return requisitar(url)

def consultaMunicipios(uf):
    url = 'https://filia2-consulta.tse.jus.br/filia-consulta/rest/v1/localidade/{}/municipios'.format(uf)
    return requisitar(url)

def consultaZonas(mun):
    url = 'https://filia2-consulta.tse.jus.br/filia-consulta/rest/v1/zona/municipio/{}/zonasEleitorais'.format(mun)
    return requisitar(url)

def consultaRelacao(uf, mun, zona, partido):
    url = 'https://filia2-consulta.tse.jus.br/filia-consulta/rest/v1/relacao-filiados?sgUe={}&cdMunicipio={}&cdZona={}&sqPartido={}&currentPage=0&pageSize=100000000'.format(uf, mun, zona, partido)
    return requisitar(url)

def main():
    labels = ["uf", "uf_id", "municipio", "municipio_id", "zona", "partido", "partido_id", "titulo_eleitor", "nome", "data_filiacao", "situacao", "secao"]
    tabela = []
    partidos = consultaPartidos()
    for uf in estados:
        print(uf['uf'])
        municipios = consultaMunicipios(uf['id'])
        for municipio in municipios:
            zonas = consultaZonas(municipio['codObjeto'])
            for zona in zonas:
                for partido in partidos:
                    # print(uf['uf'], municipio['codObjeto'], zona['numZona'], partido['id'])
                    # print(partido['sgPartido'], partido['id'], uf['uf'], uf['id'], municipio['nomLocalidade'], municipio['codObjeto'], zona['codObjeto'])
                    relacao = consultaRelacao(uf['uf'], municipio['codObjeto'], zona['codObjeto'], partido['id'])
                    if relacao.get('entitys'):
                        for item in relacao['entitys']:
                            objeto = {
                                "uf": uf['uf'],
                                "uf_id": uf['id'],
                                "municipio": municipio['nomLocalidade'],
                                "municipio_id": municipio['codObjeto'],
                                "zona": zona['codObjeto'],
                                "partido": partido['sgPartido'],
                                "partido_id": partido['id'],
                                "titulo_eleitor": item['nrTituloEleitor'],
                                "nome": item['nmEleitor'],
                                "data_filiacao": "{}/{}/{}".format(item['dtFiliacao'][2], item['dtFiliacao'][1], item['dtFiliacao'][0]),
                                "situacao": item['desSituacaoEleitor'],
                                "secao": item['numSecao'],
                            }
                            tabela.append(objeto)
                    else:
                        continue
        try:
            with open("csv/relacao{}.csv".format(uf['uf']), "w", encoding='UTF-8') as f:
                writer = csv.DictWriter(f, fieldnames=labels)
                writer.writeheader()
                writer.writerows(tabela)
                f.close()
        except IOError:
            print("I/O error")
        
        tabela = []            
        # return False
    
main()