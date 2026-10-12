import pandas as pd

# --- 1. Carregar e diagnosticar ---
df = pd.read_csv("../output/openalex_open_science.csv")

print("Shape:", df.shape)
print("\nValores ausentes (%):")
print((df.isna().sum() / len(df) * 100).round(2))

print("\nDuplicados por work_id:", df["work_id"].duplicated().sum())
print("Duplicados por doi:", df["doi"].dropna().duplicated().sum())

# --- 2. Limpeza básica ---
# Remove duplicados por DOI, mantendo a primeira ocorrência
df = df.drop_duplicates(subset="doi", keep="first")

# Garante tipos corretos
df["publication_year"] = df["publication_year"].astype(int)
df["publication_date"] = pd.to_datetime(df["publication_date"], errors="coerce")

# Preenche textos ausentes com um marcador explícito (evita NaN silencioso em groupby)
for col in ["primary_source", "institutions", "countries", "authors"]:
    df[col] = df[col].fillna("Não informado")

# --- 3. Estatísticas descritivas ---
print("\n=== Distribuição por ano ===")
print(df["publication_year"].value_counts().sort_index())

print("\n=== Distribuição por tipo ===")
print(df["type"].value_counts())

print("\n=== Estatísticas de citações ===")
print(df["cited_by_count"].describe())
print("Mediana:", df["cited_by_count"].median())

print("\n=== Open Access ===")
print(df["open_access_status"].value_counts(normalize=True).round(3) * 100)

# --- 4. Salvar versão limpa ---
df.to_csv("../output/openalex_open_science_limpo.csv", index=False, encoding="utf-8-sig")
print(f"\nSalvo: {len(df)} linhas em openalex_open_science_limpo.csv")