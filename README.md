# Course Recommendation Python Microservice

This microservice is responsible for vectorizing raw course data, interacting with a Qdrant vector database, and recommending courses based on provided input. It is designed to work as part of a larger system, communicating with a Java Spring backend via RESTful APIs.

## Features

- Accepts and vectorizes course data for storage in Qdrant.
- Processes student input to generate personalized course recommendations.
- Exposes REST API endpoints for integration with other backend services.
- Built with Flask for easy deployment and scalability.
- Designed for integration with a Java Spring backend (secured with JWT).

## Installation

### Prerequisites

- Python 3.8 or higher
- [Qdrant](https://qdrant.tech/) instance (cloud or local)
- Java Spring backend (for complete system integration)

### Setup

```bash
git clone https://github.com/Ed-Harutyunyan/Course-Recommendation-Python-Microservice.git
cd Course-Recommendation-Python-Microservice
pip install -r requirements.txt
```

### Running the Service

```bash
python run.py
```

- The service defaults to port 5000. To change the port, update `config.py`.
- Ensure port 5000 is free or change it as needed.

## API Reference

### 1. Vectorize Courses

Vectorizes and stores courses in Qdrant.

**Endpoint:**
```
PUT /api/vectorize
```


- Example usage: Send a PUT request from the backend to `http://localhost:5000/api/vectorize`

### 2. Recommend Courses

Returns recommended courses based on student input.

**Endpoint (Java Backend):**
```
POST http://localhost:8080/api/course/recommendations
```

- JWT authentication required via request headers.
- Example usage: Backend sends a POST request with proper JWT token.

| Parameter | Type   | Description                            |
|-----------|--------|----------------------------------------|
| headers   | string | **Required**. JWT token for auth       |

## Configuration

- API settings and database connection details should be configured in `config.py`.


## License

[MIT License](LICENSE)

---

*This project is maintained by Ed-Harutyunyan. For questions or support, please open an issue on GitHub.*