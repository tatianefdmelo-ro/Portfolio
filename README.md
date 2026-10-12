# Cartografia Feminina na Ciência Aberta

Mapeamento da produção, das instituições e das redes de colaboração de mulheres pesquisadoras no campo da Ciência Aberta (2015–2026), com dados extraídos do [OpenAlex](https://openalex.org).

**Dashboard interativo e site do projeto:** https://tatianefdmelo-ro.github.io/Cartografia_Feminina_Ciencia_Aberta/
<!-- EDITAR: troque pelo endereço real do seu GitHub Pages -->

---

## Sobre o projeto

O projeto investiga a presença de mulheres na produção científica sobre **Ciência Aberta, Acesso Aberto e Comunicação Científica**, com recorte em Ciência da Informação. As perguntas que orientam a análise:

1. Quantos trabalhos foram publicados entre 2015 e 2026?
2. Quantas pesquisadoras únicas atuam nesse campo?
3. Quais instituições mais produzem conhecimento sobre Ciência Aberta?
4. Que fração desses artigos é, de fato, de acesso aberto?
5. Como se conectam as pesquisadoras que publicam juntas (coautoria)?
6. Quais temas mais aparecem (Open Science, Ciência Aberta, Open Access, Scientific Communication)?
7. Quem são as pesquisadoras com maior produção?
8. A produção feminina é consistente ao longo dos anos?

## Fontes de dados

O levantamento inicial considerou **Brapci, SciELO e Web of Science**. O projeto passou a usar o **OpenAlex** como base principal porque ele é aberto, tem cobertura global, oferece API pública (sem assinatura institucional) e traz metadados estruturados de autoria, instituição, país e status de acesso aberto, o que permite que todo o pipeline seja reproduzido por qualquer pessoa.

## Metodologia

- **Busca:** artigos (`type:article`) publicados entre 2015 e 2026 que contenham "open science", "ciência aberta", "scientific communication" ou "open access" no título ou resumo.
- **Estrutura dos dados:** uma linha por autoria (autor × trabalho), com a instituição e o país de cada autor ligados individualmente.
- **Temas:** cada trabalho é classificado pela presença literal dos quatro termos no título/resumo (o resumo é reconstruído a partir do índice invertido do OpenAlex). Um trabalho pode ter mais de um tema.
- **Ciência da Informação:** a coluna `eh_ciencia_informacao` indica se o tópico principal do trabalho, segundo a classificação do OpenAlex, pertence a Ciência da Informação / Biblioteconomia. É independente dos temas acima.
- **Gênero:** inferido a partir do primeiro nome com a biblioteca [`gender-guesser`](https://pypi.org/project/gender-guesser/).

## ⚠️ Limitações

- **O gênero é inferido, não declarado.** A inferência por nome erra, principalmente em nomes unissex ou de origens pouco representadas na biblioteca, e não reconhece pessoas não binárias. Os resultados devem ser lidos como estimativas.
- Parte dos trabalhos fica como "Não classificado" quando o resumo não está disponível no OpenAlex.
- A queda aparente de produção nos anos mais recentes (2025–2026) provavelmente reflete a defasagem de indexação, não necessariamente uma redução real.
- Pesquisadoras com mais de uma afiliação podem gerar pequenas duplicações na contagem de instituições.
- O corpus reflete o que está indexado no OpenAlex, não toda a produção científica mundial.

## Estrutura do repositório

```
├── scripts/      → scripts Python de extração, limpeza e redes
├── output/       → arquivos CSV finais (usados no Power BI)
├── dashboard/    → arquivo .pbix do Power BI (opcional)
├── index.html    → página do site (GitHub Pages)
└── README.md
```

## Como reproduzir

1. Instale as dependências:
   ```
   pip install requests pandas gender-guesser
   ```
2. Nos scripts de extração, troque o valor de `MAILTO` pelo seu e-mail (o OpenAlex usa esse dado para identificar quem consulta a API).
3. Dentro da pasta `scripts/`, rode nesta ordem:
   ```
   python extrair_dados_tematizado.py
   python limpar_e_inferir_genero_tematizado.py
   python gerar_rede_instituicoes.py
   python gerar_rede_colaboracao_feminina.py
   ```
4. Os arquivos gerados ficam em `output/`. Abra o `.pbix` no Power BI Desktop e aponte as fontes de dados para eles.

## Autoria

Desenvolvido por **Tatiane Ferro de Melo** como projeto de portfólio em análise de dados.
<!-- EDITAR: coloque seu nome e, se quiser, links do LinkedIn/Lattes -->
