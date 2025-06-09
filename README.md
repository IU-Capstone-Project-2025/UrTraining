# UrTraining

A web-based platform for creating, distributing, and following personalized training plans. Users receive AI-assisted workout recommendations based on their fitness goals and conditions, while coaches can upload and manage their own structured training programs.

---

## 🧠 Project Idea

UrTraining helps clients avoid generic fitness advice and instead get structured programs tailored to their needs. At the same time, it enables trainers to easily share their expertise, grow their reach, and earn without having to learn tech or marketing.

Our AI-based system matches users with training programs created by verified coaches, making it easy to start and stay consistent with a personalized fitness journey.

---

## 💻 Proposed Tech Stack

### Frontend
- **React** – Component-based UI development
- **TailwindCSS** – Utility-first styling
- **shadcn/ui** – Reusable UI components
- **Framer Motion** – Smooth animations and transitions

### Backend
- **FastAPI** – High-performance Python backend
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM for database interactions
- **Docker** – Containerization
- **GitHub Actions** – CI/CD pipeline

### AI/ML
- **Sentence-BERT** – Embedding models for semantic search
- **HuggingFace Transformers** – LLM capabilities
- **Faiss** – Vector similarity search
- **EasyOCR / PaddleOCR** – Extracting text from documents

### Storage
- **Cloudinary / Supabase / AWS S3** – For storing images, files, and training PDFs

---

## 🔧 MVP Scope

### ✅ Included
- User registration (coach/client)
- Questionnaire for users to generate recommendations
- Simple tracking system
- Training program upload (PDF, text, images)
- AI-powered recommendation engine
- Training catalog with filtering
- Save/purchase functionality

### 🎯 Future Work
- Monetization tools for trainers
- Real-time chat/video
- Social features and mobile app
- Subscription systems
- Ratings & reviews
- Smart content moderation and estimation

---

## 👥 Team

| Name                 | Role               | Contact (Telegram) |
|----------------------|--------------------|---------------------|
| Ildar Rakiev         | Lead / Backend / Design   | @mescudiway         |
| Makar Dyachenko      | Frontend / Design  | @index099           |
| Salavat Faizullin    | Backend            | @FSA_2005           |
| Egor Chernobrovkin   | Machine Learning   | @lolyhop            |
| Alexandra Starikova  | Machine Learning   | @lexandrinnn_t      |
| Ilona Dziurava       | PM / Frontend      | @a_b_r_i_c_o_s      |
| Anisya Kochetkova    | Backend            | @anis1305           |

---

## 📈 Progress

**Week 1:** We’ve completed foundational planning, divided responsibilities, and selected our tech stack. Interface design and early implementation of core features (questionnaire, catalog, recommendation engine) are underway.

---

## 🚀 Local Setup & Run Instructions

### 1. Clone the repository

```bash
git clone https://github.com/IU-Capstone-Project-2025/UrTraining.git
cd urtraining
```

### 2. Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate     # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3. Frontend Setup (React + Tailwind)
```bash
cd frontend
npm install
npm run dev
```

### 4. ML Module (for recommendation engine)
```bash
cd ml
pip install -r requirements.txt
# Run any script or training notebook as needed
```

### 5. Environment Variables

Set environment variables for backend/frontend via .env files:


**backend/.env**

**frontend/.env**

**Hint:** copy ```.env.example``` to ```.env``` and fill in the required data before running the project.


(Templates will be provided later)

### Project Deployment
To run full stack with Docker:

```bash
docker-compose up --build
```


