import requests

MAILTO = "seuemail@exemplo.com"

termos_busca = ["open science", "scientific communication", "open access"]

for termo in termos_busca:
    print("=" * 70)
    print(f"RESULTADOS PARA: '{termo}'")
    print("=" * 70)

    response = requests.get(
        "https://api.openalex.org/topics",
        params={"search": termo, "per-page": 10, "mailto": MAILTO}
    )

    if response.status_code != 200:
        print("Erro:", response.status_code)
        continue

    data = response.json()
    for topic in data.get("results", []):
        topic_id = topic.get("id", "").replace("https://openalex.org/", "")
        nome = topic.get("display_name", "")
        works_count = topic.get("works_count", 0)
        subfield = (topic.get("subfield") or {}).get("display_name", "")
        field = (topic.get("field") or {}).get("display_name", "")

        print(f"\nID: {topic_id}")
        print(f"Nome: {nome}")
        print(f"Subfield: {subfield} | Field: {field}")
        print(f"Trabalhos indexados: {works_count:,}")

    print()