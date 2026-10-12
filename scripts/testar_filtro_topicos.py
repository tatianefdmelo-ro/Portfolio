import requests

MAILTO = "seuemail@exemplo.com"

# Núcleo: Publicação Acadêmica/Open Access, Comunicação Científica,
# Gestão de Dados de Pesquisa, Ciência da Informação/Bibliotecas
TOPIC_IDS = ["T13607", "T13516", "T11937", "T13673"]

filtro_topicos = "|".join(TOPIC_IDS)

params = {
    "filter": f"topics.id:{filtro_topicos},publication_year:2015-2026",
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
    print(f"{i}. [{ano}] {titulo}")
    print(f"   Tópico principal: {topico_principal}\n")