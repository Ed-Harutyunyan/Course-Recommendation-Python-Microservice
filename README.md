
# Course Recommendation System Python Microservice

Handles the vectorization of the raw data, sends it to Qdrant database and recommende courses with the provided input.


## Features

* Accepts course data for vectorization

* Processes student input to generate course recommendations

* REST API endpoints for communication with the Java Spring backend

* Deployed using Flask


## Installation

Ensure you have Python installed
```bash
  python --version
```

#### Setup

```bash
git clone <Github URL OR SSH>
cd Recommendation_System
```
    
#### install neccessary packages
```bash
pip install -r requirements.txt
```

#### Run 
Execute ` run.py ` file to start the Python Flask Server.
Ensure  that port 5000 is not used by other services. If yes, terminate or change the port in `config.py` file to another open port


## API Reference

#### Update current vectorized courses

Receives the courses from backend, vectorizes it and saves it to Qdrant cloud database

```http
  PUT /api/vectorize
```

This is done from backend perspective with `localhost:5000` as the URI

| Request Body | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `Courses`      | `json` | **Required**. New courses  |

#### POST the recommended courses to backend

Have to use the URI for the backend `localhsot:8080`
As the backend is secured with JWT tokens, we need request headers to access backend

```http
http://localhost:8080/api/course/recommendations
```
| Parameters | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `headers`      | `string` | **Required**. JWT token as headers to ensure connection with the backend  |