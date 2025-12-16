from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def minerar(df):

    df = df.copy()

    perfil = df["Interesses"].iloc[0]
    textos_obras = df["Texto"].fillna("").tolist()

    vectorizer = TfidfVectorizer(stop_words=["portuguese", "english"])
    matriz = vectorizer.fit_transform(textos_obras + [perfil])

    vetor_perfil = matriz[-1]
    vetor_obras = matriz[:-1]

    similaridades = cosine_similarity(vetor_perfil, vetor_obras)[0]
    df["similaridade"] = similaridades

    df = df.sort_values("similaridade", ascending=False)

    return df

def main():
    minerar('df')

if __name__ == "__main__":
    main()