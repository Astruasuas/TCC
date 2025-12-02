import re
import os
import time
from tqdm import tqdm
import requests
from requests.exceptions import RequestException

def formatar_nome_arquivo(nome,id_obra):

    nome = re.sub(r'[\\/*?:"<>|]', '_', nome)
    nome = f"{id_obra}_{nome}.pdf"
    return nome[:200]

def ver_se_pdf(resposta_http):

    tipo_de_conteudo = resposta_http.headers.get("Content-Type", "").lower()

    if "pdf" in tipo_de_conteudo:
        return True

    url_final = resposta_http.url or ""

    return url_final.lower().endswith('.pdf')

def baixar_pdfs(
        dataframe,
        quantidade_baixar = 13,
        pasta = "pdfs",
        tempo_limite_segundos = 15,
        quantidade_maxima_tentativas = 2
):

    barra = tqdm(desc="Baixando artigos", unit=" artigo")

    if not os.path.exists(pasta):
        os.makedirs(pasta)

    pdfs_salvos = []

    for indice, linha in dataframe.head(quantidade_baixar).iterrows():

        id_obra = linha.get('ID_Obra')
        titulo_obra = linha.get('Título', f'Obra_{indice}')
        link_download = linha.get("Link", None)

        if not isinstance(link_download, str) or link_download.strip() == "":
            print(f'[Ignorar] Linha {indice}: não tem link.')
            continue

        nome_do_arquivo = formatar_nome_arquivo(titulo_obra, id_obra)
        caminho_arquivo = os.path.join(pasta, nome_do_arquivo)

        tentativa = 0

        while tentativa < quantidade_maxima_tentativas:
            tentativa += 1

            try:
                print(f'[Tentativa {tentativa})]. Baixando: {titulo_obra}')

                resposta_http = requests.get(
                    link_download,
                    timeout = tempo_limite_segundos,
                    allow_redirects = True)

                if not ver_se_pdf(resposta_http):
                    print(f"Não retornou PDF, ignorando.")
                    break

                with open(caminho_arquivo, "wb") as arquivo_pdf:
                    arquivo_pdf.write(resposta_http.content)

                pdfs_salvos.append(caminho_arquivo)
                break

            except RequestException as erro:
                print(f'[Erro] Título falhou: {titulo_obra}: {erro}')
                print(f'Aguardando antes de tentar novamente...')
                time.sleep(2)

        else:
            print(f'[Erro] Não foi possível após {quantidade_maxima_tentativas} tentativas')

        barra.update(1)

    barra.close()

    return pdfs_salvos

def main():
    baixar_pdfs("ervo")

if __name__ == '__main__':
    main()











