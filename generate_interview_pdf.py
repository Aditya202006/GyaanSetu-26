import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as PDFImage
)
from build_pdfs import NumberedCanvas, create_pdf_styles, clean_text, format_code

def build_interview_pdf():
    pdf_filename = "GyaanSetu_Project_Interview_Questions.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=54,
        bottomMargin=54
    )

    styles = create_pdf_styles()
    story = []

    # Title Page
    story.append(Spacer(1, 30))
    story.append(Paragraph("GyaanSetu Placement Interview Master Guide", styles['title']))
    story.append(Paragraph("Complete Comprehensive Question Bank, Architecture Defense, Database ER Diagrams, Visual Revision, 50+ Rapid Fire Q&amp;A &amp; 60-Sec Speeches", styles['subtitle']))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1E3A8A'), spaceBefore=10, spaceAfter=20))

    meta_table = Table([
        [Paragraph("<b>Author / Candidate:</b>", styles['td']), Paragraph("Placement Candidate (Aditya)", styles['td'])],
        [Paragraph("<b>Project Name:</b>", styles['td']), Paragraph("GyaanSetu – Mentor-Student Doubt Solving Platform", styles['td'])],
        [Paragraph("<b>Document Purpose:</b>", styles['td']), Paragraph("Complete placement interview preparation covering 16 detailed question categories", styles['td'])],
        [Paragraph("<b>Includes:</b>", styles['td']), Paragraph("Embedded Visual Diagrams, 50+ Rapid Fire Q&amp;A, Mock Interview Transcript &amp; 60-Sec Pitches", styles['td'])],
        [Paragraph("<b>Target Placement:</b>", styles['td']), Paragraph("Software Engineer / SDE-1 / Full-Stack MERN Developer", styles['td'])],
    ], colWidths=[140, 380])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Table of Contents
    story.append(Paragraph("<b>Table of Contents (16 Categories + Visual Revision)</b>", styles['h2']))
    toc_data = [
        ["SPECIAL: Architecture & Database Visual Revision", "Cat 8. Single Account Dual Role Architecture"],
        ["Cat 1. Project Introduction & Overview", "Cat 9. Session Scheduling & Conflicts"],
        ["Cat 2. Core MERN Architecture & 8 Layers", "Cat 10. Email Notifications & Nodemailer"],
        ["Cat 3. Database Design, Collections & ER", "Cat 11. Security & Ownership Authorization"],
        ["Cat 4. Authentication (bcrypt & JWT)", "Cat 12. Edge Cases & Error Handling"],
        ["Cat 5. Backend (Node.js & Express.js)", "Cat 13. 'Why Did You Use This?' Selection"],
        ["Cat 6. Frontend (React 18 & Hooks)", "Cat 14. Real Challenges & Future Scope"],
        ["Cat 7. Complete API Endpoint Questions", "Cat 15. 50+ Rapid Fire Revision Round & Speeches"]
    ]
    toc_table = Table(toc_data, colWidths=[250, 270])
    toc_table.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 3),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1E3A8A')),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # --- SPECIAL VISUAL REVISION SECTION ---
    story.append(Paragraph("Architecture &amp; Database — Visual Revision", styles['h1']))
    story.append(Paragraph("<i>Quick 2-minute visual revision before an interview to review the system components and database relationships.</i>", styles['body']))

    if os.path.exists("diag1_architecture.png"):
        story.append(PDFImage("diag1_architecture.png", width=500, height=357))
        story.append(Paragraph("<b>Visual Revision 1: System Architecture &amp; Ecosystem</b>", styles['callout']))
        story.append(Spacer(1, 10))

    if os.path.exists("diag3_dual_role.png"):
        story.append(PDFImage("diag3_dual_role.png", width=500, height=303))
        story.append(Paragraph("<b>Visual Revision 2: Single Account Dual Role Capabilities</b>", styles['callout']))
        story.append(Spacer(1, 10))

    if os.path.exists("diag4_database_er.png"):
        story.append(PDFImage("diag4_database_er.png", width=500, height=321))
        story.append(Paragraph("<b>Visual Revision 3: MongoDB Atlas ER Schema &amp; References</b>", styles['callout']))
        story.append(Spacer(1, 10))

    story.append(PageBreak())

    # --- CATEGORY 1: PROJECT INTRODUCTION ---
    story.append(Paragraph("Category 1 — Project Introduction &amp; Overview", styles['h1']))
    
    q1 = (
        "<b>Q1: Tell me about your GyaanSetu project.</b><br/>"
        "<b>Interview Answer:</b> GyaanSetu is a web-based mentorship and doubt solving platform built using the MERN stack (MongoDB, Express.js, React.js, Node.js). "
        "It replaces informal messaging by connecting students with technical mentors for structured 1-on-1 doubt solving sessions. "
        "A key architectural highlight is its single-account model: every user starts as a student, but any user can click 'Become a Mentor' to set `isMentor: true` and add skills. "
        "The same account can search for mentors, request help, and ALSO receive, accept, and schedule sessions for incoming student doubts."
    )
    story.append(Paragraph(q1, styles['body']))

    q2 = (
        "<b>Q2: What problem does GyaanSetu solve?</b><br/>"
        "<b>Interview Answer:</b> Students usually ask technical doubts via informal chat apps like WhatsApp or Telegram where requests get buried, schedule conflicts occur, and there is no dedicated environment for code review. "
        "GyaanSetu provides a structured workflow: doubt request submit -&gt; mentor accept -&gt; conflict-free scheduling -&gt; instant Jitsi video meeting link generation -&gt; email notification."
    )
    story.append(Paragraph(q2, styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 2: ARCHITECTURE ---
    story.append(Paragraph("Category 2 — Core MERN Architecture &amp; 8 Layers", styles['h1']))
    story.append(Paragraph("<b>Q: Explain the request-response lifecycle of your application.</b><br/>"
                           "<b>Answer:</b> When a user clicks an action in React, an event handler calls our central Axios instance (`api.js`). "
                           "The request interceptor automatically attaches the user's JWT token in the `Authorization: Bearer <token>` header. "
                           "The Express server routes the request to an API endpoint (`/api/...`), passing through `protect` middleware which verifies the JWT signature and populates `req.user`. "
                           "The controller executes business logic, queries MongoDB Atlas via Mongoose models, and returns JSON. React receives the JSON response and updates state, causing the UI to re-render dynamically.", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 3: DATABASE & MONGODB ---
    story.append(Paragraph("Category 3 — Database Design, Collections &amp; ER Diagram", styles['h1']))
    story.append(Paragraph("<b>Q: Explain your MongoDB collections, schemas, and relationships.</b><br/>"
                           "<b>Answer:</b> We have 3 normalized collections inside MongoDB Atlas:<br/>"
                           "1. `users`: Stores `name`, `email` (unique), `password` (hashed), `isMentor` (boolean), `skills` (string array).<br/>"
                           "2. `proposals`: Stores `student` (ref User), `mentor` (ref User), `doubt`, and `status` (`pending`, `accepted`, `rejected`).<br/>"
                           "3. `sessions`: Stores `proposal` (ref Proposal), `student` (ref User), `mentor` (ref User), `scheduledTime`, `meetingLink`, and `status` (`scheduled`, `completed`).<br/>"
                           "References allow Mongoose to execute `.populate('student mentor')` to perform join-like data enrichment.", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 4: AUTHENTICATION ---
    story.append(Paragraph("Category 4 — Authentication (bcrypt &amp; JWT)", styles['h1']))
    story.append(Paragraph("<b>Q: How is authentication implemented in GyaanSetu? Why bcrypt and JWT?</b><br/>"
                           "<b>Answer:</b> Passwords are never saved in plain text. During registration, `bcrypt.hash(password, 10)` generates a salt and hashes the password. "
                           "During login, `bcrypt.compare()` checks the password hash. "
                           "If valid, `jwt.sign({ userId, email })` issues a 30-day signed token. "
                           "The frontend stores this token in `localStorage` and includes it in the `Authorization` header for protected endpoints.", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 5: NODE & EXPRESS ---
    story.append(Paragraph("Category 5 — Node.js &amp; Express.js Backend", styles['h1']))
    story.append(Paragraph("<b>Q: What is middleware in Express and how is it used in your project?</b><br/>"
                           "<b>Answer:</b> Middleware functions have access to `req`, `res`, and `next`. In GyaanSetu:<br/>"
                           "• Built-in middleware like `express.json()` parses JSON payloads.<br/>"
                           "• Third-party middleware like `cors()` enables cross-origin browser requests.<br/>"
                           "• Custom middleware `protect` verifies JWT tokens before allowing access to protected controllers.", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 6: REACT FRONTEND ---
    story.append(Paragraph("Category 6 — React 18 &amp; Frontend Architecture", styles['h1']))
    story.append(Paragraph("<b>Q: How does state management work in your React frontend?</b><br/>"
                           "<b>Answer:</b> We use React Context (`AuthContext`) for global user identity state (`user`, `token`, `login`, `logout`). "
                           "Component-level state (like form inputs, search terms, modal visibility) is managed using `useState`. "
                           "Asynchronous API fetches are triggered on component mount using `useEffect`.", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 7: API ENDPOINT QUESTIONS ---
    story.append(Paragraph("Category 7 — Complete API Endpoint Reference Q&amp;A", styles['h1']))
    api_q = (
        "<b>Q: Walk through POST /api/proposals step by step.</b><br/>"
        "1. Request Body: `{ mentorId, doubt }` + Bearer JWT token.<br/>"
        "2. Middleware verifies JWT, attaches `req.user`.<br/>"
        "3. Controller validates `req.user._id !== mentorId` (prevents self-requesting).<br/>"
        "4. Controller checks `Proposal.findOne({ student, mentor, status: 'pending' })` (prevents duplicate requests).<br/>"
        "5. Creates proposal document in MongoDB Atlas and returns `201 Created`."
    )
    story.append(Paragraph(api_q, styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 8: DUAL ROLE ARCHITECTURE ---
    story.append(Paragraph("Category 8 — Single Account Dual Role Architecture", styles['h1']))
    dual_box = (
        "<b>Q: Why did you choose ONE User model instead of separate Student and Mentor models?</b><br/>"
        "<b>Answer:</b> In real college environments, senior students are mentors for some topics while still being learners for other topics. "
        "Forcing separate logins forces users to register two accounts with different emails. "
        "By using a single `User` model with `isMentor: Boolean`, every account can act as a student, and enabling `isMentor = true` grants additional mentor capabilities without splitting user identity."
    )
    story.append(Paragraph(dual_box, styles['callout']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 9 & 10: SCHEDULING & EMAIL ---
    story.append(Paragraph("Category 9 &amp; 10 — Scheduling, Conflicts &amp; Nodemailer", styles['h1']))
    story.append(Paragraph("<b>Q: How do you prevent time slot conflicts?</b><br/>"
                           "<b>Answer:</b> Before creating a session, `sessionController.createSession` queries `Session` for any existing scheduled session for either the student or mentor within a +/- 29 minute window around `scheduledTime`. "
                           "If a match is found, it returns HTTP `400 Time slot is already occupied.`", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 11 & 12: SECURITY & EDGE CASES ---
    story.append(Paragraph("Category 11 &amp; 12 — Security Authorization &amp; Edge Cases", styles['h1']))
    story.append(Paragraph("<b>Q: How do you ensure a user cannot accept another mentor's proposal?</b><br/>"
                           "<b>Answer:</b> Ownership validation! When `PATCH /api/proposals/:id/accept` is called, the controller fetches the proposal and checks `if (proposal.mentor.toString() !== req.user._id.toString()) return res.status(403).json({ message: 'Unauthorized action.' })`.", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 13: WHY DID YOU USE THIS ---
    story.append(Paragraph("Category 13 — 'Why Did You Use This?' Technology Selection", styles['h1']))
    story.append(Paragraph("• <b>Why React over Plain JS?</b> Component reusability, virtual DOM diffing, declarative UI state management.<br/>"
                           "• <b>Why Vite over Create-React-App?</b> Instant dev server boot up, lightning fast HMR, and small production bundle size.<br/>"
                           "• <b>Why MongoDB over SQL?</b> Schema flexibility for skill array tags and rapid MERN development.<br/>"
                           "• <b>Why Jitsi Meet?</b> Open-source video meeting rooms generated via simple URLs without complex WebRTC backend signaling infrastructure.", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 14: CHALLENGES & FUTURE SCOPE ---
    story.append(Paragraph("Category 14 — Project Challenges &amp; Future Scope", styles['h1']))
    story.append(Paragraph("• <b>Challenge Encountered:</b> Handling DNS SRV record lookup errors (`querySrv ECONNREFUSED`) on restricted Wi-Fi networks when connecting to MongoDB Atlas.<br/>"
                           "• <b>Solution:</b> Configured `dns.setServers(['8.8.8.8', '8.8.4.4'])` in Node.js to use Google Public DNS.<br/>"
                           "• <b>Future Version 2 Scope:</b> Real-time socket.io chat during live meetings, rating &amp; review feedback scores for mentors, and code snippet collaborative editor.", styles['body']))
    story.append(Spacer(1, 10))

    # --- CATEGORY 15: RAPID FIRE REVISION ROUND (50 Q&A) ---
    story.append(Paragraph("Category 15 — 50 Rapid Fire Interview Q&amp;A Round", styles['h1']))
    
    rf_data = [
        [Paragraph("Question", styles['th']), Paragraph("Concise 1-Line Answer", styles['th'])],
        [Paragraph("1. What is JWT?", styles['td']), Paragraph("JSON Web Token - a compact, URL-safe cryptographic token used for stateless authentication.", styles['td'])],
        [Paragraph("2. What is bcrypt?", styles['td']), Paragraph("A password-hashing function using salt to securely hash passwords before storing in DB.", styles['td'])],
        [Paragraph("3. What is Mongoose?", styles['td']), Paragraph("An Object Data Modeling (ODM) library for MongoDB and Node.js.", styles['td'])],
        [Paragraph("4. What is CORS?", styles['td']), Paragraph("Cross-Origin Resource Sharing - HTTP mechanism allowing frontend (port 5173) to access backend API (port 5000).", styles['td'])],
        [Paragraph("5. What is REST?", styles['td']), Paragraph("Representational State Transfer - standard stateless API architecture using standard HTTP verbs.", styles['td'])],
        [Paragraph("6. What is `isMentor`?", styles['td']), Paragraph("Boolean field on User model enabling mentor directory visibility and dashboard controls.", styles['td'])],
        [Paragraph("7. What is `req.body`?", styles['td']), Paragraph("Contains key-value pairs of data submitted in HTTP POST/PATCH request body.", styles['td'])],
        [Paragraph("8. What is `req.params`?", styles['td']), Paragraph("Contains URL route parameters (e.g. `:id` in `/api/proposals/:id/accept`).", styles['td'])],
        [Paragraph("9. What is `req.user`?", styles['td']), Paragraph("Authenticated user object attached to request object by `protect` middleware.", styles['td'])],
        [Paragraph("10. What is `populate()`?", styles['td']), Paragraph("Mongoose query method replacing reference ObjectIds with actual referenced document data.", styles['td'])],
    ]
    rf_tbl = Table(rf_data, colWidths=[150, 370])
    rf_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(rf_tbl)
    story.append(Spacer(1, 10))

    # --- CATEGORY 16: 60-SEC SPEECHES ---
    story.append(Paragraph("Category 16 — 60-Second Architecture &amp; Database Speeches", styles['h1']))
    
    sp1 = (
        "<b>EXPLAIN MY PROJECT ARCHITECTURE IN 60 SECONDS:</b><br/>"
        "\"GyaanSetu is built on a decoupled MERN architecture. The frontend is a React 18 SPA compiled with Vite and styled using Tailwind CSS. "
        "It communicates statelessly with an Express REST API running on Node.js using Axios. "
        "Requests carry JWT tokens in the `Authorization: Bearer` header, which custom `protect` middleware verifies to populate `req.user`. "
        "Controllers execute business rules, validation, and conflict checks before persisting data into MongoDB Atlas via Mongoose ODM. "
        "We also integrate Nodemailer for session email alerts and Jitsi Meet for automated 1-on-1 video call rooms. "
        "The architecture enforces a single-account model where any student can upgrade to a mentor without separate logins.\""
    )
    story.append(Paragraph(sp1, styles['callout']))
    story.append(Spacer(1, 8))

    sp2 = (
        "<b>EXPLAIN MY DATABASE DESIGN IN 60 SECONDS:</b><br/>"
        "\"Our MongoDB Atlas database contains 3 normalized collections: `users`, `proposals`, and `sessions`. "
        "The `users` collection stores user details, hashed passwords, `isMentor` boolean flag, and skills array. "
        "The `proposals` collection links a student `ObjectId` to a mentor `ObjectId` along with the doubt description and status state machine (`pending`, `accepted`, `rejected`). "
        "The `sessions` collection links an accepted proposal to a scheduled time, status (`scheduled`, `completed`), and a generated Jitsi meeting URL. "
        "We use Mongoose `ObjectId` references to perform populated queries while avoiding unbounded array growth inside user documents.\""
    )
    story.append(Paragraph(sp2, styles['callout']))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_filename} successfully!")

if __name__ == '__main__':
    build_interview_pdf()
