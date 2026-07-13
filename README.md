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
* **Environment Management:** Pydantic Settings

---

## 🚀 Getting Started

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
