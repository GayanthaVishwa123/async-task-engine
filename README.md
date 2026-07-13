# Async Task Engine

A robust, high-performance Asynchronous Task Processing Engine built with **FastAPI**, **Celery**, **Redis**, and **MongoDB**. This project demonstrates a production-ready architecture designed to offload heavy, time-consuming background tasks (like notifications and email dispatching) from the main API thread to asynchronous workers, ensuring zero-blocking and high availability.

---

## 🏛️ Architecture Overview

The system architecture is designed for optimal performance by splitting workloads between asynchronous web handling and synchronous background processing:

* **FastAPI (The Brain):** Handles incoming asynchronous client requests. It utilizes `motor` (an async MongoDB driver) via `app/db/mongo_async.py` for non-blocking I/O operations and instantly dispatches background tasks to the broker.
* **Redis (The Message Broker):** Acts as a high-speed message broker/queue, storing tasks sent by FastAPI until they are picked up by a worker.
* **Celery (The Worker):** Operates as an independent background process that executes the actual heavy lifting (e.g., critical notifications). It communicates synchronously with MongoDB using the standard `pymongo` driver via `app/db/mongo_sync.py`.
* **MongoDB (The Data Store):** Stores system event and execution logs inside the `task_audit_logs` collection for tracking and auditing purposes.

---

## 🛠️ Tech Stack

* **Backend Framework:** FastAPI
* **Task Queue & Broker:** Celery & Redis
* **Database:** MongoDB (`motor` for async, `pymongo` for sync)
* **Containerization:** Docker & Docker Compose
* **Cloud Platform:** Microsoft Azure (Container Apps / App Service)
* **CI/CD Automation:** GitHub Actions

---

## 🚀 Getting Started (Local Development)

Follow these steps to set up and run the project locally on your machine.

### 1. Prerequisites
Make sure you have the following installed:
* Python 3.10+
* Docker & Docker Compose

### 2. Clone the Repository
```bash
git clone [https://github.com/GayanthaVishwa123/async-task-engine.git](https://github.com/GayanthaVishwa123/async-task-engine.git)
cd async-task-engine
git checkout dev
### 2. Clone the Repository
```bash
git clone [https://github.com/GayanthaVishwa123/async-task-engine.git](https://github.com/GayanthaVishwa123/async-task-engine.git)
cd async-task-engine
git checkout dev




### 📊 System Architecture Diagram

```mermaid
graph TD
    %% Styling
    classDef github fill:#24292e,stroke:#fff,stroke-width:2px,color:#fff;
    classDef azure fill:#0078d4,stroke:#fff,stroke-width:2px,color:#fff;
    classDef compute fill:#00188f,stroke:#fff,stroke-width:1px,color:#fff;
    classDef database fill:#f25f22,stroke:#fff,stroke-width:1px,color:#fff;

    %% Nodes
    User([🌐 Client / User]) -->|HTTP Requests| FastAPI

    subgraph GitHub_Repo [GitHub Repository]
        Push[Push to dev/main branch] -->|Triggers| GHA[GitHub Actions Pipeline]
    end
    class GitHub_Repo,Push,GHA github;

    subgraph Azure_Cloud [Microsoft Azure Cloud]
        GHA -->|1. Runs IaC| Bicep[Azure Bicep Templates]
        Bicep -->|Provisions| ACA_Env

        GHA -->|2. Builds & Pushes Docker Images| ACR[Azure Container Registry]
        ACR -->|Pulls Images| ACA_Env

        subgraph ACA_Env [Azure Container Apps Environment]
            FastAPI[🚀 FastAPI Web App <br> Ingress: Public]
            Celery[⚙️ Celery Task Worker <br> Ingress: None]
        end
        class ACA_Env,FastAPI,Celery compute;

        subgraph Data_Layer [Managed Data & Broker Layer]
            Redis[(🧠 Azure Cache for Redis <br> Message Broker)]
            Cosmos[(🗄️ Azure Cosmos DB <br> MongoDB API)]
        end
        class Data_Layer,Redis,Cosmos database;

        FastAPI -->|3. Enqueues Task| Redis
        Redis -->|4. Fetches Task| Celery
        Celery -->|5. Writes Audit Logs| Cosmos
        FastAPI -.->|Async Reads/Writes| Cosmos
    end
    class Azure_Cloud,Bicep,ACR azure;
