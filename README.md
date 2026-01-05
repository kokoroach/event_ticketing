# Event Ticketing System

A full-stack event ticketing platform that enables event creation, ticket purchasing, and dynamic payment management.

---

## 🚀 Project Overview

This system enables event organizers to manage events and tickets while allowing users to purchase tickets with flexible payment like that of **EventBrite** and **TicketMaster**.

### 📌 Features

1. Event creation and management
2. Ticket inventory and reservation
3. Dynamic pricing and payment handling
4. Secure and validated API requests
5. Decoupled domain logic from infrastructure
6. Fully containerized development environment

---

## 🏗️ Architecture Overview

The project follows **Clean** and **Hexagonal Architecture** combined ensuring that:

1. The domain layer contains only business rules
2. The application layer coordinates use cases
3. The infrastructure layer handles external concerns (DB, web, payment providers)
4. Dependencies always point inward

Other implementations:

1. **Unit of Work Pattern** - Ensures Transaction and consistency management of data
2. **Deployment** - Containerization and local orchestration via Docker

---

## 🧱 Tech Stack

| Layer      | Technology           | Purpose                                       |
| ---------- | -------------------- | --------------------------------------------- |
| Backend    | **Python (FastAPI)** | High-performance async-based API framework    |
| Frontend   | **ReactJS**          | Interactive user interface                    |
| Validation | **Pydantic**         | Request/response validation and data modeling |
| Database   | **PostgreSQL**       | Relational data storage                       |
| ORM / DB   | **SQLAlchemy**       | Database interaction                          |

---

## ⚙️ Setup Instructions

### Setting up Backend

1. Create a local copy

```
git clone https://github.com/kokoroach/event_ticketing
cd event-ticketing-system
```

2. Update placeholder env file

```
cp .env.sample .env
```

3. Initialize pre-commit hook

```
pre-commit install
```

4. Setup environment

```
cd ./backend && uv sync
```

### Running Backend

1. Run local database instance

```
cd <project_root_dir>
docker-compose up -d
```

2. Run backend service

```
cd backend/
uvicorn app.main:api --reload
```

3. Check available APIs

```
http://127.0.0.1:8000/docs
```

4. Run test suites

```
cd ./backend/
pytest ./tests
```

---

### Setting up Frontend

1. Install dependencies

```
npm install
```

### Running Frontend

1. Run dev instance of React

```
cd ./frontend/app

npm run dev
```
