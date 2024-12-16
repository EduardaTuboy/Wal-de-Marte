# Wal-de-Marte

Repositório do trabalho final da disciplina de Análise
e projeto orientados a objetos, ICMC-USP, 2024

Realizado pelos alunos:

- Felipe Carneiro Machado - 14569373

- Eduarda Tuboy Nardin - 13732495

- Gabriel Barbosa dos Santos - 14613991

- Augusto Cavalcante Barbosa Pereira - 14651531

## Requisitos

Este projeto requer o PostgresSQL, o python3 e as bibliotecas python Django e psycopg2 (driver do postgres).

O PostgresSQL deve ser instalado através de um gerenciador de pacotes ou do seu site.

As dependências python devem ser instaladas a partir do requirements.txt.

## Como rodar

Os comandos a seguir assumem um ambiente linux com a shell bash, utilizando o diretório raiz
desse projeto como diretório de trabalho

Primeiro é necessário configurar o ambiente virtual e baixar as dependências
```bash
python3 -m venv .
pip install -r requirements.txt
```

Antes de iniciar o servidor, é preciso configurar o banco de dados,
através do PgAdmin ou interface de terminal do PostgreSQL, crie a database com o nome "waldemarte_db"

```sql
CREATE DATABASE waldemarte_db;
```

O Django cria as tabelas com os comandos:

```bash
python waldemarte/manage.py makemigrations
python waldemarte/manage.py migrate
```
Agora, o servidor tem tudo que precisa para rodar, ele é iniciado com um banco de produtos de teste. 
Execute o seguinte comando para o servidor começar a executar:

```bash
python waldemarte/manage.py runserver
```


