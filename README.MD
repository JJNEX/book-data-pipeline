# 🚀 Book Data Pipeline

Sistema completo de coleta, processamento e persistência de dados de livros, construído com arquitetura em camadas, scraping automatizado e API REST.

O projeto simula um pipeline de dados real:

```text
Scraper → Parser → Service → Repository → PostgreSQL → API
```

---

# 🧠 Descrição

Este projeto realiza:

- Coleta de dados do site https://books.toscrape.com/
- Processamento e normalização dos dados extraídos
- Persistência em banco de dados PostgreSQL
- Exposição dos dados via API REST (FastAPI)
- Pipeline com processamento paralelo para otimização de scraping
- Execução manual ou via API

---

# ⚙️ Arquitetura

```text
Scraper (Python + Requests)
↓
Parser (extração e limpeza de dados)
↓
Service Layer (regras de negócio)
↓
Repository (persistência no banco)
↓
PostgreSQL
↓
FastAPI (API REST)
```


---

# 🧰 Stack Tecnológica

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker / Docker Compose
- ThreadPoolExecutor (paralelismo)
- Pytest
- Logging estruturado

---

# 🚀 Como rodar o projeto

---

## 🐳 Docker

Subir toda a aplicação (API + banco):

```bash
docker compose up --build -d
```

## 🌐 API

```text
http://localhost:8000/docs
```



## ⚡ Rodar localmente

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned; & ".\venv\Scripts\Activate.ps1"
```

Subir API

```bash
uvicorn app.main:app --reload
```

##  🧪 Testes

```bash
pytest tests/api/test_book.py -v
pytest tests/test_parser.py -v
pytest tests/test_repository.py -v
```

## 🐘 Migrations

Rodar Migration

```bash
docker exec -it books_api alembic upgrade head
```