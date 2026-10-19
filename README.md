# Asynchronous AI-Powered ETL Pipeline

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Pydantic AI](https://img.shields.io/badge/Pydantic_AI-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://ai.pydantic.dev/)
[![Celery](https://img.shields.io/badge/Celery-37B24D?style=for-the-badge&logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

A production-grade, asynchronous ETL (Extract, Transform, Load) pipeline engineered to ingest messy, unstructured data streams (e.g., Zendesk support webhooks, app reviews, customer feedback), enforce strict data contracts using **Pydantic AI**, redact sensitive PII, and guarantee **idempotent persistence** into PostgreSQL.

---

## 📌 Architecture Overview

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#1e293b',
    'primaryTextColor': '#f8fafc',
    'primaryBorderColor': '#38bdf8',
    'lineColor': '#38bdf8',
    'secondaryColor': '#0f172a',
    'tertiaryColor': '#334155'
  }
}}%%

graph TD
    %% Styling Classes
    classDef client fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#f8fafc,rx:8,ry:8;
    classDef api fill:#1e293b,stroke:#06b6d4,stroke-width:2px,color:#f8fafc,rx:8,ry:8;
    classDef broker fill:#312e81,stroke:#818cf8,stroke-width:2px,color:#f8fafc,rx:8,ry:8;
    classDef worker fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#f8fafc,rx:8,ry:8;
    classDef monitor fill:#701a75,stroke:#e879f9,stroke-width:2px,color:#f8fafc,rx:8,ry:8;
    classDef db fill:#451a03,stroke:#fb923c,stroke-width:2px,color:#f8fafc,rx:8,ry:8;

    subgraph Client ["🌐 Client Layer"]
        Webhook["📥 External Webhooks<br/>(Zendesk, Apps, Support)"]:::client
    end

    subgraph Ingestion ["⚡ Ingestion Gateway"]
        FastAPI["🚀 FastAPI Endpoint<br/>• SHA-256 Hashing<br/>• Payload Validation<br/>• Task Dispatcher"]:::api
    end

    subgraph Broker ["📦 Message Broker & State"]
        Redis["⚡ Redis<br/>• Celery Message Broker<br/>• Task Queue & Backends"]:::broker
    end

    subgraph Workers ["🧠 Async AI Transform Engine"]
        Celery["⚙️ Celery Workers<br/>(Concurrent Processing)"]:::worker
        PydanticAI["🤖 Pydantic AI Agent<br/>• Structured Extraction<br/>• PII Anonymization<br/>• Sentiment Analysis"]:::worker
        Celery ==>|Executes Task| PydanticAI
    end

    subgraph Monitoring ["📊 System Observability"]
        Flower["📈 Flower Dashboard<br/>• Real-time Worker UI<br/>• Task Monitoring"]:::monitor
    end

    subgraph Storage ["💾 Persistent Storage"]
        Postgres[(🐘 PostgreSQL / SQLModel<br/>• Idempotent Upserts<br/>• Clean Structured Data)]:::db
    end

    %% Flow Connections with Styling
    Webhook ==>|HTTP POST JSON| FastAPI
    FastAPI -->|1. Idempotency Check| Postgres
    FastAPI ==>|2. Enqueue Payload| Redis
    Redis ==>|3. Consume Task| Celery
    Flower -.->|Inspects & Tracks| Redis
    PydanticAI -->|4. Persist Clean Data| Postgres

    linkStyle default stroke:#38bdf8,stroke-width:2px,fill:none;
```

---

## 🚀 Key Engineering Features

1. **Deterministic Data Contracts (Transform Layer)**
   * Utilizes **Pydantic AI** to turn non-deterministic LLM responses into strictly validated JSON schemas.
   * Automatic retry loops handle model format hallucinations before persisting data to storage.

2. **PII Anonymization & Security**
   * Automatically detects and redacts Personally Identifiable Information (names, emails, phone numbers) at the transform stage to maintain data privacy compliance.

3. **Idempotency via SHA-256 Payload Hashing**
   * Webhooks regularly retry upon network failure. To prevent duplicate database records, the ingestion engine generates a unique SHA-256 fingerprint from payload metadata and raw text (`ON CONFLICT DO NOTHING`).

4. **Async Queue & Decoupled Execution**
   * Heavy LLM calls are offloaded from FastAPI request-response cycles to **Celery** workers using **Redis** as a message broker, ensuring high API throughput.

5. **Real-time Observability**
   * Integrated **Flower** dashboard to monitor task queues, worker concurrency, throughput rates, and retry failures in real time.

---

## 🛠️ Tech Stack

* **API Ingestion:** FastAPI (Python 3.11+)
* **Task Queue & Broker:** Celery, Redis
* **AI Transformation & Extraction:** Pydantic AI, Pydantic v2
* **Database & ORM:** PostgreSQL, SQLModel / SQLAlchemy
* **Monitoring UI:** Flower
* **Containerization:** Docker, Docker Compose

---

## ⚡ Quick Start (Local Setup)

### Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Git](https://git-scm.com/)

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/fastapi-pydantic-ai-etl.git
cd fastapi-pydantic-ai-etl
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=feedback_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run with Docker Compose
Spin up all microservices (FastAPI, Postgres, Redis, Celery Worker, Flower):
```bash
docker compose up --build -d
```

### 4. Service Endpoints
* **FastAPI Docs:** `http://localhost:8000/docs`
* **Flower Monitoring:** `http://localhost:5555`
* **PostgreSQL:** `localhost:5432`

---

## 🧪 Example Request

Send a raw, messy customer feedback payload via curl:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/feedback' \
  -H 'Content-Type: application/json' \
  -d '{
  "source_id": "TICK-99482",
  "channel": "zendesk_webhook",
  "raw_text": "URGENT! My payment failed for subscription ID 4481. My name is John Doe, call me at 555-0199 or john@example.com ASAP! Fix this app crash!"
}'
```

### Processed Output (Persisted in PostgreSQL):
```json
{
  "id": 1,
  "source_id": "TICK-99482",
  "payload_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "sanitized_text": "URGENT! My payment failed for subscription ID 4481. My name is [REDACTED], call me at [REDACTED] or [REDACTED] ASAP! Fix this app crash!",
  "category": "Billing & Payments",
  "sentiment": "Negative",
  "urgency": "High",
  "extracted_keywords": ["payment failed", "app crash", "subscription"],
  "created_at": "2026-10-19T08:00:00Z"
}
```

---
