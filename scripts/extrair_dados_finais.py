import requests
import pandas as pd
import time

MAILTO = "seuemail@exemplo.com"
BASE_URL = "https://api.openalex.org/works"

# Busca a frase exata no título/resumo — não busca de texto completo,
# não usa buckets de tópicos genéricos. Isso é o que garantiu os
# resultados relevantes no teste.
FILTER = (
    'title_and_abstract.search:"open science"|"ciência aberta"|"scientific communication",'
    "publication_year:2015-2026,"
    "type:article"
)

MAX_RESULTS = 10000  # número de TRABALHOS (não de autorias) a coletar


def eh_ciencia_da_informacao(primary_topic):
    """Sinaliza se o tópico principal do trabalho está na área de
    Ciência da Informação / Biblioteconomia — útil para destacar ou
    filtrar esses trabalhos no dashboard, sem excluir os demais."""
    if not primary_topic:
        return False
    subfield = (primary_topic.get("subfield") or {}).get("display_name", "") or ""
    field = (primary_topic.get("field") or {}).get("display_name", "") or ""
    termos = ["information", "library"]
    texto = (subfield + " " + field).lower()
    return any(t in texto for t in termos)


def extract_authorships(work):
    rows = []
    work_id = work.get("id") or ""
    title = work.get("title") or "N/A"
    year = work.get("publication_year") or ""
    pub_date = work.get("publication_date") or ""
    language = work.get("language") or "N/A"
    cited = work.get("cited_by_count") or 0
    oa = work.get("open_access") or {}

    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    primary_source = source.get("display_name") or "N/A"

    primary_topic = work.get("primary_topic") or {}
    topico_nome = primary_topic.get("display_name") or "N/A"
    topico_subfield = (primary_topic.get("subfield") or {}).get("display_name", "") or "N/A"
    topico_field = (primary_topic.get("field") or {}).get("display_name", "") or "N/A"
    eh_ci_info = eh_ciencia_da_informacao(primary_topic)

    for a in work.get("authorships", []):
        author = a.get("author") or {}
        institutions = a.get("institutions") or []
        inst_names = [i.get("display_name") or "" for i in institutions]
        inst_countries = [i.get("country_code") or "" for i in institutions if i.get("country_code")]

        rows.append({
            "work_id": work_id,
            "title": title,
            "publication_year": year,
            "publication_date": pub_date,
            "language": language,
            "cited_by_count": cited,
            "is_open_access": oa.get("is_oa") if oa.get("is_oa") is not None else "",
            "open_access_status": oa.get("oa_status") or "N/A",
            "primary_source": primary_source,
            "primary_topic": topico_nome,
            "primary_topic_subfield": topico_subfield,
            "primary_topic_field": topico_field,
            "eh_ciencia_informacao": eh_ci_info,
            "author_name": author.get("display_name") or "N/A",
            "author_id": author.get("id") or "N/A",
            "author_position": a.get("author_position") or "N/A",
            "institution": "; ".join(inst_names) if inst_names else "N/A",
            "country": "; ".join(sorted(set(inst_countries))) if inst_countries else "N/A",
        })
    return rows


def main():
    all_rows = []
    work_ids_seen = set()
    cursor = "*"

    # Primeiro, verifica o total disponível antes de começar a coletar
    check = requests.get(BASE_URL, params={"filter": FILTER, "per-page": 1, "mailto": MAILTO})
    if check.status_code == 200:
        total_disponivel = check.json().get("meta", {}).get("count", 0)
        print(f"Total de trabalhos disponíveis com esse filtro: {total_disponivel}")
        print(f"Coletando até {MAX_RESULTS} trabalhos...\n")
    else:
        print("Aviso: não foi possível verificar o total antes de iniciar.")

    while True:
        params = {
            "filter": FILTER,
            "per-page": 200,
            "cursor": cursor,
            "mailto": MAILTO,
        }
        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print("Erro:", response.status_code, response.text)
            break

        data = response.json()
        results = data.get("results", [])

        for work in results:
            all_rows.extend(extract_authorships(work))
            work_ids_seen.add(work.get("id"))

        print(f"Trabalhos processados: {len(work_ids_seen)} | Autorias coletadas: {len(all_rows)}")

        cursor = data.get("meta", {}).get("next_cursor")

        if not cursor or not results or len(work_ids_seen) >= MAX_RESULTS:
            break

        time.sleep(0.2)

    df = pd.DataFrame(all_rows)
    df.to_csv("../output/openalex_autorias_final.csv", index=False, encoding="utf-8-sig")
    print(f"\nConcluído. {len(df)} autorias de {len(work_ids_seen)} trabalhos salvas em openalex_autorias_final.csv")


if __name__ == "__main__":
    main()