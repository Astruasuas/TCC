import requests
from tqdm import tqdm

def scraper_openalex(busca, limite=100):
    url = "https://api.openalex.org/works"
    lista_de_obras = []

    per_page = 50 if limite > 50 else limite

    parametros = {
        "search": busca,
        "filter": "is_oa:true",
        "per_page": per_page,
        "cursor": "*",
        "mailto": "seuemail@email.com"
    }

    barra = tqdm(desc="Coletando obras", unit=" artigo")

    while len(lista_de_obras) < limite:
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
                "Texto" : titulo + "; " + texto_kw,
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
#nota para o eu de amanhã: verificar o bgl de open access e link direto pra pdf



 
