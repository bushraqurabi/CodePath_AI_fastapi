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
│   ├── topic_router.py
│   ├── roadmap_router.py        # NEW - /api/roadmap
│   ├── contest_router.py        # NEW - /api/contest
│   └── reference_router.py      # NEW - /api/reference
│
├── services/
│   ├── chatbot/
│   ├── quiz/
│   ├── codeprint/
│   ├── topic/
│   ├── common/topic_analysis.py # NEW - weakness scoring, tier ratings
│   ├── roadmap/                 # NEW - AI roadmap generation
│   ├── contest/                 # NEW - virtual contest problem selection
│   └── reference/               # NEW - reference sheet curation
│
├── schemas/
│   ├── chatbot/
│   ├── quiz/
│   ├── codeprint/
│   ├── topic/
│   ├── roadmap/                 # NEW
│   ├── contest/                 # NEW
│   └── reference/               # NEW
│
├── core/
│   ├── config.py        # Environment & settings
│   └── gemini.py        # Gemini client wrapper
│
├── main.py              # FastAPI entry point
│
requirements.txt
Dockerfile
docker-compose.yml
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

## AI Feature Modules (used by CodePath Backend)

These stateless services are consumed by the Node backend (`codepath-backend`) via `FASTAPI_BASE_URL`. They never touch a database — the caller sends the user's topics, quiz performance and Codeforces stats. Every module falls back to a **deterministic response** when Gemini is unreachable, so the platform keeps working offline.

### Roadmap Module (`/api/roadmap`)

Weakness-ranked, personalized study roadmap.

* Canonical topic order + aliases and prereq ranking (shared in `services/common/topic_analysis.py`)
* Gemini strict-JSON generation with a deterministic fallback
* Difficulty range derived from the user's tier

**Endpoint**: `POST /api/roadmap/generate`

```json
{ "userId": "u1", "topics": [{ "id": 1, "title": "Arrays" }], "codeforcesStats": { "rating": 1400, "tier": "Intermediate" } }
```

### Contest Module (`/api/contest`)

Selects problems for a virtual contest.

* Weakest topics get the most problems and sit at the easier end
* Ascending difficulty curve across the contest (step of ~100 rating)
* Base difficulty = tier base rating − 200

**Endpoint**: `POST /api/contest/select-problems`

```json
{ "userId": "u1", "targetSkillTier": "Intermediate", "topics": [{ "id": 1, "title": "Arrays" }], "totalProblems": 12 }
```

### Reference Module (`/api/reference`)

Curates the user's saved solution snippets into a study sheet.

* Groups snippets by topic, ordered by weakness
* Gemini-written per-topic intros with a templated fallback

**Endpoint**: `POST /api/reference/curate`

```json
{ "userId": "u1", "snippets": [{ "id": "a1", "title": "Two pointers", "topicTitle": "Arrays", "language": "cpp" }] }
```

---

## Environment Variables

Create a `.env` file (do **not** commit it):

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

| Variable       | Description           |
| -------------- | --------------------- |
| GEMINI_API_KEY | Google Gemini API key |
| GEMINI_MODEL   | Gemini model name (`gemini-2.5-flash` is the free default; `gemini-2.5-flash-lite` is deprecated for new users) |

Copy `.env.example` to `.env` and fill in your key.

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

### Run with Docker Compose (Recommended)

A `docker-compose.yml` is included. It builds the image, publishes port `8000`, and loads your `.env` automatically.

**macOS / Linux / Windows (PowerShell or CMD)**

```bash
docker compose up -d --build
```

Older Docker versions:

```bash
docker-compose up -d --build
```

Stop the container:

```bash
docker compose down
```

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

## Postman

Import `postman/codepath-fastapi_postman_collection.json` in Postman and set the `fastApiBaseUrl` variable to `http://127.0.0.1:8000`. The collection covers the three AI feature endpoints (`/api/roadmap/generate`, `/api/contest/select-problems`, `/api/reference/curate`).

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
