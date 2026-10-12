import requests
import pandas as pd
import time

MAILTO = "seuemail@exemplo.com"
BASE_URL = "https://api.openalex.org/works"
SEARCH_TERMS = "open science OR scientific communication"
FILTER = "publication_year:2015-2026"
MAX_RESULTS = 5000  # número de TRABALHOS (não de autorias) a coletar


def extract_authorships(work):
    rows = []
    work_id = work.get("id") or ""
    title = work.get("title") or ""
    year = work.get("publication_year") or ""
    cited = work.get("cited_by_count") or 0
    oa = work.get("open_access") or {}

    for a in work.get("authorships", []):
        author = a.get("author") or {}
        institutions = a.get("institutions") or []
        inst_names = [i.get("display_name") or "" for i in institutions]
        inst_countries = [i.get("country_code") or "" for i in institutions if i.get("country_code")]

        rows.append({
            "work_id": work_id,
            "title": title,
            "publication_year": year,
            "cited_by_count": cited,
            "is_open_access": oa.get("is_oa") if oa.get("is_oa") is not None else "",
            "open_access_status": oa.get("oa_status") or "N/A",
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

    while True:
        params = {
            "search": SEARCH_TERMS,
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
    df.to_csv("../output/openalex_autorias.csv", index=False, encoding="utf-8-sig")
    print(f"\nConcluído. {len(df)} autorias de {len(work_ids_seen)} trabalhos salvas em openalex_autorias.csv")


if __name__ == "__main__":
    main()