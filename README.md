# 📚 GyaanSetu – Mentor-Student Doubt Solving Platform

GyaanSetu is a full-stack MERN (MongoDB, Express.js, React.js, Node.js) web application that connects students with mentors to solve technical doubts through structured 1-on-1 scheduled sessions.

---

## 💡 Key Architectural Design

The platform uses a **unified single-account model**:
- There are **no separate account types** or separate login pages for students and mentors.
- Every registered user starts as a student (`isMentor: false`).
- Any user can click **"Become a Mentor"** to add technical skills and enable mentor capabilities (`isMentor: true`).
- The **same account** can seamlessly act as both a student (finding mentors & sending doubt requests) and a mentor (receiving requests & scheduling sessions).

---

## ✨ Features

- **🔐 Single Authentication**: Email/password registration and login with JWT token & bcrypt hashing.
- **👨‍🎓 Student Capabilities**:
  - Search & filter mentors by skills and name.
  - Send technical doubt proposals to mentors.
  - Track doubt proposal status (Pending, Accepted, Rejected).
  - Join scheduled 1-on-1 virtual sessions via Jitsi Meet.
- **👨‍🏫 Mentor Capabilities**:
  - Upgrade account with custom technical skills ("Become a Mentor").
  - View incoming student doubt proposals.
  - Accept or reject student proposals.
  - Schedule conflict-free mentoring sessions.
  - Automatic email notification on session scheduling.
  - Mark completed mentoring sessions.
- **📅 Conflict-Free Scheduling**: Automatically checks for time slot overlaps before saving sessions.
- **🎥 Virtual Meeting Integration**: Generates Jitsi Meet video room links for direct 1-on-1 interaction.

---

## 🛠️ Tech Stack

- **Frontend**: React.js, Vite, React Router, Axios, Tailwind CSS, Lucide React Icons.
- **Backend**: Node.js, Express.js, MongoDB, Mongoose ODM, bcryptjs, jsonwebtoken, Nodemailer, CORS, dotenv.
- **Meeting Platform**: Jitsi Meet (`meet.jit.si`).

---

## 📁 Project Structure

```text
gyaansetu/
├── client/                 # React Frontend (Vite)
│   ├── src/
│   │   ├── components/     # Navbar, BecomeMentorModal, RequestDoubtModal, ScheduleModal, ProtectedRoute
│   │   ├── context/        # AuthContext for state & token management
│   │   ├── pages/          # Home, Login, Register, Mentors, Dashboard, Sessions, Profile
│   │   ├── services/       # api.js (Axios instance with Bearer token interceptor)
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
└── server/                 # Express Backend API
    ├── config/             # db.js (MongoDB Connection)
    ├── controllers/        # authController, userController, mentorController, proposalController, sessionController
    ├── middleware/         # authMiddleware (JWT Verification)
    ├── models/             # User.js, Proposal.js, Session.js
    ├── routes/             # authRoutes, userRoutes, mentorRoutes, proposalRoutes, sessionRoutes
    ├── utils/              # sendEmail.js (Nodemailer)
    ├── seed.js             # Initial database seeder script
    ├── server.js           # Server entry point
    └── package.json
```

---

## 🗄️ Database Schemas (MongoDB)

### 1. User (`users`)
```json
{
  "_id": "ObjectId",
  "name": "Aditya Kumar",
  "email": "aditya@gmail.com",
  "password": "hashedPassword",
  "isMentor": true,
  "skills": ["Java", "DSA", "SQL"],
  "createdAt": "2026-09-26T21:00:00.000Z"
}
```

### 2. Proposal (`proposals`)
```json
{
  "_id": "ObjectId",
  "student": "ObjectId(User)",
  "mentor": "ObjectId(User)",
  "studentEmail": "aditya@gmail.com",
  "mentorEmail": "rahul@gmail.com",
  "doubt": "I am confused about binary search recursion.",
  "status": "pending | accepted | rejected",
  "createdAt": "2026-09-26T21:00:00.000Z"
}
```

### 3. Session (`sessions`)
```json
{
  "_id": "ObjectId",
  "proposal": "ObjectId(Proposal)",
  "student": "ObjectId(User)",
  "mentor": "ObjectId(User)",
  "studentEmail": "aditya@gmail.com",
  "mentorEmail": "rahul@gmail.com",
  "scheduledTime": "2026-09-27T10:00:00.000Z",
  "meetingLink": "https://meet.jit.si/gyaansetu-session-id",
  "status": "scheduled | completed",
  "createdAt": "2026-09-26T21:00:00.000Z"
}
```

---

## 🔌 API Endpoints Summary

### Authentication (`/api/auth`)
- `POST /api/auth/register` – Register a new user account.
- `POST /api/auth/login` – Login & receive JWT token.
- `GET /api/auth/me` – Fetch current authenticated user.

### User & Mentors (`/api/users` & `/api/mentors`)
- `PATCH /api/users/become-mentor` – Upgrade current user to mentor and save skills.
- `PATCH /api/users/update-skills` – Update mentor skills.
- `GET /api/mentors` – Fetch all users where `isMentor = true`.

### Proposals (`/api/proposals`)
- `POST /api/proposals` – Create doubt proposal to a mentor.
- `GET /api/proposals/my` – Get proposals sent by logged-in user as student.
- `GET /api/proposals/received` – Get proposals received by logged-in user as mentor.
- `PATCH /api/proposals/:id/accept` – Accept a doubt proposal (mentor only).
- `PATCH /api/proposals/:id/reject` – Reject a doubt proposal (mentor only).

### Sessions (`/api/sessions`)
- `POST /api/sessions` – Schedule session for accepted proposal with time conflict check.
- `GET /api/sessions/my` – Get all sessions for user (student or mentor).
- `PATCH /api/sessions/:id/complete` – Mark session complete (mentor only).

---

## ⚙️ Environment Variables

Create `.env` in `server/` directory:
```env
PORT=5000
MONGO_URI=mongodb://127.0.0.1:27017/gyaansetu
JWT_SECRET=gyaansetu_secret_key_2026_placement_project
EMAIL_USER=demo@gyaansetu.com
EMAIL_PASS=demopassword
CLIENT_URL=http://localhost:5173
```

---

## 🚀 How to Run Locally

### 1. Install Dependencies & Seed Database
```bash
# Terminal 1: Backend Setup
cd server
npm install
npm run seed     # Populates test users: Rahul (mentor), Priya (mentor), Aditya (student)
npm run dev      # Starts Express API at http://localhost:5000

# Terminal 2: Frontend Setup
cd client
npm install
npm run dev      # Starts Vite React dev server at http://localhost:5173
```

---

## 🧪 Testing the Dual-Role Workflow

1. Open `http://localhost:5173` in your browser.
2. Click **Login** and use **Aditya (Student)** quick login (`aditya@gmail.com` / `123456`).
3. Click **Mentors** in Navbar, select **Rahul**, and click **Ask Doubt**.
4. Log out and login as **Rahul (Mentor)** (`rahul@gmail.com` / `123456`).
5. Open **Dashboard** -> See incoming request from Aditya -> Click **Accept** -> Click **Schedule Session**.
6. Switch back to **Aditya**: Go to **Sessions** -> Click **Join Meeting** (opens Jitsi URL in new tab).
7. On **Aditya's account**, click **Become a Mentor** in top bar, enter `Java, Spring Boot` -> Now Aditya can ALSO receive incoming doubt requests as a mentor on the exact same account!
