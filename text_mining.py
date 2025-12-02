from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def minerar_textos(textos_limpos, perfil_texto, df_obras):
    ids = list(textos_limpos.keys())
    corpus = list(textos_limpos.values()) + [perfil_texto]

    vectorizer = TfidfVectorizer()
    matriz = vectorizer.fit_transform(corpus)

    vetor_obras = matriz[:-1]
    vetor_perfil = matriz[-1]

    similaridades = cosine_similarity(vetor_perfil, vetor_obras)[0]

    df_obras["similaridade"] = similaridades

    return df_obras.sort_values("similaridade", ascending=False)
