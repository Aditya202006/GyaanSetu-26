import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from build_pdfs import NumberedCanvas, create_pdf_styles, clean_text, format_code

def build_frontend_pdf():
    pdf_filename = "GyaanSetu_Frontend_Deep_Dive.pdf"
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
    story.append(Spacer(1, 40))
    story.append(Paragraph("GyaanSetu Frontend Deep Dive", styles['title']))
    story.append(Paragraph("A Comprehensive, Code-by-Code Technical Analysis of the React 18, Vite &amp; Tailwind CSS Architecture for Placement Preparation", styles['subtitle']))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#1E3A8A'), spaceBefore=10, spaceAfter=20))

    meta_table = Table([
        [Paragraph("<b>Author / Candidate:</b>", styles['td']), Paragraph("Placement Candidate (Aditya)", styles['td'])],
        [Paragraph("<b>Project Name:</b>", styles['td']), Paragraph("GyaanSetu – Mentor-Student Doubt Solving Platform", styles['td'])],
        [Paragraph("<b>Frontend Stack:</b>", styles['td']), Paragraph("React 18, Vite, React Router v6, Axios, Tailwind CSS, Lucide React Icons", styles['td'])],
        [Paragraph("<b>Document Scope:</b>", styles['td']), Paragraph("Complete source component analysis, React Hooks breakdown, AuthContext &amp; routing logic", styles['td'])],
        [Paragraph("<b>Target Role:</b>", styles['td']), Paragraph("Frontend Developer / React Engineer / Full-Stack SDE", styles['td'])],
    ], colWidths=[140, 380])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 30))

    # Table of Contents
    story.append(Paragraph("<b>Table of Contents</b>", styles['h2']))
    toc_data = [
        ["1. Frontend Overview & Architecture", "8. Pages Detailed Analysis"],
        ["2. Actual Frontend Folder Structure", "9. React Hooks Deep Dive"],
        ["3. Core Files (main.jsx, App.jsx, index.css)", "10. Conditional UI & Dual-Role Rendering"],
        ["4. Client Routing & Protected Routes", "11. End-to-End Frontend User Flows"],
        ["5. Auth Context & State Management", "12. Controlled Forms & API States"],
        ["6. Central Axios Service & Interceptors", "13. Tailwind CSS & UI Design Patterns"],
        ["7. Reusable Components Breakdown", "14. Frontend Placement Revision Notes"]
    ]
    toc_table = Table(toc_data, colWidths=[250, 270])
    toc_table.setStyle(TableStyle([
        ('PADDING', (0,0), (-1,-1), 4),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#1E3A8A')),
    ]))
    story.append(toc_table)
    story.append(PageBreak())

    # --- SECTION 1: OVERVIEW & ARCHITECTURE ---
    story.append(Paragraph("1. Frontend Overview &amp; Architecture", styles['h1']))
    story.append(Paragraph(
        "The GyaanSetu frontend is a Single Page Application (SPA) built using React 18, Vite, and Tailwind CSS. "
        "It communicates asynchronously with the Express backend API via Axios. Client-side routing is handled by React Router v6, "
        "and user identity state is managed globally using React Context (`AuthContext`).",
        styles['body']
    ))
    
    story.append(Paragraph("<b>Why this frontend stack was chosen:</b>", styles['h2']))
    story.append(Paragraph("• <b>React 18:</b> Component-driven architecture allowing fast re-renders, virtual DOM diffing, and declarative UI states.", styles['bullet']))
    story.append(Paragraph("• <b>Vite:</b> Next-generation build tool providing instantaneous Hot Module Replacement (HMR) and optimized Rollup production bundling.", styles['bullet']))
    story.append(Paragraph("• <b>React Router v6:</b> Provides client-side dynamic route navigation without page reloads.", styles['bullet']))
    story.append(Paragraph("• <b>Axios:</b> Promise-based HTTP client equipped with request interceptors for automated Bearer token injection.", styles['bullet']))
    story.append(Paragraph("• <b>Tailwind CSS:</b> Utility-first CSS framework delivering clean responsive styling without heavy CSS bloat.", styles['bullet']))

    story.append(Paragraph("<b>Frontend Component Interaction Lifecycle:</b>", styles['h2']))
    arch_box = Paragraph(
        "<b>User Action (e.g. Click Button)</b> -&gt; <b>Event Handler (handleSubmit)</b> -&gt; <b>API Call (Axios Service)</b> -&gt; "
        "<b>Backend REST API</b> -&gt; <b>JSON Response</b> -&gt; <b>State Update (useState / AuthContext)</b> -&gt; <b>React UI Re-render</b>",
        styles['callout']
    )
    story.append(arch_box)
    story.append(Spacer(1, 10))

    # --- SECTION 2: FOLDER STRUCTURE ---
    story.append(Paragraph("2. Actual Frontend Folder Structure", styles['h1']))
    story.append(Paragraph("The frontend code lives in `client/` and is organized modularly by concerns:", styles['body']))
    
    struct_code = (
        "client/\n"
        "├── src/\n"
        "│   ├── components/\n"
        "│   │   ├── Navbar.jsx               # Top navigation bar with role badges & persona actions\n"
        "│   │   ├── BecomeMentorModal.jsx    # Modal form to submit technical skills and become mentor\n"
        "│   │   ├── RequestDoubtModal.jsx    # Modal form to send doubt requests to a target mentor\n"
        "│   │   ├── ScheduleModal.jsx        # Modal form for mentors to pick date & time for session\n"
        "│   │   └── ProtectedRoute.jsx       # Route guard component restricting unauthenticated users\n"
        "│   ├── context/\n"
        "│   │   └── AuthContext.jsx          # React Context holding user state, JWT token, login & logout\n"
        "│   ├── pages/\n"
        "│   │   ├── Home.jsx                 # Landing page with CTA hero & feature cards\n"
        "│   │   ├── Login.jsx                # Login page with clean single account login form\n"
        "│   │   ├── Register.jsx             # User registration page\n"
        "│   │   ├── Mentors.jsx              # Mentor directory with real-time name & skill search\n"
        "│   │   ├── Dashboard.jsx            # Unified dashboard showing student requests & mentor requests\n"
        "│   │   ├── Sessions.jsx             # Mentoring sessions list with Jitsi join links\n"
        "│   │   └── Profile.jsx              # User profile & skill editor page\n"
        "│   ├── services/\n"
        "│   │   └── api.js                   # Axios client instance with Authorization Bearer header interceptor\n"
        "│   ├── App.jsx                      # Main router setup & global modal container\n"
        "│   ├── main.jsx                     # React DOM root entry point\n"
        "│   └── index.css                    # Tailwind CSS directives & global base styles\n"
        "├── package.json                     # Frontend dependencies (React, Vite, React Router, Axios, Lucide)\n"
        "├── vite.config.js                   # Vite dev server & API proxy configuration\n"
        "├── tailwind.config.js               # Tailwind theme customization\n"
        "├── postcss.config.js                # PostCSS Tailwind processor config\n"
        "└── vercel.json                      # Vercel deployment rewrite rule for SPA routing"
    )
    story.append(Paragraph(format_code(struct_code), styles['code']))
    story.append(Spacer(1, 10))

    # --- SECTION 3: CORE FILES ---
    story.append(Paragraph("3. Core Files (main.jsx, App.jsx, index.css)", styles['h1']))
    
    story.append(Paragraph("<b>A. main.jsx:</b> Initializes the React DOM root element and renders `<App />` inside `<React.StrictMode>`.", styles['body']))
    main_code = (
        "import React from 'react';\n"
        "import ReactDOM from 'react-dom/client';\n"
        "import App from './App.jsx';\n"
        "import './index.css';\n\n"
        "ReactDOM.createRoot(document.getElementById('root')).render(\n"
        "  <React.StrictMode>\n"
        "    <App />\n"
        "  </React.StrictMode>,\n"
        ");"
    )
    story.append(Paragraph(format_code(main_code), styles['code']))

    story.append(Paragraph("<b>B. App.jsx:</b> Encloses the application in `<AuthProvider>` and `<Router>`, defines page routes, and holds state for the global `<BecomeMentorModal />`.", styles['body']))
    app_code = (
        "import React, { useState } from 'react';\n"
        "import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';\n"
        "import { AuthProvider } from './context/AuthContext';\n"
        "import Navbar from './components/Navbar';\n"
        "import BecomeMentorModal from './components/BecomeMentorModal';\n"
        "import ProtectedRoute from './components/ProtectedRoute';\n"
        "// Pages import...\n\n"
        "function App() {\n"
        "  const [isBecomeMentorModalOpen, setIsBecomeMentorModalOpen] = useState(false);\n"
        "  return (\n"
        "    <AuthProvider>\n"
        "      <Router>\n"
        "        <Navbar onOpenBecomeMentor={() => setIsBecomeMentorModalOpen(true)} />\n"
        "        <Routes>\n"
        "          <Route path='/' element={<Home onOpenBecomeMentor={() => setIsBecomeMentorModalOpen(true)} />} />\n"
        "          <Route path='/login' element={<Login />} />\n"
        "          <Route path='/register' element={<Register />} />\n"
        "          <Route path='/mentors' element={<Mentors />} />\n"
        "          <Route path='/dashboard' element={<ProtectedRoute><Dashboard onOpenBecomeMentor={() => setIsBecomeMentorModalOpen(true)} /></ProtectedRoute>} />\n"
        "          <Route path='/sessions' element={<ProtectedRoute><Sessions /></ProtectedRoute>} />\n"
        "          <Route path='/profile' element={<ProtectedRoute><Profile onOpenBecomeMentor={() => setIsBecomeMentorModalOpen(true)} /></ProtectedRoute>} />\n"
        "        </Routes>\n"
        "        <BecomeMentorModal isOpen={isBecomeMentorModalOpen} onClose={() => setIsBecomeMentorModalOpen(false)} />\n"
        "      </Router>\n"
        "    </AuthProvider>\n"
        "  );\n"
        "}"
    )
    story.append(Paragraph(format_code(app_code), styles['code']))
    story.append(Spacer(1, 10))

    # --- SECTION 4: ROUTING ---
    story.append(Paragraph("4. Client Routing &amp; Protected Routes", styles['h1']))
    story.append(Paragraph("Routing is configured using React Router v6. Protected pages (`/dashboard`, `/sessions`, `/profile`) are wrapped in `<ProtectedRoute>`.", styles['body']))

    routes_tbl = Table([
        [Paragraph("Path", styles['th']), Paragraph("Component Rendered", styles['th']), Paragraph("Access Level", styles['th']), Paragraph("Purpose", styles['th'])],
        [Paragraph("`/`", styles['td']), Paragraph("`Home.jsx`", styles['td']), Paragraph("Public", styles['td']), Paragraph("Landing hero page &amp; platform overview", styles['td'])],
        [Paragraph("`/login`", styles['td']), Paragraph("`Login.jsx`", styles['td']), Paragraph("Public", styles['td']), Paragraph("User authentication login form", styles['td'])],
        [Paragraph("`/register`", styles['td']), Paragraph("`Register.jsx`", styles['td']), Paragraph("Public", styles['td']), Paragraph("User account registration form", styles['td'])],
        [Paragraph("`/mentors`", styles['td']), Paragraph("`Mentors.jsx`", styles['td']), Paragraph("Public", styles['td']), Paragraph("Mentor directory with skill search &amp; doubt request trigger", styles['td'])],
        [Paragraph("`/dashboard`", styles['td']), Paragraph("`Dashboard.jsx`", styles['td']), Paragraph("Protected", styles['td']), Paragraph("Unified dashboard for student requests &amp; mentor incoming requests", styles['td'])],
        [Paragraph("`/sessions`", styles['td']), Paragraph("`Sessions.jsx`", styles['td']), Paragraph("Protected", styles['td']), Paragraph("List of scheduled &amp; completed mentoring sessions with Jitsi URLs", styles['td'])],
        [Paragraph("`/profile`", styles['td']), Paragraph("`Profile.jsx`", styles['td']), Paragraph("Protected", styles['td']), Paragraph("User details view &amp; mentor skills editor", styles['td'])],
    ], colWidths=[70, 100, 75, 275])
    routes_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(routes_tbl)
    story.append(Spacer(1, 10))

    # --- SECTION 5: AUTH CONTEXT ---
    story.append(Paragraph("5. Auth Context &amp; State Management (AuthContext.jsx)", styles['h1']))
    story.append(Paragraph("`AuthContext` provides global user identity state across all components without prop drilling.", styles['body']))

    auth_code = (
        "import React, { createContext, useState, useEffect } from 'react';\n"
        "import API from '../services/api';\n\n"
        "export const AuthContext = createContext();\n\n"
        "export const AuthProvider = ({ children }) => {\n"
        "  const [user, setUser] = useState(null);\n"
        "  const [token, setToken] = useState(localStorage.getItem('gyaansetu_token') || null);\n"
        "  const [loading, setLoading] = useState(true);\n\n"
        "  useEffect(() => {\n"
        "    const checkLoggedInUser = async () => {\n"
        "      if (token) {\n"
        "        try {\n"
        "          const response = await API.get('/auth/me');\n"
        "          if (response.data.success) setUser(response.data.user);\n"
        "        } catch (error) { logout(); }\n"
        "      }\n"
        "      setLoading(false);\n"
        "    };\n"
        "    checkLoggedInUser();\n"
        "  }, [token]);\n\n"
        "  const login = (userData, userToken) => {\n"
        "    localStorage.setItem('gyaansetu_token', userToken);\n"
        "    setToken(userToken);\n"
        "    setUser(userData);\n"
        "  };\n"
        "  const logout = () => {\n"
        "    localStorage.removeItem('gyaansetu_token');\n"
        "    setToken(null);\n"
        "    setUser(null);\n"
        "  };\n"
        "  const updateUser = (updatedUser) => setUser(updatedUser);\n"
        "  return (\n"
        "    <AuthContext.Provider value={{ user, token, loading, login, logout, updateUser }}>\n"
        "      {children}\n"
        "    </AuthContext.Provider>\n"
        "  );\n"
        "};"
    )
    story.append(Paragraph(format_code(auth_code), styles['code']))
    story.append(Spacer(1, 10))

    # --- SECTION 6: AXIOS SERVICE ---
    story.append(Paragraph("6. Central Axios Service &amp; Interceptors (api.js)", styles['h1']))
    story.append(Paragraph("`client/src/services/api.js` creates a single Axios client configured with a request interceptor.", styles['body']))

    api_code = (
        "import axios from 'axios';\n\n"
        "const API = axios.create({\n"
        "  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api'\n"
        "});\n\n"
        "// Automatically attach Authorization Bearer token to all outgoing protected requests\n"
        "API.interceptors.request.use((config) => {\n"
        "  const token = localStorage.getItem('gyaansetu_token');\n"
        "  if (token) {\n"
        "    config.headers.Authorization = `Bearer ${token}`;\n"
        "  }\n"
        "  return config;\n"
        "}, (error) => Promise.reject(error));\n\n"
        "export default API;"
    )
    story.append(Paragraph(format_code(api_code), styles['code']))
    story.append(Paragraph("<b>Why Interceptors are crucial:</b> Prevents manual token handling on every API call. Every request automatically includes `Authorization: Bearer <token>`.", styles['callout']))
    story.append(Spacer(1, 10))

    # --- SECTION 7: COMPONENTS BREAKDOWN ---
    story.append(Paragraph("7. Reusable Components Breakdown", styles['h1']))
    
    story.append(Paragraph("<b>A. Navbar.jsx:</b> Renders logo branding, main menu links (`Home`, `Mentors`, `Dashboard`, `Sessions`), and user persona status. If `user.isMentor === false`, displays the 'Become a Mentor' CTA button.", styles['body']))
    story.append(Paragraph("<b>B. BecomeMentorModal.jsx:</b> Modal form allowing logged-in students to enter comma-separated skills and call `PATCH /api/users/become-mentor`.", styles['body']))
    story.append(Paragraph("<b>C. RequestDoubtModal.jsx:</b> Modal form triggered from mentor cards allowing students to submit technical doubts via `POST /api/proposals`.", styles['body']))
    story.append(Paragraph("<b>D. ScheduleModal.jsx:</b> Modal dialog used by mentors to pick date &amp; time (`POST /api/sessions`), checking conflicts and generating Jitsi URLs.", styles['body']))
    story.append(Paragraph("<b>E. ProtectedRoute.jsx:</b> Checks `token` from `AuthContext`. If unauthenticated, redirects to `/login` using `<Navigate to='/login' replace />`.", styles['body']))
    story.append(Spacer(1, 10))

    # --- SECTION 8: PAGES DETAILED ANALYSIS ---
    story.append(Paragraph("8. Pages Detailed Analysis", styles['h1']))
    story.append(Paragraph("• <b>Home.jsx:</b> Hero landing page showcasing tagline 'Connect. Learn. Solve.', CTA buttons, and platform overview cards.", styles['bullet']))
    story.append(Paragraph("• <b>Login.jsx &amp; Register.jsx:</b> Controlled forms managing auth submission, error alerts, and redirect handling.", styles['bullet']))
    story.append(Paragraph("• <b>Mentors.jsx:</b> Renders mentor directory with client-side real-time filtering by name and skills. Prevents self-requesting by hiding the 'Ask Doubt' button on the user's own card.", styles['bullet']))
    story.append(Paragraph("• <b>Dashboard.jsx:</b> Unified dual-role dashboard. Renders 'My Requests' for student mode and 'Incoming Requests' for mentor mode.", styles['bullet']))
    story.append(Paragraph("• <b>Sessions.jsx:</b> Displays scheduled &amp; completed sessions with direct external Jitsi video call links and 'Mark Complete' action buttons.", styles['bullet']))
    story.append(Paragraph("• <b>Profile.jsx:</b> User details overview and skill tag editor for mentors.", styles['bullet']))
    story.append(Spacer(1, 10))

    # --- SECTION 9: REACT HOOKS DEEP DIVE ---
    story.append(Paragraph("9. React Hooks Deep Dive", styles['h1']))
    hooks_tbl = Table([
        [Paragraph("React Hook", styles['th']), Paragraph("Purpose &amp; Usage in GyaanSetu", styles['th']), Paragraph("Example Usage File", styles['th'])],
        [Paragraph("`useState`", styles['td']), Paragraph("Local component state management (form inputs, loading spinners, modal visibility)", styles['td']), Paragraph("`Login.jsx`, `Mentors.jsx`", styles['td'])],
        [Paragraph("`useEffect`", styles['td']), Paragraph("Side-effect execution on mount (fetching mentors, sync auth token, fetching dashboard data)", styles['td']), Paragraph("`Dashboard.jsx`, `Mentors.jsx`", styles['td'])],
        [Paragraph("`useContext`", styles['td']), Paragraph("Consuming global `AuthContext` state (`user`, `login`, `logout`) without prop drilling", styles['td']), Paragraph("`Navbar.jsx`, `Dashboard.jsx`", styles['td'])],
        [Paragraph("`useNavigate`", styles['td']), Paragraph("Programmatic client-side navigation between routes", styles['td']), Paragraph("`Register.jsx`, `Login.jsx`", styles['td'])],
        [Paragraph("`useLocation`", styles['td']), Paragraph("Accessing current URL location &amp; state passed during navigation", styles['td']), Paragraph("`Login.jsx`", styles['td'])],
    ], colWidths=[90, 290, 140])
    hooks_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(hooks_tbl)
    story.append(Spacer(1, 10))

    # --- SECTION 10 & 11: CONDITIONAL UI & USER FLOWS ---
    story.append(Paragraph("10. Conditional UI &amp; Dual-Role Rendering", styles['h1']))
    story.append(Paragraph("The UI dynamically renders capabilities based on `user.isMentor`:<br/>"
                           "• If `isMentor === false`: Shows 'Become a Mentor' amber CTA button.<br/>"
                           "• If `isMentor === true`: Shows 'Active Mentor' badge and enables 'Incoming Requests' and 'My Mentoring Sessions' on Dashboard.", styles['body']))

    story.append(Paragraph("11. End-to-End Frontend User Flows", styles['h1']))
    story.append(Paragraph("<b>Complete Lifecycle Flow:</b><br/>"
                           "1. User registers (`/register`) ➔ redirects to Login (`/login`).<br/>"
                           "2. Logged-in student browses Mentors (`/mentors`), searches 'React', clicks 'Ask Doubt'.<br/>"
                           "3. Mentor logs in, opens Dashboard (`/dashboard`), sees incoming request, clicks 'Accept' then 'Schedule Session'.<br/>"
                           "4. Both users open Sessions (`/sessions`) and click 'Join Meeting' (opens Jitsi URL in new tab).<br/>"
                           "5. Student clicks 'Become a Mentor' in top bar, enters skills ➔ account gains full mentor capabilities!", styles['body']))
    story.append(Spacer(1, 10))

    # --- SECTION 12 & 13: FORMS & STYLING ---
    story.append(Paragraph("12. Controlled Forms &amp; API States", styles['h1']))
    story.append(Paragraph("All inputs use controlled components (`value={email} onChange={(e) => setEmail(e.target.value)}`). Submit buttons handle loading disable state (`disabled={loading}`) to prevent double submissions.", styles['body']))

    story.append(Paragraph("13. Tailwind CSS &amp; UI Design Patterns", styles['h1']))
    story.append(Paragraph("Uses a clean, placement-ready blue/indigo design system (`bg-blue-600`, `hover:bg-blue-700`, `bg-amber-500`, `rounded-xl`, `shadow-sm`) with Lucide React icons (`GraduationCap`, `Users`, `Calendar`, `Video`).", styles['body']))
    story.append(Spacer(1, 10))

    # --- SECTION 14: REVISION NOTES ---
    story.append(Paragraph("14. Frontend Placement Revision Notes", styles['h1']))
    rev_box = (
        "<b>Key Frontend Concepts to Speak in Interviews:</b><br/>"
        "• <b>Single Page Application (SPA):</b> Only one HTML page (`index.html`) is loaded. React Router updates the view dynamically without browser page reloads.<br/>"
        "• <b>Virtual DOM:</b> React keeps a lightweight in-memory copy of the DOM. When state changes, React computes diffs and updates only changed real DOM nodes.<br/>"
        "• <b>Controlled Components:</b> Form input state is bound to React state (`useState`), making React the single source of truth.<br/>"
        "• <b>Axios Interceptors:</b> Centralizes auth token headers, so individual components do not need to manually pass Authorization headers.<br/>"
        "• <b>Context API:</b> Eliminates prop drilling by making auth state globally accessible via `useContext(AuthContext)`."
    )
    story.append(Paragraph(rev_box, styles['callout']))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {pdf_filename} successfully!")

if __name__ == '__main__':
    build_frontend_pdf()
