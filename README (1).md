# PostgreSQL AI Assistant 

A production-ready, AI-powered intelligent backend foundation for managing PostgreSQL databases through natural language. This project provides a robust architecture for converting natural language queries into safe, executable SQL queries.

## 🌟 Key Features

- **Natural Language Orchestration**: Seamlessly translates user intent into structured SQL.
- **Multi-Layered Processing**:
  - **Intent Classification**: Identifies if the user wants to query, insert, or modify data.
  - **SQL Generation**: Dynamically builds SQL queries based on identified intent.
  - **Safety Validation**: Security layer to prevent destructive operations (e.g., `DROP`, `TRUNCATE`).
  - **Query Execution**: Executes validated queries against a PostgreSQL instance.
- **Enterprise-Grade Infrastructure**:
  - **Structured Logging**: Uses `structlog` and JSON formatters for observability.
  - **App Factory Pattern**: Flexible and scalable Flask application structure.
  - **Containerized Development**: Fully Dockerized with `docker-compose` for easy setup.
  - **Environment-Based Config**: Clean separation of development, testing, and production environments.

---

## 🏗️ Architecture

The application follows a modular architecture:

1.  **Transport Layer (`app.py`)**: Handles REST API requests and orchestrates the flow.
2.  **Logic Layer (`nlp/`)**: Contains modules for understanding query intent and generating SQL.
3.  **Security Layer (`safety/`)**: Validates generated SQL against a whitelist/blacklist of operations.
4.  **Data Layer (`db/`)**: Manages database connections and query execution.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+, Flask
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Logging**: Structlog, Python-JSON-Logger
- **Containerization**: Docker, Docker Compose
- **Server**: Gunicorn (for production)

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) and Docker Compose installed.
- [Python 3.9+](https://www.python.org/downloads/) (if running locally without Docker).

### Option 1: Running with Docker (Recommended)

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd Bisag
    ```

2.  **Environment Setup**: Create a `.env` file from the template:
    ```bash
    cp .env.example .env  # Or create one manually based on config.py requirements
    ```

3.  **Launch the stack**:
    ```bash
    docker-compose up --build
    ```
    This will start the Flask application on `http://localhost:5000` and a PostgreSQL instance on `5432`.

### Option 2: Running Locally

1.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application**:
    ```bash
    python app.py
    ```

---

## 📡 API Endpoints

### 1. Health Check
`GET /health`
- **Response**: `{"status": "healthy", "version": "1.0.0", ...}`

### 2. Process Query
`POST /api/v1/query`
- **Payload**:
  ```json
  {
    "query": "Show me all users who signed up last month"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "intent": "query_data",
    "sql": "SELECT * FROM users WHERE ...",
    "data": [...],
    "message": "Query processed successfully through all layers."
  }
  ```

---

## 📂 Project Structure

```text
├── db/                 # Database connection and execution logic
├── nlp/                # NLP, Intent classification, and SQL generation
├── safety/             # SQL Validation and Security filters
├── models/             # SQLAlchemy Database Models
├── static/             # Static assets (CSS, JS, Images)
├── templates/          # HTML templates
├── logs/               # Application logs (auto-generated)
├── app.py              # Main application entry point
├── config.py           # Configuration management
├── Dockerfile          # Production Docker configuration
└── docker-compose.yml  # Orchestration for App & DB services
```

---

## 🔒 Security

The system includes a mandatory SQL safety layer. By default, it blocks:
- `DROP` operations
- `TRUNCATE` operations
- (Configurable via `SQL_SAFETY_STRICT_MODE`)

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
