# Portfólio de dados | Tatiane Ferro de Melo

Site pessoal com meus projetos de análise de dados, visualização e automação. Sou estudante de Arquivologia (UFF) e atuo com Power BI, Power Automate, Copilot Studio e governança da informação.

**Site:** https://github.com/tatianefdmelo-ro/Portfolio

## Projetos

| Projeto | Ferramentas | Descrição |
|---|---|---|
| [Cartografia Feminina na Ciência Aberta](./projetos/Cartografia_Feminina_Ciencia_Aberta/) | Power BI, Python, OpenAlex | Mapeamento da produção científica, das instituições e das redes de colaboração de mulheres pesquisadoras em Ciência Aberta (2015–2026). |
| [Hashtag Eletro: análise de vendas](./projetos/Hashtag_Eletro/) | Power BI, Jupyter Notebook, Python | Análise do desempenho comercial, dos produtos mais vendidos e de oportunidades de melhoria nos resultados. |

## Estrutura do repositório

```text
.
├── index.html                  # página principal (HTML e CSS em um único arquivo)
├── README.md
└── projetos/
    ├── Cartografia_Feminina_Ciencia_Aberta/
    │   └── index.html
    └── Hashtag_Eletro/
        ├── index.html
        └── README.md

## Como publicar no GitHub Pages

1. Envie os arquivos para um repositório no GitHub, com o `index.html` na raiz.
2. Vá em **Settings > Pages**.
3. Em **Build and deployment**, escolha **Deploy from a branch**, selecione a branch `main` e a pasta `/ (root)`.
4. Salve. Em alguns minutos o site fica disponível no endereço indicado na própria página.

## Como editar

- **Textos e projetos:** edite direto o `index.html`. Cada seção tem um `id` (`sobre`, `competencias`, `projetos`, `experiencia`, `formacao`, `contato`).
- **Cores e fontes:** estão nas variáveis CSS no começo do arquivo (`:root`).
- **Novo projeto:** copie um bloco `<article class="project">` dentro da seção `#projetos`, ajuste título, descrição, tags e o link para `./projetos/<nome-da-pasta>/index.html`.

## Tecnologias

HTML e CSS puros, sem framework e sem JavaScript. Fontes Fraunces e Public Sans, carregadas do Google Fonts (há fontes de reserva caso não carreguem).

## Contato

- E-mail: tatianefdmelo@gmail.com
- [LinkedIn](https://www.linkedin.com/in/tatianefdmelo)
- [GitHub](https://github.com/tatianefdmelo-ro)

## Licença

Textos, currículo e identidade visual: todos os direitos reservados. Se quiser permitir o reuso do código, adicione um arquivo `LICENSE` (por exemplo, MIT) e atualize esta seção.
