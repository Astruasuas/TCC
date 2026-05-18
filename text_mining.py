"""
Esse script faz a mineração dos textos e gera uma nuvem de termos.
Função das bibliotecas:
TfidVectorizer --> Vetorizar os textos
cosine_similarity --> Calcular similaridade
WordCloud --> Gerar nuvem de termos
matplotlib --> Auxiliar o wordcloud
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def gerar_wordcloud(texto):
    wc = WordCloud(width=1200, height=600, background_color="white").generate(texto)

    plt.figure(figsize=(12, 6))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("nuvem.png", dpi=300, bbox_inches="tight")
    plt.close()

def minerar_textos(textos_limpos, perfil_texto, df_obras, wc = True):
    ids = list(textos_limpos.keys())  # Por algum motivo nada funciona se eu tirar isso
    corpus = list(textos_limpos.values()) + [perfil_texto]

    vectorizer = TfidfVectorizer()
    matriz = vectorizer.fit_transform(corpus)

    vetor_obras = matriz[:-1]
    vetor_perfil = matriz[-1]

    similaridades = cosine_similarity(vetor_perfil, vetor_obras)[0]

    df_obras["similaridade"] = similaridades

    if wc:
        corpus_wc = " ".join(textos_limpos.values())
        gerar_wordcloud(corpus_wc)

    return df_obras.sort_values("similaridade", ascending=False)
