# 🎓 EduLoop – Auto-Grading Assignment Submission System

EduLoop is an assignment submission and auto-grading platform built with **FastAPI**. It allows faculty to create assignments and automatically grade student submissions using Hugging Face's AI models. It uses **Redis** for performance and caching, and **Supabase PostgreSQL** as the primary database.

---

## 🚀 Features

- 👥 Role-based access for students and faculty
- 📝 Assignment creation, submission, and auto-grading
- 🤖 AI-powered grading via Hugging Face transformers
- 💾 Supabase PostgreSQL for persistent storage
- ⚡ Redis caching for performance optimization
- 📦 Modular and scalable FastAPI architecture

---

## ⚙️ Requirements

- Redis (local or Docker-based)
- Supabase PostgreSQL (or compatible Postgres DB)
- Hugging Face Account (for auto-grading)
- Hugging Face API Token
- \`venv\` (recommended for isolation)

---

## 📦 Setup Instructions

### 1. Create and Activate Virtual Environment

\`\`\`bash
python -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
\`\`\`

### 2. Install Required Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Configure Environment Variables

Copy the sample \`.env.example\` and create the .env file:

Then open \`.env\` and fill in values like:

\`\`\`dotenv
SUPABASE_DB_URL=postgresql://your_user:your_password@your_host:5432/your_database
REDIS_HOST=localhost
REDIS_PORT=6379
COOKIE_NAME=SubmitAssignment
SECRET_KEY=your-secret-key
HF_TOKEN=your-huggingface-api-token
\`\`\`

> ⚠️ \`HF_TOKEN\` is **mandatory** for enabling the auto-grading feature using Hugging Face models.

---

## 🛢️ Database Initialization

Before running the server, initialize the database:

\`\`\`bash
python init_db.py
\`\`\`

This script uses SQLAlchemy to create all the required tables in your Supabase PostgreSQL database.

---

## 🧠 Running Redis (Using Docker)

If you don't have Redis installed locally, you can run it via Docker:

\`\`\`bash
docker run -d -p 6379:6379 --name redis redis
\`\`\`

Ensure your \`.env\` has these matching:

\`\`\`dotenv
REDIS_HOST=localhost
REDIS_PORT=6379
\`\`\`

---

## ▶️ Run the FastAPI Server

\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

Server will start at:

\`\`\`
http://localhost:8000
\`\`\`

---

## 📮 API Usage & Testing

- You can import the **Postman Collection** shared in the repository to test endpoints easily.

---

## 🛡️ License

This project is licensed under the MIT License.

---

## 📬 Contact

For questions or feedback, feel free to reach out or open an issue in the repo.
