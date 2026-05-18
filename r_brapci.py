"""
Esse script faz a raspagem das obras do BRAPCI.
Funcionalidade de cada importação:

request --> Fazer requisições do site
tqdm --> Barra de progresso
"""

import requests
from tqdm import tqdm

# Essa função faz uma raspagem no BRAPCI, o campo "busca" recebe como entrada um interesse do usuário.
def scraper_brapci(busca: str,
                   resultados: int = 5) -> list:

    url = "https://cip.brapci.inf.br/api/brapci/search/v3"

    lista_de_obras = []
    offset = 0

    barra = tqdm(desc="Coletando obras", unit=" artigo")

    # Essas especificações correspondem ao que é pedido no JSON do site.
    while True:
        payload = {
            "term": busca,
            "year_start": 1962,
            "year_end": 2026,
            "field": "FL",
            "collection": "JA,JE,EV,BK",
            "api_version": 3,
            "offset": offset
        }

        # O script verifica se o cite consegue devolver um JSON válido.
        response = requests.post(url, data=payload)
        try:
            dados = response.json()
        except ValueError:
            print("Resposta não é JSON!")
            print(response.status_code)
            print(response.text[:500])
            return []

        artigos = dados["works"]

        if not artigos:
            break

        if len(lista_de_obras) >= resultados:
            break

        # Pega as informações de cada obra e coloca na lista que será devolvida.
        for artigo in artigos:
            metadados = artigo["data"]

            lista_de_obras.append({"Fonte" : "BRAPCI",
                                   "Título" : metadados.get("TITLE"),
                                   "Autores" : metadados.get("AUTHORS"),
                                   "Tipo de Obra" : metadados.get("CLASS"),
                                   "Editora" : metadados.get("JOURNAL"),
                                   "Ano" : artigo.get("year"),
                                   "Palavras-chave" : metadados.get("KEYWORDS"),
                                   "Texto" : metadados.get("TITLE") + "; " + metadados.get("KEYWORDS"), # Essa parte é necessária para a mineração de dados
                                   "Link" : f"https://cip.brapci.inf.br//download/{metadados.get("ID")}"})

            barra.update(1)

            if len(lista_de_obras) >= resultados:
                break


        # Pega o prócimo conjunto de obras, como se estivesse "passando a página".
        offset += 6

    barra.close()

    return lista_de_obras

def main():
    scraper_brapci("raspagem de dados")

if __name__ == "__main__":
    main()


