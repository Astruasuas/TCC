"""
Esse script faz a raspagem das obras do OpenAlex.
Funcionalidade de cada importação:

request --> Fazer requisições do site
tqdm --> Barra de progresso
"""

import requests
from tqdm import tqdm

# Essa função faz uma raspagem no OpenAlex, o campo "busca" recebe como entrada um interesse do usuário.
def scraper_openalex(busca, limite=100):
    url = "https://api.openalex.org/works"
    lista_de_obras = []

    per_page = 50 if limite > 50 else limite

    # Parametros do mecanismo de busca interno do site
    parametros = {
        "search": busca,
        "filter": "is_oa:true",
        "per_page": per_page,
        "cursor": "*",
        "mailto": "seu@email"
    }

    barra = tqdm(desc="Coletando obras", unit=" artigo")

    while len(lista_de_obras) < limite:
        # O script verifica se o site consegue devolver um JSON válido
        resposta = requests.get(url, params=parametros)

        if resposta.status_code != 200:
            print(f"Erro HTTP {resposta.status_code}")
            break

        if not resposta.text.strip():
            print("Resposta vazia da API")
            break

        try:
            dados = resposta.json()
        except Exception as e:
            print("Erro ao converter JSON:", e)
            print("Conteúdo recebido:", resposta.text[:200])
            break

        resultados = dados.get("results", [])
        if not resultados:
            break

        # Pega as informações de cada obra e coloca na lista que será devolvida.
        for artigo in resultados:
            if len(lista_de_obras) >= limite:
                break

            artigo = artigo or {}

            titulo = artigo.get("title")
            autor = [
                a.get("author", {}).get("display_name")
                for a in artigo.get("authorships", [])
            ]
            tipo = artigo.get("type")
            loc = artigo.get("primary_location") or {}
            source = loc.get("source") or {}
            editora = source.get("display_name")
            ano = artigo.get("publication_year")
            palavra_chave = [
                kw.get("display_name")
                for kw in artigo.get("keywords", [])
            ]
            url = artigo.get("pdf_url")

            if not url:
                pl = artigo.get("primary_location", {})
                url = pl.get("pdf_url")

            if not url:
                for loc in artigo.get("locations", []):
                    if loc.get("pdf_url"):
                        url = loc["pdf_url"]
                        break

            texto_kw = "; ".join(palavra_chave) if palavra_chave else ""

            lista_de_obras.append({
                "Fonte": "OpenAlex",
                "Título": titulo,
                "Autores": "; ".join(autor) if autor else "",
                "Tipo de Obra": tipo,
                "Editora": editora,
                "Ano": ano,
                "Palavras-chave": texto_kw,
                "Texto" : titulo + "; " + texto_kw, # Essa parte é necessária para a mineração de dados
                "Link" : url
            })

            barra.update(1)

        meta = dados.get("meta", {})
        next_cursor = meta.get("next_cursor")
        if not next_cursor:
            break
        parametros["cursor"] = next_cursor

    barra.close()
    return lista_de_obras

if __name__ == '__main__':
    r = scraper_openalex("data mining", limite=7)
    print(len(r))


 