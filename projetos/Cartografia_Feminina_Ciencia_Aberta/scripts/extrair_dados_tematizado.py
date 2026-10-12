import requests
import pandas as pd
import time
import re

MAILTO = "seuemail@exemplo.com"
BASE_URL = "https://api.openalex.org/works"

FILTER = (
    'title_and_abstract.search:"open science"|"ciência aberta"|"scientific communication"|"open access",'
    "publication_year:2015-2026,"
    "type:article"
)

MAX_RESULTS = 10000  # número de TRABALHOS (não de autorias) a coletar

# Termos que definem SEUS temas — verificados diretamente no título/resumo,
# não na classificação genérica do OpenAlex.
TEMAS = {
    "Open Science": [r"open science"],
    "Ciência Aberta": [r"ci[êe]ncia aberta"],
    "Open Access": [r"open access"],
    "Scientific Communication": [r"scientific communication", r"comunica[çc][ãa]o cient[íi]fica"],
}


def reconstruir_abstract(inverted_index):
    """Reconstrói o resumo a partir do índice invertido que o OpenAlex usa
    para economizar espaço (palavra -> lista de posições no texto)."""
    if not inverted_index:
        return ""
    posicoes = {}
    for palavra, idxs in inverted_index.items():
        for i in idxs:
            posicoes[i] = palavra
    if not posicoes:
        return ""
    max_pos = max(posicoes.keys())
    palavras = [posicoes.get(i, "") for i in range(max_pos + 1)]
    return " ".join(palavras)


def classificar_temas(titulo, abstract):
    """Classifica o trabalho pelos SEUS 4 termos de interesse (regex sobre
    título + resumo) — não pela classificação de Topics do OpenAlex."""
    texto = f"{titulo} {abstract}".lower()
    temas_encontrados = []
    for tema, padroes in TEMAS.items():
        if any(re.search(p, texto) for p in padroes):
            temas_encontrados.append(tema)
    return temas_encontrados if temas_encontrados else ["Não classificado"]


def eh_ciencia_da_informacao(primary_topic):
    """Sinaliza se o TÓPICO PRINCIPAL do trabalho (classificação própria do
    OpenAlex, baseada no assunto geral do artigo) pertence à área de Ciência
    da Informação / Biblioteconomia. Isso é INDEPENDENTE da classificação por
    tema acima — um trabalho pode falar de 'open access' (tema) e ainda assim
    ter como assunto principal genômica, por exemplo."""
    if not primary_topic:
        return False
    subfield = (primary_topic.get("subfield") or {}).get("display_name", "") or ""
    field = (primary_topic.get("field") or {}).get("display_name", "") or ""
    texto = (subfield + " " + field).lower()
    termos = ["information", "library"]
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

    abstract = reconstruir_abstract(work.get("abstract_inverted_index"))
    temas = classificar_temas(title, abstract)
    temas_str = "; ".join(temas)

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
            "temas": temas_str,
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

    check = requests.get(BASE_URL, params={"filter": FILTER, "per-page": 1, "mailto": MAILTO})
    if check.status_code == 200:
        total_disponivel = check.json().get("meta", {}).get("count", 0)
        print(f"Total de trabalhos disponíveis com esse filtro: {total_disponivel}")
        print(f"Coletando até {MAX_RESULTS} trabalhos...\n")

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

    df_trabalhos_unicos = df.drop_duplicates("work_id")
    print("\n=== Distribuição por tema (trabalhos únicos) ===")
    contagem_temas = {}
    for temas_str in df_trabalhos_unicos["temas"]:
        for tema in temas_str.split("; "):
            contagem_temas[tema] = contagem_temas.get(tema, 0) + 1
    for tema, qtd in sorted(contagem_temas.items(), key=lambda x: -x[1]):
        print(f"{tema}: {qtd}")

    print("\n=== Trabalhos em Ciência da Informação (Topics do OpenAlex) ===")
    print(df_trabalhos_unicos["eh_ciencia_informacao"].value_counts())

    df.to_csv("../output/openalex_autorias_tematizado.csv", index=False, encoding="utf-8-sig")
    print(f"\nConcluído. {len(df)} autorias de {len(work_ids_seen)} trabalhos salvas em openalex_autorias_tematizado.csv")


if __name__ == "__main__":
    main()