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
- **vite** – Fast build- and dev-server for service
- **Nginx** - Serve built frontend vite-application to users

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

- Main page with Sign In and Sign Up buttons for trainers and clients

![main](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/main_page.png)

- Registration process

![re-login](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/logfix.gif) 

- Questionnaire for users to generate recommendations

![client_survey](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/client_survey.gif)

- AI-powered recommendation engine

![main](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/client_recomendation.png)

- Client profile

![profile](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/client_profilee.gif)

- Training catalog with filtering

![catalog](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/catalog.gif)

- Course card

![card](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/card1.png)
![card](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/card2.png)

- Save functionality

![save](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/save.gif)

- Simple tracking system

![tracking1](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/tracking1.png)
![tracking2](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/tracking2.png)

- Questionnaire for trainers

![trainer_survey](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/trainer_survey.gif)

- Trainer profile

![trainer_profile](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/trainer_profile.gif)

- Course metadata information

![metadata](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/course_step1.gif)

- Manual course creation

![upload_manualy](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/course_step2.gif)

- Training upload from photo

![upload_photo](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/photo_upload.gif)

- FAQ page

![FAQ](https://raw.githubusercontent.com/IU-Capstone-Project-2025/UrTraining/main/reports/static/FAQ.gif)

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
docker-compose build
docker-compose up -d
```

Server will be accessible at **port 8000**.

### 3. Frontend Setup (React + Tailwind)
```bash
cd frontend
npm install
npm run dev
```

### 4. Vector Database (for recommendation engine)
```bash
cd ml/vector-db
docker-compose build
docker-compose up -d
# Run any script or training notebook as needed
```

Endpoints will be accessible at **port 1337**.

### 5. Image2tracker Module
```bash
cd ml/image2tracker
docker-compose build
docker-compose up -d
# Run any script or training notebook as needed
```

Endpoints will be accessible at **port 1338**.

### 6. Smart Assistant (for the course card)
```bash
cd ml/course-assistant
# Run any script or training notebook as needed
```

### 7. Trainer Assistant (for the training uploading)
```bash
cd ml/course-checker
pip install -r requirements.txt
# Run any script or training notebook as needed
```

### 8. Environment Variables

Set environment variables for backend/frontend via .env files:


**backend/.env**

**frontend/.env.local**

**Hint:** copy ```.env.example``` to ```.env``` and fill in the required data before running the project.


(Templates will be provided later)



