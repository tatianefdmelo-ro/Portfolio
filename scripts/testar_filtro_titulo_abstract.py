import requests

MAILTO = "seuemail@exemplo.com"

# Busca a frase exata "open science" (ou variações) especificamente no
# título e resumo do trabalho — não no texto completo, não em tópicos
# de infraestrutura de software.
params = {
    "filter": (
        'title_and_abstract.search:"open science"|"ciência aberta"|"scientific communication",'
        "publication_year:2015-2026,"
        "type:article"
    ),
    "per-page": 25,
    "mailto": MAILTO,
}

response = requests.get("https://api.openalex.org/works", params=params)
print("Status:", response.status_code)

data = response.json()
print("Total estimado com esse filtro:", data["meta"]["count"])
print()
print("=== Primeiros 25 títulos (amostra) ===\n")

for i, work in enumerate(data["results"], 1):
    titulo = work.get("title") or "(sem título)"
    ano = work.get("publication_year")
    topico_principal = (work.get("primary_topic") or {}).get("display_name", "N/A")
    citacoes = work.get("cited_by_count", 0)
    print(f"{i}. [{ano}] {titulo}")
    print(f"   Tópico principal: {topico_principal} | Citações: {citacoes}\n")