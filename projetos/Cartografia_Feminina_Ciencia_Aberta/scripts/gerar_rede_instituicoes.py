import pandas as pd
from itertools import combinations
from collections import defaultdict

# --- 1. Carregar dados de autorias ---
# keep_default_na=False evita que o pandas transforme o texto "N/A" (que nós
# mesmos escrevemos no CSV) de volta em um valor nulo real ao ler o arquivo.
df = pd.read_csv("../output/openalex_autorias_limpo.csv", keep_default_na=False)

# Explode instituições: cada autor pode ter mais de uma, separadas por "; "
df["institution"] = df["institution"].astype(str)
df_exp = df.assign(institution=df["institution"].str.split("; ")).explode("institution")
df_exp["institution"] = df_exp["institution"].astype(str).str.strip()

# Remove qualquer variação de valor ausente, por segurança
valores_invalidos = {"N/A", "", "nan", "None", "NA", "null"}
df_exp = df_exp[~df_exp["institution"].isin(valores_invalidos)]
df_exp = df_exp.dropna(subset=["institution"])

# --- 2. Métricas básicas por instituição ---
trabalhos_por_inst = df_exp.groupby("institution")["work_id"].nunique().rename("total_trabalhos")
citacoes_por_inst = df_exp.groupby("institution")["cited_by_count"].sum().rename("total_citacoes")

# --- 3. Colaboração: pares de instituições que aparecem no mesmo work_id ---
colaboradores = defaultdict(set)

for work_id, grupo in df_exp.groupby("work_id"):
    instituicoes_unicas = sorted(set(str(x) for x in grupo["institution"].unique()))
    if len(instituicoes_unicas) > 1:
        for a, b in combinations(instituicoes_unicas, 2):
            colaboradores[a].add(b)
            colaboradores[b].add(a)

num_colaboradores = pd.Series(
    {inst: len(parceiros) for inst, parceiros in colaboradores.items()},
    name="num_instituicoes_parceiras"
)

# --- 4. Combinar tudo em uma tabela final ---
resultado = pd.concat([trabalhos_por_inst, citacoes_por_inst, num_colaboradores], axis=1)
resultado["num_instituicoes_parceiras"] = resultado["num_instituicoes_parceiras"].fillna(0).astype(int)
resultado = resultado.reset_index().rename(columns={"institution": "instituicao"})

# --- 5. Classificar centralidade (para colorir no gráfico) ---
def classificar_centralidade(n):
    if n >= resultado["num_instituicoes_parceiras"].quantile(0.85):
        return "Alta centralidade"
    elif n >= resultado["num_instituicoes_parceiras"].quantile(0.50):
        return "Média centralidade"
    else:
        return "Baixa centralidade"

resultado["centralidade"] = resultado["num_instituicoes_parceiras"].apply(classificar_centralidade)

# --- 6. Ordenar e salvar ---
resultado = resultado.sort_values("total_trabalhos", ascending=False)

print("Total de instituições:", len(resultado))
print()
print(resultado.head(15).to_string(index=False))

resultado.to_csv("../output/rede_instituicoes.csv", index=False, encoding="utf-8-sig")
print("\nSalvo: rede_instituicoes.csv")