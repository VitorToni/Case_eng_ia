# Projeto Pessoal de um Engenheiro de Dados e entusiasta em IA
Esse projeto foi criado em Abril de 2024 com o intuito de utilizar e estudar ferramentas de engenharia de dados.
Esta presente:

* Dependências e requisitos automatizados
* Consumo de dados via API
* Ingestão, armazenamento e consulta com DuckDB
* Gen IA para insights (Grátis com o Google Gemini)
* Uso de streamlit para aplicação web


Estrutura:

```
Case_eng_ia/
├── duckdb/
├── infra/
│   ├── instalar_dependencias.py
│   └── requirements.txt
├── src/
│   ├── funcs_duckdb.py
│   ├── funcs_ia.py
│   └── interface.py
└── main.py
```


Melhorias mapeadas: 

* Dependências com poetry
* Logging mais robusto
* Orquestrar com Airflow
