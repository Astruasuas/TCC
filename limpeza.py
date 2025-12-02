import pandas as pd
import requests

def limpar(df):

    df = df.copy()

    df.drop_duplicates(subset=['Título'], inplace=True)
    df = df.dropna(subset=['Título','Palavras-chave', 'Autores'])

    df['Autores'] = df['Autores'].apply(
        lambda x: "; ".join([a.strip() for a in str(x).replace(",", ";").split(";")])
    )

    df["Palavras-chave"] = (
        df["Palavras-chave"]
        .astype(str)
        .str.lower()
        .apply(lambda x: "; ".join(
            sorted({
                k.strip()                    
                for k in x.split(";")       
                if k.strip() not in {"", "-", "–", "nan", "none"} 
            })
        ))
    )

    remover = {"", " ", "–", "-", "nan", "none"}
    df["Palavras-chave"] = df["Palavras-chave"].apply(
        lambda x: "; ".join([w for w in x.split(";") if w not in remover])
    )

    df = df[df["Link"].notna() & (df["Link"].str.strip() != "")]

    linhas_validas = []

    for idx, row in df.iterrows():
        link = str(row["Link"]).strip()

        # Ignora vazios
        if not link or link.lower() == "nan":
            continue

        try:
            resp = requests.head(link, timeout=5, allow_redirects=True)

            content_type = resp.headers.get("Content-Type", "").lower()

            if "pdf" in content_type:
                linhas_validas.append(row)

        except Exception:
            continue

    return df

def main():
    limpar('artigos')

if __name__ == '__main__':
    main()




