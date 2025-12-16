import requests
from tqdm import tqdm

def scraper_brapci(busca, resultados = 5):
    url = "https://cip.brapci.inf.br/api/brapci/search/v3"

    lista_de_obras = []
    offset = 0

    barra = tqdm(desc="Coletando obras", unit=" artigo")

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

        for artigo in artigos:
            metadados = artigo["data"]

            lista_de_obras.append({"Fonte" : "BRAPCI",
                                   "Título" : metadados.get("TITLE"),
                                   "Autores" : metadados.get("AUTHORS"),
                                   "Tipo de Obra" : metadados.get("CLASS"),
                                   "Editora" : metadados.get("JOURNAL"),
                                   "Ano" : artigo.get("year"),
                                   "Palavras-chave" : metadados.get("KEYWORDS"),
                                   "Texto" : metadados.get("TITLE") + "; " + metadados.get("KEYWORDS"),
                                   "Link" : f"https://cip.brapci.inf.br//download/{metadados.get("ID")}"})

            barra.update(1)

            if len(lista_de_obras) >= resultados:
                break


        offset += 6

    barra.close()

    return lista_de_obras

def main():
    scraper_brapci("raspagem de dados")

if __name__ == "__main__":
    main()


