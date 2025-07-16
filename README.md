# UrTraining

A web-based platform for creating, distributing, and following personalized training plans. Users receive AI-assisted workout recommendations based on their fitness goals and conditions, while coaches can upload and manage their own structured training programs.

**Try it yourself:** [UrTraining](http://31.129.96.182/)
---

## 🧠 Project Idea

UrTraining helps clients avoid generic fitness advice and instead get structured programs tailored to their needs. At the same time, it enables trainers to easily share their expertise, grow their reach, and earn without having to learn tech or marketing.

Our AI-based system matches users with training programs created by verified coaches, making it easy to start and stay consistent with a personalized fitness journey.

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
| Anisya Kochetkova    | Backend, Testing   | @anis1305           |

---

## 💻 Proposed Tech Stack

### Frontend
- **React** – Component-based UI development
- **shadcn/ui** – Reusable UI components

### Backend
- **FastAPI** – High-performance Python backend
- **PostgreSQL** – Relational database
- **SQLAlchemy** – ORM for database interactions
- **Docker** – Containerization
- **GitHub Actions** – CI/CD pipeline

### ML
- **FAISS** - Vector storage library
- **PyTorch, Transformers** -  Fine-tuned, pre-trained models hosting
- **OpenAI-like APIs** - LLMs integration
- **sentence_transformers** - embedding models training

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
- Save functionality

### 🎯 Future Work
- Monetization tools for trainers
- Real-time chat/video
- Social features and mobile app
- Subscription systems
- Ratings & reviews
- Smart content moderation and estimation

---

## 📈 Progress

**Week 1:** We’ve completed foundational planning, divided responsibilities, and selected our tech stack. Interface design and early implementation of core features (questionnaire, catalog, recommendation engine) are underway.

**Week 2:** Transformed initial ideas into concrete requirements, established foundational designs, and set up project structures across the frontend and backend.

**Week 3:** Delivered the first working version of the Minimum Viable Product (MVP). This includes a fully functional end-to-end user journey, with integrated frontend and backend components, persistent data storage, and a basic authentication flow. Additionally, the ML team delivered the first model iteration, integrated via a backend API for early testing and validation.

**Week 4:** By the end of Week 4, we had a stable, tested, and deployed version of our application in a staging environment, complete with CI/CD automation. This allows for updates and reliable testing going forward. Additionally, the trainer user flow was successfully implemented.

**Week 5:** Gathering real user feedback, analyzing it, and iterating on our MVP to improve usability and stability. Usability testing sessions were conducted with external testers, allowing us to uncover both critical bugs and areas for UX enhancement.

**Week 6:** Our primary focus was on finalizing and polishing the project in preparation for the upcoming final presentation. We completed remaining high-priority features, fixed outstanding bugs, and performed comprehensive end-to-end testing to ensure stability and usability across the application. Also we conducted two more feedback sessions to see the user perpective.

**Week 7:** Final presentation.

---

Implemented features:

---

## Deploy

Fronted part is deployed [HERE](http://31.129.96.182/).

Backend part is deployed [HERE](http://31.129.96.182:8000/).

ML part is deployed [HERE](http://31.129.96.182:1337/).

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


