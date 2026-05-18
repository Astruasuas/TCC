from TCC.r_brapci import scraper_brapci
from TCC.r_openalex import scraper_openalex
from ontologia import *
from limpeza import *
from data_mining import *
from import_pdf import *
from extrair_texto import *
from text_mining import *
import time
import pandas as pd

inicio = time.time()

termos_pt, termos_en = interesses(pesquisador)

interesse = termos_pt + termos_en
interesse = sum(interesse, [])
interesse_str = "; ".join(interesse)
df_usuario = pd.DataFrame({"Interesses" : [interesse_str]})

obras_brapci = []
obras_oa = []

for termo in termos_pt:
    obras_brapci.append(scraper_brapci(termo, resultados = 5))

for termo in termos_en:
    obras_oa.append(scraper_openalex(termo, limite = 5))

todos_brapci = [obra for lista in obras_brapci for obra in lista]
todos_oa = [obra for lista in obras_oa for obra in lista]

df_brapci = pd.DataFrame(todos_brapci)
df_oa = pd.DataFrame(todos_oa)
df_total = pd.concat([df_brapci, df_oa], ignore_index=True)

df_mineracao = pd.concat([df_total, df_usuario], ignore_index=True)
df_mineracao["Interesses"] = interesse_str
df_mineracao["ID_Obra"] = df_mineracao.index

print("Limpando obras...")
df_mineracao = limpar(df_mineracao)

print("Calculando similaridade dos artigos com o gosto do usuário...")
df_mineracao = minerar(df_mineracao)

baixar_pdfs(df_mineracao)

print("Iniciando mineração dos textos")

texto_pdfs = devolver_texto("pdfs")
textos_limpos = {
    id_obra: limpar_texto(texto)
    for id_obra, texto in texto_pdfs.items()
}

ids_validos = list(textos_limpos.keys())
df_validos = df_mineracao[df_mineracao["ID_Obra"].isin(ids_validos)].copy()

df_minerado = minerar_textos(textos_limpos, interesse_str, df_validos)

fim = time.time()

print(f"Tempo de execução: {fim - inicio:.2f} segundos")

nome = input('Nome do arquivo: ')
df_minerado.to_csv(f"{nome}.csv", index=False, encoding="utf-8")

