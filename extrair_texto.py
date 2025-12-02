import os
import re
import nltk
from nltk.corpus import stopwords
from pypdf import PdfReader

nltk.download("stopwords")
stopwords_pt = set(stopwords.words("portuguese"))

def extrair_texto(caminho_arquivo):

    leitor = PdfReader(caminho_arquivo)
    texto = ""
    for pagina in leitor.pages:
        texto += pagina.extract_text() or ""

    return texto

def devolver_texto(pasta):

    resultados = {}

    for nome_arquivo in os.listdir(pasta):
        if nome_arquivo.lower().endswith(".pdf"):

            id_obra = nome_arquivo.split('_')[0]

            caminho = os.path.join(pasta, nome_arquivo)
            texto = extrair_texto(caminho)

            resultados[int(id_obra)] = texto

    return resultados

def limpar_texto(texto):

    texto.lower()
    texto = re.sub(r"[^\w\s]", " ", texto)
    texto = re.sub(r"\d+", " ", texto)

    tokens = texto.split()
    tokens = [t for t in tokens if t not in stopwords_pt]

    return " ".join(tokens)

