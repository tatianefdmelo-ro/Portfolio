import requests
import pandas as pd
import time

MAILTO = "seuemail@exemplo.com"  # troque pelo seu email

BASE_URL = "https://api.openalex.org/works"

SEARCH_TERMS = "open science AND scientific communication"
FILTER = "publication_year:2015-2026"

MAX_RESULTS = 5000  # aumente depois que confirmar que está tudo certo


def extract_work_data(work):
    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    open_access = work.get("open_access") or {}

    authorships = work.get("authorships", [])
    author_names = []
    author_ids = []
    institutions = []
    countries = []

    for a in authorships:
        author = a.get("author") or {}
        author_names.append(author.get("display_name") or "")
        author_ids.append(author.get("id") or "")
        for inst in a.get("institutions") or []:
            institutions.append(inst.get("display_name") or "")
            if inst.get("country_code"):
                countries.append(inst.get("country_code"))

    return {
        "work_id": work.get("id") or "",
        "doi": work.get("doi") or "",
        "title": work.get("title") or "",
        "publication_year": work.get("publication_year") or "",
        "publication_date": work.get("publication_date") or "",
        "type": work.get("type") or "",
        "language": work.get("language") or "",
        "cited_by_count": work.get("cited_by_count") or 0,
        "is_open_access": open_access.get("is_oa") if open_access.get("is_oa") is not None else "",
        "open_access_status": open_access.get("oa_status") or "",
        "primary_source": source.get("display_name") or "",
        "authors": "; ".join(author_names),
        "author_ids": "; ".join(author_ids),
        "institutions": "; ".join(sorted(set(institutions))),
        "countries": "; ".join(sorted(set(countries))),
    }


def main():
    all_rows = []
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
            all_rows.append(extract_work_data(work))

        print(f"Coletados até agora: {len(all_rows)}")

        cursor = data.get("meta", {}).get("next_cursor")

        if not cursor or not results or len(all_rows) >= MAX_RESULTS:
            break

        time.sleep(0.2)

    df = pd.DataFrame(all_rows)
    df.to_csv("../output/openalex_open_science.csv", index=False, encoding="utf-8-sig")
    print(f"\nConcluído. {len(df)} trabalhos salvos em output/openalex_open_science.csv")


if __name__ == "__main__":
    main()