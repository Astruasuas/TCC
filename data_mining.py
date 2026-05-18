"""
Esse script faz a mineração dos dados e calcula a similaridade com os gostos do perfil do usuário.
Função das bibliotecas:

TfidVectorizer --> Converte os textos em vetores usando TF-IDF
cosine_similarity --> Calcula a similaridade dos vetores
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def minerar(df):

    df = df.copy()

    perfil = df["Interesses"].iloc[0]
    textos_obras = df["Texto"].fillna("").tolist()

    # Vetorização
    vectorizer = TfidfVectorizer(stop_words=["portuguese", "english"])
    matriz = vectorizer.fit_transform(textos_obras + [perfil])

    vetor_perfil = matriz[-1]
    vetor_obras = matriz[:-1]

    # Calculo de similaridade
    similaridades = cosine_similarity(vetor_perfil, vetor_obras)[0]
    df["similaridade"] = similaridades

    df = df.sort_values("similaridade", ascending=False)

    return df

def main():
    minerar('df')

if __name__ == "__main__":
    main()