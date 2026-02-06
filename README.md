# CodePath AI – FastAPI Backend

CodePath AI is a **modular FastAPI backend** built to support **competitive programming education, analytics, and AI-powered insights**.  
It integrates **quizzes**, **Codeforces-style performance dashboards**, **topic-level intelligence**, and a **Gemini-powered AI assistant** into a clean, extensible, and production-ready system.

The backend is **stateless**, **Docker-ready**, and designed with **clear separation of concerns**, making it easy to extend or integrate into larger systems.

---

## What This Mini Module Does

This project is a **mini backend module** designed to help:

* Students and programmers **practice quizzes** and track performance
* Analyze **topic-level strengths and weaknesses**
* Provide **AI-powered guidance and summaries**
* Generate **Codeforces-style insights** with user-friendly dashboards

It is **fully modular**, so you can pick and use only the parts you need.  
It can help in **learning, teaching, or integrating AI guidance into competitive programming platforms**.

---

## Key Features

* **AI Chatbot** powered by Google Gemini for competitive programming guidance
* **Quiz Engine** with scoring, topic-wise analysis, and AI-style feedback
* **CodePrint Dashboard** with Codeforces-inspired analytics and insights
* **Topic Intelligence Module** for skill breakdown and AI-generated recommendations
* **Dockerized setup** for consistent and reproducible builds
* **Swagger / OpenAPI documentation** out of the box

---

## Architecture Overview

The backend follows a **modular, micro-module architecture**:

* Each module is **self-contained**
* No database dependency (in-memory / mock data)
* AI integrations are isolated behind dedicated service layers
* Designed for clarity, testability, and future scalability

---

## Technology Stack

| Category          | Technology                     |
| ----------------- | ------------------------------ |
| Language          | Python 3.11                    |
| Framework         | FastAPI                        |
| ASGI Server       | Uvicorn                        |
| Validation        | Pydantic v2                    |
| AI Integration    | Google Gemini (`google-genai`) |
| Containerization  | Docker                         |
| API Documentation | Swagger (OpenAPI)              |

---

## Project Structure

```

app/
├── api/
│   ├── chatbot_router.py
│   ├── quiz_router.py
│   ├── codeprint_router.py
│   └── topic_router.py
│
├── services/
│   ├── chatbot/
│   ├── quiz/
│   ├── codeprint/
│   └── topic/
│
├── schemas/
│   ├── chatbot/
│   ├── quiz/
│   ├── codeprint/
│   └── topic/
│
├── core/
│   ├── config.py        # Environment & settings
│   └── gemini.py        # Gemini client wrapper
│
├── main.py              # FastAPI entry point
│
requirements.txt
Dockerfile
.dockerignore
.env.example
README.md

````

---

## Module Overview

### Chatbot Module (`/api/chat`)

An AI-powered chatbot that:

* Accepts competitive programming questions
* Enhances prompts with contextual examples
* Generates responses using Google Gemini

**Endpoints**

* `POST /api/chat`

---

### Quiz Module (`/quiz`)

Provides quiz functionality including:

* Randomized question generation
* Answer submission and validation
* Accuracy calculation
* Topic-wise performance analysis
* AI-style feedback summaries

**Endpoints**

* `GET /quiz/start`
* `POST /quiz/submit`

---

### CodePrint Module (`/dashboard`)

Codeforces-style analytics and insights:

* User rating and tier estimation
* Topic strength visualization (radar data)
* AI-generated learning recommendations

**Endpoints**

* `GET /dashboard/user/{handle}`
* `GET /dashboard/radar/{handle}`
* `GET /dashboard/ai/{handle}`

---

### Topic Intelligence Module (`/topic`)

Advanced topic and subskill analysis:

* Accuracy metrics and level classification
* Subskill performance breakdown
* Gemini-powered summaries and insights

**Endpoints**

* `GET /topic/{topic_name}?user_handle=...`
* `GET /topic/{topic_name}/ai-summary?user_handle=...`

---

## Environment Variables

Create a `.env` file (do **not** commit it):

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
````

| Variable       | Description           |
| -------------- | --------------------- |
| GEMINI_API_KEY | Google Gemini API key |
| GEMINI_MODEL   | Gemini model name     |

---

## Running with Docker (Recommended)

### Build the Image

**macOS / Linux**

```bash
docker build -t codepath-ai .
```

**Windows (PowerShell or CMD)**

```powershell
docker build -t codepath-ai .
```

---

### Run the Container

**macOS / Linux**

```bash
docker run -p 8000:8000 --env-file .env codepath-ai
```

**Windows (PowerShell)**

```powershell
docker run -p 8000:8000 --env-file .env codepath-ai
```

**Windows (CMD)**

```cmd
docker run -p 8000:8000 --env-file .env codepath-ai
```

**Benefits**

* No virtual environment required
* No local Python dependency conflicts
* Clean, reproducible builds

---

## Running Locally with Virtual Environment

### Create and Activate Virtual Environment

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (CMD)**

```cmd
python -m venv venv
venv\Scripts\activate
```

---

### Install Dependencies and Run Server

**All Platforms**

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## API Documentation

Once the server is running, access Swagger UI at:

```
http://127.0.0.1:8000/docs
```

---

## Testing

* Manual testing via **Swagger UI**
* Automated tests can be added in future iterations

---

## Dependencies

From `requirements.txt`:

* fastapi
* uvicorn
* pydantic
* pydantic-settings
* google-genai
* All other packages listed in `requirements.txt`

```

---
