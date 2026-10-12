import pandas as pd
import gender_guesser.detector as gender

# --- 1. Carregar ---
df = pd.read_csv("../output/openalex_autorias_tematizado.csv", keep_default_na=False)

print("Shape original:", df.shape)

# --- 2. Limpeza ---
df = df.drop_duplicates(subset=["work_id", "author_id"], keep="first")

df["publication_year"] = df["publication_year"].astype(int)
df["cited_by_count"] = df["cited_by_count"].fillna(0).astype(int)

# eh_ciencia_informacao vem como texto "True"/"False" do CSV — converte para booleano real
df["eh_ciencia_informacao"] = df["eh_ciencia_informacao"].astype(str).map({"True": True, "False": False})

colunas_texto = [
    "title", "language", "open_access_status", "primary_source",
    "temas", "primary_topic", "primary_topic_subfield", "primary_topic_field",
    "author_name", "author_id", "author_position", "institution", "country"
]
for col in colunas_texto:
    df[col] = df[col].replace("", "N/A")

# --- 3. Inferência de gênero a partir do primeiro nome ---
d = gender.Detector(case_sensitive=False)

def primeiro_nome(nome_completo):
    if not isinstance(nome_completo, str) or nome_completo.strip() in ("", "N/A"):
        return ""
    return nome_completo.strip().split(" ")[0]

df["primeiro_nome"] = df["author_name"].apply(primeiro_nome)
df["genero_bruto"] = df["primeiro_nome"].apply(lambda n: d.get_gender(n) if n else "unknown")

mapa_genero = {
    "male": "Masculino",
    "mostly_male": "Masculino (provável)",
    "female": "Feminino",
    "mostly_female": "Feminino (provável)",
    "andy": "Ambíguo",
    "unknown": "Não identificado"
}
df["genero_inferido"] = df["genero_bruto"].map(mapa_genero)
df = df.drop(columns=["genero_bruto"])

# --- 4. Estatísticas ---
print("\n=== Distribuição de gênero inferido ===")
print(df["genero_inferido"].value_counts())
print("\n% do total:")
print((df["genero_inferido"].value_counts(normalize=True) * 100).round(1))

print("\n=== Trabalhos únicos por tema ===")
df_unicos = df.drop_duplicates("work_id")
contagem_temas = {}
for temas_str in df_unicos["temas"]:
    for tema in temas_str.split("; "):
        contagem_temas[tema] = contagem_temas.get(tema, 0) + 1
for tema, qtd in sorted(contagem_temas.items(), key=lambda x: -x[1]):
    print(f"{tema}: {qtd}")

print("\n=== Trabalhos em Ciência da Informação (Topics do OpenAlex) ===")
print(df_unicos["eh_ciencia_informacao"].value_counts())

print("\n=== Cruzamento: gênero feminino DENTRO de Ciência da Informação ===")
generos_femininos = ["Feminino", "Feminino (provável)"]
df_ci = df[df["eh_ciencia_informacao"] == True]
print("Trabalhos únicos em Ciência da Informação:", df_ci["work_id"].nunique())
print("Autoras únicas (fem.) em Ciência da Informação:",
      df_ci[df_ci["genero_inferido"].isin(generos_femininos)]["author_id"].nunique())

print("\n=== Resumo geral ===")
print("Autores únicos:", df["author_id"].nunique())
print("Trabalhos únicos:", df["work_id"].nunique())
print("Total de linhas (autorias):", len(df))

# --- 5. Salvar versão final ---
df.to_csv("../output/openalex_autorias_tematizado_limpo.csv", index=False, encoding="utf-8-sig")
print(f"\nSalvo: {len(df)} linhas em openalex_autorias_tematizado_limpo.csv")