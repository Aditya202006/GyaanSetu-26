import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image as PDFImage
)
from build_pdfs import NumberedCanvas, create_pdf_styles, clean_text, format_code

def build_backend_pdf():
    pdf_filename = "GyaanSetu_Backend_Deep_Dive.pdf"
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
    story.append(Spacer(1, 20))
    story.append(Paragraph("GyaanSetu Backend &amp; Architecture Deep Dive", styles['title']))
    story.append(Paragraph("A Comprehensive, Code-Verified Architecture &amp; Database Design Master Guide with Visual Diagrams for Placement Preparation", styles['subtitle']))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1E3A8A'), spaceBefore=10, spaceAfter=20))

    meta_table = Table([
        [Paragraph("<b>Author / Candidate:</b>", styles['td']), Paragraph("Placement Candidate (Aditya)", styles['td'])],
        [Paragraph("<b>Project Name:</b>", styles['td']), Paragraph("GyaanSetu – Mentor-Student Doubt Solving Platform", styles['td'])],
        [Paragraph("<b>Backend Stack:</b>", styles['td']), Paragraph("Node.js, Express.js, MongoDB Atlas, Mongoose ODM, JWT, bcryptjs, Nodemailer", styles['td'])],
        [Paragraph("<b>Database Design:</b>", styles['td']), Paragraph("3 Collections (users, proposals, sessions) with Mongoose ObjectId References", styles['td'])],
        [Paragraph("<b>Visual Diagrams Included:</b>", styles['td']), Paragraph("System Architecture, Business Flow, Dual-Role Tree, Database ER, Entity Relationships, DB Lifecycle", styles['td'])],
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
    story.append(Paragraph("<b>Table of Contents</b>", styles['h2']))
    toc_data = [
        ["1. High-Level Project Architecture & Visual Diagram", "11. Single Account Dual-Role Architecture & Diagram"],
        ["2. 8-Layer Architecture Breakdown", "12. Database Design & Visual ER Diagram"],
        ["3. End-to-End Business Flowchart Diagram", "13. Entity Relationship Visual Diagram"],
        ["4. Server Entry Point (server.js)", "14. Database State Machine Lifecycle Diagram"],
        ["5. Database Connection & DNS (db.js)", "15. Why Three Separate Collections?"],
        ["6. Schema 1: User Model (User.js)", "16. Database Document Flow Examples"],
        ["7. Schema 2: Proposal Model (Proposal.js)", "17. Mongoose Query Methods Line-by-Line"],
        ["8. Schema 3: Session Model (Session.js)", "18. Complete Request Lifecycle (9 Traces)"],
        ["9. Authentication & Auth Middleware", "19. Environment Variables Security"],
        ["10. Controllers Code-by-Code Analysis", "20. 60-Second Architecture & Database Speeches"]
    ]
    toc_table = Table(toc_data, colWidths=[250, 270])
    toc_table.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 3),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1E3A8A')),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # --- SECTION 1: HIGH-LEVEL ARCHITECTURE & VISUAL DIAGRAM ---
    story.append(Paragraph("1. High-Level Project Architecture &amp; Visual Diagram", styles['h1']))
    story.append(Paragraph(
        "GyaanSetu is structured as a decoupled full-stack web application. The frontend React Single Page Application (SPA) "
        "interacts statelessly with the Express REST API backend over HTTP using JSON data formatting. Database operations are handled "
        "asynchronously by Mongoose ODM connected to MongoDB Atlas.",
        styles['body']
    ))
    
    # VISUAL DIAGRAM 1: ARCHITECTURE
    if os.path.exists("diag1_architecture.png"):
        story.append(PDFImage("diag1_architecture.png", width=520, height=371))
        story.append(Paragraph("<i>Figure 1.1: GyaanSetu Complete System Architecture &amp; Ecosystem Services Interconnection Diagram</i>", styles['callout']))
        story.append(Spacer(1, 10))

    # --- SECTION 2: 8-LAYER BREAKDOWN ---
    story.append(Paragraph("2. 8-Layer Architecture Breakdown", styles['h1']))
    layers_data = [
        [Paragraph("Layer", styles['th']), Paragraph("Implementing Files", styles['th']), Paragraph("Layer Responsibilities &amp; Data Flow", styles['th'])],
        [Paragraph("1. Frontend Layer", styles['td']), Paragraph("`client/src/pages/*`, `components/*`", styles['td']), Paragraph("Captures user input, manages local state (`useState`), and renders clean responsive UI.", styles['td'])],
        [Paragraph("2. API / HTTP Layer", styles['td']), Paragraph("`client/src/services/api.js`", styles['td']), Paragraph("Axios instance appending `Authorization: Bearer <token>` to HTTP requests sent to backend.", styles['td'])],
        [Paragraph("3. Backend Route Layer", styles['td']), Paragraph("`server/routes/*.js`", styles['td']), Paragraph("Maps URL paths (`/api/proposals`) and HTTP methods (`POST`, `GET`, `PATCH`) to controllers.", styles['td'])],
        [Paragraph("4. Auth Middleware", styles['td']), Paragraph("`server/middleware/authMiddleware.js`", styles['td']), Paragraph("Intercepts requests, verifies JWT token signature, fetches user, and attaches `req.user`.", styles['td'])],
        [Paragraph("5. Controller Layer", styles['td']), Paragraph("`server/controllers/*.js`", styles['td']), Paragraph("Executes business rules, input validations, conflict checks, ownership authorization &amp; responses.", styles['td'])],
        [Paragraph("6. Model / ODM Layer", styles['td']), Paragraph("`server/models/*.js`", styles['td']), Paragraph("Defines Mongoose schemas (`User`, `Proposal`, `Session`), data types, defaults, and references.", styles['td'])],
        [Paragraph("7. Database Layer", styles['td']), Paragraph("MongoDB Atlas Cluster", styles['td']), Paragraph("Persists JSON documents inside 3 collections (`users`, `proposals`, `sessions`).", styles['td'])],
        [Paragraph("8. External Services", styles['td']), Paragraph("Nodemailer, Jitsi Meet", styles['td']), Paragraph("Dispatches automated email notifications and generates virtual video room links.", styles['td'])],
    ]
    layers_tbl = Table(layers_data, colWidths=[90, 140, 290])
    layers_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(layers_tbl)
    story.append(Spacer(1, 10))

    # --- SECTION 3: BUSINESS FLOWCHART DIAGRAM ---
    story.append(Paragraph("3. End-to-End Business Flowchart Visual Diagram", styles['h1']))
    if os.path.exists("diag2_business_flow.png"):
        story.append(PDFImage("diag2_business_flow.png", width=520, height=353))
        story.append(Paragraph("<i>Figure 3.1: GyaanSetu End-to-End Doubt Solving &amp; Session Scheduling Business Flowchart Diagram</i>", styles['callout']))
        story.append(Spacer(1, 10))

    # --- SECTION 4: SERVER.JS ---
    story.append(Paragraph("4. Server Entry Point (server.js)", styles['h1']))
    server_code = (
        "const express = require('express');\n"
        "const cors = require('cors');\n"
        "const dotenv = require('dotenv');\n"
        "const connectDB = require('./config/db');\n\n"
        "dotenv.config();\n"
        "connectDB();\n\n"
        "const app = express();\n"
        "app.use(cors());\n"
        "app.use(express.json());\n\n"
        "app.use('/api/auth', require('./routes/authRoutes'));\n"
        "app.use('/api/users', require('./routes/userRoutes'));\n"
        "app.use('/api/mentors', require('./routes/mentorRoutes'));\n"
        "app.use('/api/proposals', require('./routes/proposalRoutes'));\n"
        "app.use('/api/sessions', require('./routes/sessionRoutes'));\n\n"
        "app.get('/', (req, res) => res.json({ success: true, message: 'GyaanSetu Backend API is running smoothly.' }));\n\n"
        "const PORT = process.env.PORT || 5000;\n"
        "app.listen(PORT, () => console.log(`Server running on port ${PORT}`));"
    )
    story.append(Paragraph(format_code(server_code), styles['code']))
    story.append(Spacer(1, 10))

    # --- SECTION 5: DB.JS ---
    story.append(Paragraph("5. Database Connection &amp; DNS Fallback (config/db.js)", styles['h1']))
    db_code = (
        "const mongoose = require('mongoose');\n"
        "const dns = require('dns');\n\n"
        "try {\n"
        "  dns.setServers(['8.8.8.8', '8.8.4.4']); // Override local DNS for SRV queries\n"
        "} catch (err) {}\n\n"
        "const connectDB = async () => {\n"
        "  const targetUri = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/gyaansetu';\n"
        "  try {\n"
        "    const conn = await mongoose.connect(targetUri);\n"
        "    console.log(`MongoDB Connected: ${conn.connection.host}`);\n"
        "    return conn;\n"
        "  } catch (error) {\n"
        "    console.error(`Connection Error: ${error.message}`);\n"
        "    throw error;\n"
        "  }\n"
        "};\n"
        "module.exports = connectDB;"
    )
    story.append(Paragraph(format_code(db_code), styles['code']))
    story.append(Spacer(1, 10))

    # --- SECTION 6, 7, 8: SCHEMAS ---
    story.append(Paragraph("6. Schema 1: User Data Model (models/User.js)", styles['h1']))
    user_tbl = Table([
        [Paragraph("Field Name", styles['th']), Paragraph("Data Type", styles['th']), Paragraph("Rules", styles['th']), Paragraph("Purpose in Application", styles['th'])],
        [Paragraph("`_id`", styles['td']), Paragraph("ObjectId", styles['td']), Paragraph("Auto Unique", styles['td']), Paragraph("MongoDB Primary Key", styles['td'])],
        [Paragraph("`name`", styles['td']), Paragraph("String", styles['td']), Paragraph("Required, Trimmed", styles['td']), Paragraph("Full user name", styles['td'])],
        [Paragraph("`email`", styles['td']), Paragraph("String", styles['td']), Paragraph("Required, Unique, Lowercase", styles['td']), Paragraph("Login handle &amp; communication email", styles['td'])],
        [Paragraph("`password`", styles['td']), Paragraph("String", styles['td']), Paragraph("Required", styles['td']), Paragraph("Bcrypt hashed password", styles['td'])],
        [Paragraph("`isMentor`", styles['td']), Paragraph("Boolean", styles['td']), Paragraph("Default: `false`", styles['td']), Paragraph("Flag enabling mentor profile &amp; incoming request controls", styles['td'])],
        [Paragraph("`skills`", styles['td']), Paragraph("Array of Strings", styles['td']), Paragraph("Default: `[]`", styles['td']), Paragraph("Technical tags (e.g. Java, React, SQL)", styles['td'])],
        [Paragraph("`createdAt`", styles['td']), Paragraph("Date", styles['td']), Paragraph("Default: `Date.now`", styles['td']), Paragraph("Account creation timestamp", styles['td'])],
    ], colWidths=[70, 70, 110, 270])
    user_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(user_tbl)

    story.append(Paragraph("7. Schema 2: Proposal Data Model (models/Proposal.js)", styles['h1']))
    prop_tbl = Table([
        [Paragraph("Field Name", styles['th']), Paragraph("Data Type", styles['th']), Paragraph("Reference / Rules", styles['th']), Paragraph("Purpose in Application", styles['th'])],
        [Paragraph("`_id`", styles['td']), Paragraph("ObjectId", styles['td']), Paragraph("Auto Unique", styles['td']), Paragraph("Proposal Primary Key", styles['td'])],
        [Paragraph("`student`", styles['td']), Paragraph("ObjectId", styles['td']), Paragraph("Ref: `User` (Required)", styles['td']), Paragraph("FK referencing student who submitted doubt", styles['td'])],
        [Paragraph("`mentor`", styles['td']), Paragraph("ObjectId", styles['td']), Paragraph("Ref: `User` (Required)", styles['td']), Paragraph("FK referencing mentor selected for help", styles['td'])],
        [Paragraph("`studentEmail`", styles['td']), Paragraph("String", styles['td']), Paragraph("Required", styles['td']), Paragraph("Snapshot of student email address", styles['td'])],
        [Paragraph("`mentorEmail`", styles['td']), Paragraph("String", styles['td']), Paragraph("Required", styles['td']), Paragraph("Snapshot of mentor email address", styles['td'])],
        [Paragraph("`doubt`", styles['td']), Paragraph("String", styles['td']), Paragraph("Required", styles['td']), Paragraph("Technical doubt description text", styles['td'])],
        [Paragraph("`status`", styles['td']), Paragraph("String", styles['td']), Paragraph("`['pending', 'accepted', 'rejected']`", styles['td']), Paragraph("State machine status (default: 'pending')", styles['td'])],
        [Paragraph("`createdAt`", styles['td']), Paragraph("Date", styles['td']), Paragraph("Default: `Date.now`", styles['td']), Paragraph("Timestamp when request was sent", styles['td'])],
    ], colWidths=[75, 65, 125, 255])
    prop_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(prop_tbl)

    story.append(Paragraph("8. Schema 3: Session Data Model (models/Session.js)", styles['h1']))
    sess_tbl = Table([
        [Paragraph("Field Name", styles['th']), Paragraph("Data Type", styles['th']), Paragraph("Reference / Rules", styles['th']), Paragraph("Purpose in Application", styles['th'])],
        [Paragraph("`_id`", styles['td']), Paragraph("ObjectId", styles['td']), Paragraph("Auto Unique", styles['td']), Paragraph("Session Primary Key", styles['td'])],
        [Paragraph("`proposal`", styles['td']), Paragraph("ObjectId", styles['td']), Paragraph("Ref: `Proposal` (Required)", styles['td']), Paragraph("FK referencing accepted proposal", styles['td'])],
        [Paragraph("`student`", styles['td']), Paragraph("ObjectId", styles['td']), Paragraph("Ref: `User` (Required)", styles['td']), Paragraph("FK referencing student participant", styles['td'])],
        [Paragraph("`mentor`", styles['td']), Paragraph("ObjectId", styles['td']), Paragraph("Ref: `User` (Required)", styles['td']), Paragraph("FK referencing mentor host", styles['td'])],
        [Paragraph("`scheduledTime`", styles['td']), Paragraph("Date", styles['td']), Paragraph("Required (Future Date)", styles['td']), Paragraph("Conflict-free scheduled session date &amp; time", styles['td'])],
        [Paragraph("`meetingLink`", styles['td']), Paragraph("String", styles['td']), Paragraph("Required", styles['td']), Paragraph("Unique Jitsi Meet room URL (`https://meet.jit.si/...`)", styles['td'])],
        [Paragraph("`status`", styles['td']), Paragraph("String", styles['td']), Paragraph("`['scheduled', 'completed']`", styles['td']), Paragraph("Session status (default: 'scheduled')", styles['td'])],
    ], colWidths=[75, 65, 125, 255])
    sess_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(sess_tbl)
    story.append(Spacer(1, 10))

    # --- SECTION 11: SINGLE ACCOUNT DUAL ROLE ARCHITECTURE & DIAGRAM ---
    story.append(Paragraph("11. Single Account — Student + Mentor Architecture &amp; Diagram", styles['h1']))
    story.append(Paragraph(
        "Instead of maintaining split account types or separate login paths, GyaanSetu uses a <b>Single Account Architecture</b>. "
        "Every user is inherently a student. When a user clicks 'Become a Mentor', the API sets `isMentor = true` and updates `skills`. "
        "The exact same account immediately retains student capabilities while unlocking mentor features.",
        styles['body']
    ))
    
    # VISUAL DIAGRAM 3: DUAL ROLE
    if os.path.exists("diag3_dual_role.png"):
        story.append(PDFImage("diag3_dual_role.png", width=520, height=315))
        story.append(Paragraph("<i>Figure 11.1: Single Account Dual Role Capabilities &amp; Real Aditya Scenario Diagram</i>", styles['callout']))
        story.append(Spacer(1, 10))

    # --- SECTION 12 & 13: DATABASE ER & RELATIONSHIP DIAGRAMS ---
    story.append(Paragraph("12. Database Design &amp; Visual ER Diagram", styles['h1']))
    story.append(Paragraph("The database contains 3 normalized collections inside the `gyaansetu` database on MongoDB Atlas:", styles['body']))

    # VISUAL DIAGRAM 4: DATABASE ER
    if os.path.exists("diag4_database_er.png"):
        story.append(PDFImage("diag4_database_er.png", width=520, height=334))
        story.append(Paragraph("<i>Figure 12.1: GyaanSetu MongoDB Atlas ER Database Schema Diagram</i>", styles['callout']))
        story.append(Spacer(1, 10))

    story.append(Paragraph("13. Entity Relationship Visual Diagram", styles['h1']))
    # VISUAL DIAGRAM 5: RELATIONSHIPS
    if os.path.exists("diag5_relationships.png"):
        story.append(PDFImage("diag5_relationships.png", width=520, height=260))
        story.append(Paragraph("<i>Figure 13.1: Database Collections Entity Relationships Flow Diagram</i>", styles['callout']))
        story.append(Spacer(1, 10))

    # --- SECTION 14: DB LIFECYCLE DIAGRAM ---
    story.append(Paragraph("14. Database State Machine Lifecycle Diagram", styles['h1']))
    # VISUAL DIAGRAM 6: DB LIFECYCLE
    if os.path.exists("diag6_db_lifecycle.png"):
        story.append(PDFImage("diag6_db_lifecycle.png", width=520, height=278))
        story.append(Paragraph("<i>Figure 14.1: Database Documents State Machine Lifecycle Flowchart</i>", styles['callout']))
        story.append(Spacer(1, 10))

    # --- SECTION 15: WHY THREE COLLECTIONS ---
    story.append(Paragraph("15. Why Three Separate Collections?", styles['h1']))
    story.append(Paragraph("• <b>Why not embed proposals in User?</b> Unbounded array anti-pattern! If a popular mentor receives hundreds of proposals, embedding arrays would exceed MongoDB's 16MB document size limit.", styles['bullet']))
    story.append(Paragraph("• <b>Why separate Session from Proposal?</b> Separation of concerns! A proposal represents an intent/request, while a session represents an active scheduled event with time conflict validation and meeting URLs.", styles['bullet']))
    story.append(Spacer(1, 10))

    # --- SECTION 16: DB FLOWS ---
    story.append(Paragraph("16. Database Document Flow Examples", styles['h1']))
    story.append(Paragraph("<b>Scenario: From Doubt Request to Completed Session in MongoDB:</b><br/>"
                           "1. <b>Create Proposal:</b> `Proposal.create({ student: studentId, mentor: mentorId, doubt: 'Help with SQL', status: 'pending' })`<br/>"
                           "2. <b>Accept Proposal:</b> `Proposal.findByIdAndUpdate(proposalId, { status: 'accepted' })`<br/>"
                           "3. <b>Schedule Session:</b> `Session.create({ proposal: proposalId, student, mentor, scheduledTime, meetingLink })`<br/>"
                           "4. <b>Complete Session:</b> `Session.findByIdAndUpdate(sessionId, { status: 'completed' })`", styles['body']))
    story.append(Spacer(1, 10))

    # --- SECTION 17: MONGOOSE QUERIES ---
    story.append(Paragraph("17. Mongoose Query Methods Line-by-Line", styles['h1']))
    query_code = (
        "// 1. Fetch all mentors for directory page\n"
        "User.find({ isMentor: true }).select('-password').sort({ createdAt: -1 });\n\n"
        "// 2. Prevent duplicate active requests between same student & mentor\n"
        "Proposal.findOne({ student: studentId, mentor: mentorId, status: 'pending' });\n\n"
        "// 3. Time slot conflict query for scheduling\n"
        "Session.findOne({\n"
        "  status: 'scheduled',\n"
        "  $or: [\n"
        "    { mentor, scheduledTime: { $gte: startTimeWindow, $lte: endTimeWindow } },\n"
        "    { student, scheduledTime: { $gte: startTimeWindow, $lte: endTimeWindow } }\n"
        "  ]\n"
        "});\n\n"
        "// 4. Data enrichment using populate\n"
        "Proposal.find({ student: req.user._id }).populate('mentor', 'name email skills');"
    )
    story.append(Paragraph(format_code(query_code), styles['code']))
    story.append(Spacer(1, 10))

    # --- SECTION 18: LIFECYCLE TRACES ---
    story.append(Paragraph("18. Complete Request Lifecycle (9 Traces)", styles['h1']))
    story.append(Paragraph("<b>Trace 1: User Registration</b> ➔ POST `/api/auth/register` ➔ check existing email ➔ bcrypt hash ➔ `User.create` ➔ issue JWT.<br/>"
                           "<b>Trace 2: User Login</b> ➔ POST `/api/auth/login` ➔ find email ➔ `bcrypt.compare` ➔ issue JWT.<br/>"
                           "<b>Trace 3: Get Mentors</b> ➔ GET `/api/mentors` ➔ query `isMentor: true` ➔ return JSON directory.<br/>"
                           "<b>Trace 4: Send Doubt</b> ➔ POST `/api/proposals` ➔ check self-request &amp; duplicate ➔ `Proposal.create`.<br/>"
                           "<b>Trace 5: Accept Request</b> ➔ PATCH `/api/proposals/:id/accept` ➔ verify mentor ownership ➔ set status `'accepted'`.<br/>"
                           "<b>Trace 6: Become Mentor</b> ➔ PATCH `/api/users/become-mentor` ➔ parse skills array ➔ set `isMentor = true`.<br/>"
                           "<b>Trace 7: Schedule Session</b> ➔ POST `/api/sessions` ➔ check time conflict ➔ generate Jitsi link ➔ send email.<br/>"
                           "<b>Trace 8: Get Sessions</b> ➔ GET `/api/sessions/my` ➔ query `$or: [{ student }, { mentor }]` ➔ return sessions.<br/>"
                           "<b>Trace 9: Complete Session</b> ➔ PATCH `/api/sessions/:id/complete` ➔ verify mentor ownership ➔ set status `'completed'`.", styles['body']))
    story.append(Spacer(1, 10))

    # --- SECTION 19: ENVIRONMENT VARIABLES ---
    story.append(Paragraph("19. Environment Variables Security", styles['h1']))
    env_tbl = Table([
        [Paragraph("Variable Name", styles['th']), Paragraph("Purpose", styles['th']), Paragraph("Security Risk if Exposed", styles['th'])],
        [Paragraph("`PORT`", styles['td']), Paragraph("HTTP Server Port (default 5000)", styles['td']), Paragraph("Low (public network configuration)", styles['td'])],
        [Paragraph("`MONGO_URI`", styles['td']), Paragraph("MongoDB Atlas connection string", styles['td']), Paragraph("CRITICAL: Exposes database read/write access", styles['td'])],
        [Paragraph("`JWT_SECRET`", styles['td']), Paragraph("Secret key for signing auth tokens", styles['td']), Paragraph("CRITICAL: Allows attackers to forge fake auth tokens", styles['td'])],
        [Paragraph("`EMAIL_USER`", styles['td']), Paragraph("Nodemailer SMTP email address", styles['td']), Paragraph("Medium: Spam risk", styles['td'])],
        [Paragraph("`EMAIL_PASS`", styles['td']), Paragraph("SMTP application password", styles['td']), Paragraph("HIGH: Unauthorized email sending", styles['td'])],
    ], colWidths=[95, 175, 250])
    env_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(env_tbl)
    story.append(Spacer(1, 10))

    # --- SECTION 20: 60-SECOND REVISION SPEECHES ---
    story.append(Paragraph("20. 60-Second Architecture &amp; Database Speeches", styles['h1']))
    
    speech1 = (
        "<b>EXPLAIN MY PROJECT ARCHITECTURE IN 60 SECONDS:</b><br/>"
        "\"GyaanSetu is built on a decoupled MERN architecture. The frontend is a React 18 SPA compiled with Vite and styled using Tailwind CSS. "
        "It communicates statelessly with an Express REST API running on Node.js using Axios. "
        "Requests carry JWT tokens in the `Authorization: Bearer` header, which custom `protect` middleware verifies to populate `req.user`. "
        "Controllers execute business rules, validation, and conflict checks before persisting data into MongoDB Atlas via Mongoose ODM. "
        "We also integrate Nodemailer for session email alerts and Jitsi Meet for automated 1-on-1 video call rooms. "
        "The architecture enforces a single-account model where any student can upgrade to a mentor without separate logins.\""
    )
    story.append(Paragraph(speech1, styles['callout']))
    story.append(Spacer(1, 8))

    speech2 = (
        "<b>EXPLAIN MY DATABASE DESIGN IN 60 SECONDS:</b><br/>"
        "\"Our MongoDB Atlas database contains 3 normalized collections: `users`, `proposals`, and `sessions`. "
        "The `users` collection stores user details, hashed passwords, `isMentor` boolean flag, and skills array. "
        "The `proposals` collection links a student `ObjectId` to a mentor `ObjectId` along with the doubt description and status state machine (`pending`, `accepted`, `rejected`). "
        "The `sessions` collection links an accepted proposal to a scheduled time, status (`scheduled`, `completed`), and a generated Jitsi meeting URL. "
        "We use Mongoose `ObjectId` references to perform populated queries while avoiding unbounded array growth inside user documents.\""
    )
    story.append(Paragraph(speech2, styles['callout']))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_filename} successfully!")

if __name__ == '__main__':
    build_backend_pdf()
