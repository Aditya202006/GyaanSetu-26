import os
from PIL import Image, ImageDraw, ImageFont

def draw_rounded_rect(draw, box, radius, fill, outline, width=2):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color='#2563EB', width=3, arrow_size=10):
    x1, y1 = start
    x2, y2 = end
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    
    # Calculate arrowhead polygon depending on direction
    if x1 == x2: # Vertical arrow
        if y2 > y1: # Down
            p1 = (x2, y2)
            p2 = (x2 - arrow_size, y2 - arrow_size)
            p3 = (x2 + arrow_size, y2 - arrow_size)
        else: # Up
            p1 = (x2, y2)
            p2 = (x2 - arrow_size, y2 + arrow_size)
            p3 = (x2 + arrow_size, y2 + arrow_size)
    else: # Horizontal arrow
        if x2 > x1: # Right
            p1 = (x2, y2)
            p2 = (x2 - arrow_size, y2 - arrow_size)
            p3 = (x2 - arrow_size, y2 + arrow_size)
        else: # Left
            p1 = (x2, y2)
            p2 = (x2 + arrow_size, y2 - arrow_size)
            p3 = (x2 + arrow_size, y2 + arrow_size)
    draw.polygon([p1, p2, p3], fill=color)

def get_font(size=18, bold=False):
    # Try loading default TTF fonts, fallback to default font if unavailable
    font_names = ["arialbd.ttf" if bold else "arial.ttf", "calibribd.ttf" if bold else "calibri.ttf", "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

# -------------------------------------------------------------
# DIAGRAM 1: PROJECT ARCHITECTURE DIAGRAM
# -------------------------------------------------------------
def build_diag1():
    img = Image.new('RGB', (1400, 1000), color='#FFFFFF')
    draw = ImageDraw.Draw(img)
    
    title_font = get_font(24, bold=True)
    box_title_font = get_font(18, bold=True)
    text_font = get_font(15, bold=False)

    # Title Banner
    draw_rounded_rect(draw, [50, 20, 1350, 70], radius=8, fill='#1E3A8A', outline='#1E3A8A')
    draw.text((700, 45), "GyaanSetu System Architecture & Component Interactions", fill='#FFFFFF', font=title_font, anchor="mm")

    # Main Stack Nodes
    nodes = [
        ("USER (Browser / Student & Mentor)", 450, 100, 950, 150, '#EFF6FF', '#2563EB', '#1E3A8A'),
        ("React Frontend (Vite + React Router + Tailwind CSS)", 400, 200, 1000, 250, '#F0FDFA', '#0D9488', '#0F766E'),
        ("Axios HTTP Client (Authorization: Bearer <token>)", 420, 300, 980, 350, '#FEF3C7', '#D97706', '#92400E'),
        ("Express REST API Backend (Node.js App Server)", 400, 400, 1000, 450, '#EFF6FF', '#2563EB', '#1E3A8A'),
        ("Authentication Middleware (protect - JWT Verification)", 400, 500, 1000, 550, '#FDF2F8', '#DB2777', '#9D174D'),
        ("Controller Business Logic Layer (auth, user, mentor, proposal, session)", 350, 600, 1050, 650, '#F0FDF4', '#16A34A', '#15803D'),
        ("Mongoose ODM Layer (User, Proposal, Session Models)", 400, 700, 1000, 750, '#FFF7ED', '#EA580C', '#C2410C'),
        ("MongoDB Atlas Database Cluster (Cloud users, proposals, sessions)", 380, 800, 1020, 850, '#F0FDFA', '#0D9488', '#0F766E'),
    ]

    for label, x1, y1, x2, y2, bg, border, tc in nodes:
        draw_rounded_rect(draw, [x1, y1, x2, y2], radius=10, fill=bg, outline=border, width=2)
        draw.text(((x1 + x2)//2, (y1 + y2)//2), label, fill=tc, font=box_title_font, anchor="mm")

    # Connecting Arrows Downwards
    for i in range(len(nodes) - 1):
        _, _, _, _, y2_prev, _, _, _ = nodes[i]
        _, _, _, _, y1_next, _, _, _ = nodes[i+1]
        draw_arrow(draw, (700, y2_prev), (700, y1_next), color='#2563EB', width=3, arrow_size=8)

    # External Services Side Nodes
    # Nodemailer
    draw_rounded_rect(draw, [50, 400, 320, 470], radius=10, fill='#FEE2E2', outline='#DC2626', width=2)
    draw.text((185, 435), "Nodemailer (SMTP Emails)", fill='#991B1B', font=box_title_font, anchor="mm")
    draw_arrow(draw, (400, 425), (320, 425), color='#DC2626', width=3, arrow_size=8)

    draw_rounded_rect(draw, [50, 500, 320, 560], radius=10, fill='#FEF3C7', outline='#D97706', width=2)
    draw.text((185, 530), "Student & Mentor Emails", fill='#92400E', font=text_font, anchor="mm")
    draw_arrow(draw, (185, 470), (185, 500), color='#D97706', width=3, arrow_size=8)

    # Jitsi Meet
    draw_rounded_rect(draw, [1080, 400, 1350, 470], radius=10, fill='#F3E8FF', outline='#9333EA', width=2)
    draw.text((1215, 435), "Jitsi Meet (Video Call)", fill='#6B21A8', font=box_title_font, anchor="mm")
    draw_arrow(draw, (1000, 425), (1080, 425), color='#9333EA', width=3, arrow_size=8)

    draw_rounded_rect(draw, [1080, 500, 1350, 560], radius=10, fill='#EFF6FF', outline='#2563EB', width=2)
    draw.text((1215, 530), "https://meet.jit.si/gyaansetu-...", fill='#1E3A8A', font=text_font, anchor="mm")
    draw_arrow(draw, (1215, 470), (1215, 500), color='#2563EB', width=3, arrow_size=8)

    img.save("diag1_architecture.png")
    print("Created diag1_architecture.png")

# -------------------------------------------------------------
# DIAGRAM 2: BUSINESS FLOWCHART DIAGRAM
# -------------------------------------------------------------
def build_diag2():
    img = Image.new('RGB', (1400, 950), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    title_font = get_font(22, bold=True)
    box_font = get_font(16, bold=True)

    draw_rounded_rect(draw, [50, 20, 1350, 70], radius=8, fill='#1E3A8A', outline='#1E3A8A')
    draw.text((700, 45), "Complete GyaanSetu End-to-End Business & Data Flowchart", fill='#FFFFFF', font=title_font, anchor="mm")

    steps = [
        ("1. Student Browses Mentors Page", 100, 120, 450, 170, '#EFF6FF', '#2563EB'),
        ("2. Student Selects Mentor & Sends Doubt Request", 500, 120, 900, 170, '#EFF6FF', '#2563EB'),
        ("3. Proposal Saved in DB (status: 'pending')", 950, 120, 1300, 170, '#FEF3C7', '#D97706'),
        
        ("6. Schedule Session (Pick Date & Time)", 950, 270, 1300, 320, '#F0FDF4', '#16A34A'),
        ("5. Mentor Reviews Request in Dashboard", 500, 270, 900, 320, '#EFF6FF', '#2563EB'),
        ("4. If Rejected -> status: 'rejected'", 100, 270, 450, 320, '#FEE2E2', '#DC2626'),
        
        ("7. Verify Time Conflicts against DB", 950, 420, 1300, 470, '#FEF3C7', '#D97706'),
        ("8. Generate Unique Jitsi Room URL", 500, 420, 900, 470, '#F3E8FF', '#9333EA'),
        ("9. Dispatch Email Alerts via Nodemailer", 100, 420, 450, 470, '#FEE2E2', '#DC2626'),
        
        ("12. Mentor Marks Session Completed", 100, 570, 450, 620, '#F0FDF4', '#16A34A'),
        ("11. Student & Mentor Join Jitsi Video Room", 500, 570, 900, 620, '#F3E8FF', '#9333EA'),
        ("10. Session Saved in DB (status: 'scheduled')", 950, 570, 1300, 620, '#F0FDFA', '#0D9488'),
    ]

    for label, x1, y1, x2, y2, bg, border in steps:
        draw_rounded_rect(draw, [x1, y1, x2, y2], radius=8, fill=bg, outline=border, width=2)
        draw.text(((x1 + x2)//2, (y1 + y2)//2), label, fill='#1F2937', font=box_font, anchor="mm")

    # Connect flow steps
    draw_arrow(draw, (450, 145), (500, 145), color='#2563EB')
    draw_arrow(draw, (900, 145), (950, 145), color='#2563EB')
    draw_arrow(draw, (1125, 170), (1125, 270), color='#2563EB')
    draw_arrow(draw, (950, 295), (900, 295), color='#2563EB')
    draw_arrow(draw, (500, 295), (450, 295), color='#DC2626')
    draw_arrow(draw, (1125, 320), (1125, 420), color='#16A34A')
    draw_arrow(draw, (950, 445), (900, 445), color='#9333EA')
    draw_arrow(draw, (500, 445), (450, 445), color='#DC2626')
    draw_arrow(draw, (275, 470), (275, 570), color='#2563EB')
    draw_arrow(draw, (450, 595), (500, 595), color='#9333EA')
    draw_arrow(draw, (900, 595), (950, 595), color='#0D9488')

    img.save("diag2_business_flow.png")
    print("Created diag2_business_flow.png")

# -------------------------------------------------------------
# DIAGRAM 3: SINGLE ACCOUNT DUAL ROLE DIAGRAM
# -------------------------------------------------------------
def build_diag3():
    img = Image.new('RGB', (1400, 850), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    title_font = get_font(24, bold=True)
    box_title_font = get_font(18, bold=True)
    text_font = get_font(15, bold=False)

    draw_rounded_rect(draw, [50, 20, 1350, 70], radius=8, fill='#1E3A8A', outline='#1E3A8A')
    draw.text((700, 45), "Single Account Architecture — Student & Mentor Dual Capabilities", fill='#FFFFFF', font=title_font, anchor="mm")

    # Root User Box
    draw_rounded_rect(draw, [450, 100, 950, 180], radius=12, fill='#EFF6FF', outline='#2563EB', width=3)
    draw.text((700, 125), "ONE UNIFIED USER ACCOUNT", fill='#1E3A8A', font=box_title_font, anchor="mm")
    draw.text((700, 155), "Schema: { name, email, password, isMentor, skills }", fill='#4B5563', font=text_font, anchor="mm")

    # Split Lines
    draw_arrow(draw, (700, 180), (350, 260), color='#2563EB', width=3)
    draw_arrow(draw, (700, 180), (1050, 260), color='#D97706', width=3)

    # Student Side Box
    draw_rounded_rect(draw, [100, 260, 600, 650], radius=12, fill='#F0FDFA', outline='#0D9488', width=2)
    draw_rounded_rect(draw, [120, 280, 580, 330], radius=6, fill='#0D9488', outline='#0D9488')
    draw.text((350, 305), "STUDENT FEATURES (Default: isMentor = false)", fill='#FFFFFF', font=box_title_font, anchor="mm")

    student_items = [
        "✔ Browse Verified Mentors Directory",
        "✔ Search Mentors by Skill (e.g. Java, React, SQL)",
        "✔ Submit Doubt Proposals to Target Mentor",
        "✔ Track Request Status (Pending / Accepted / Rejected)",
        "✔ View Scheduled 1-on-1 Sessions",
        "✔ Join Jitsi Video Meeting Room"
    ]
    for idx, item in enumerate(student_items):
        draw.text((140, 360 + idx * 45), item, fill='#0F766E', font=text_font)

    # Mentor Side Box
    draw_rounded_rect(draw, [800, 260, 1300, 650], radius=12, fill='#FEF3C7', outline='#D97706', width=2)
    draw_rounded_rect(draw, [820, 280, 1280, 330], radius=6, fill='#D97706', outline='#D97706')
    draw.text((1050, 305), "MENTOR FEATURES (Unlocked: isMentor = true)", fill='#FFFFFF', font=box_title_font, anchor="mm")

    mentor_items = [
        "⚡ Click 'Become a Mentor' CTA Button",
        "⚡ Add/Edit Technical Skills (e.g. Java, DSA)",
        "⚡ Receive Incoming Student Doubt Requests",
        "⚡ Accept or Reject Pending Proposals",
        "⚡ Schedule Session (Conflict-Free Slot)",
        "⚡ Mark Mentoring Session Completed"
    ]
    for idx, item in enumerate(mentor_items):
        draw.text((840, 360 + idx * 45), item, fill='#92400E', font=text_font)

    # Real Scenario Callout Box at bottom
    draw_rounded_rect(draw, [100, 690, 1300, 780], radius=10, fill='#F8FAFC', outline='#CBD5E1', width=2)
    scenario_text = "Real Scenario: Aditya registers ➔ requests Rahul for help ➔ Aditya clicks 'Become a Mentor' ➔ Priya requests Aditya for Java help."
    draw.text((700, 720), "Aditya Scenario:", fill='#1E3A8A', font=get_font(16, bold=True), anchor="mm")
    draw.text((700, 750), scenario_text, fill='#334155', font=text_font, anchor="mm")

    img.save("diag3_dual_role.png")
    print("Created diag3_dual_role.png")

# -------------------------------------------------------------
# DIAGRAM 4: DATABASE ER ARCHITECTURE DIAGRAM
# -------------------------------------------------------------
def build_diag4():
    img = Image.new('RGB', (1400, 900), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    title_font = get_font(24, bold=True)
    tbl_title_font = get_font(18, bold=True)
    field_font = get_font(14, bold=False)

    draw_rounded_rect(draw, [50, 20, 1350, 70], radius=8, fill='#1E3A8A', outline='#1E3A8A')
    draw.text((700, 45), "GyaanSetu MongoDB Atlas ER Database Schema Diagram", fill='#FFFFFF', font=title_font, anchor="mm")

    # USERS Table Box
    draw_rounded_rect(draw, [50, 120, 420, 520], radius=10, fill='#FFFFFF', outline='#2563EB', width=2)
    draw_rounded_rect(draw, [50, 120, 420, 170], radius=8, fill='#2563EB', outline='#2563EB')
    draw.text((235, 145), "USERS Collection", fill='#FFFFFF', font=tbl_title_font, anchor="mm")

    user_fields = [
        "🔑 _id (ObjectId) [PK]",
        "• name (String)",
        "• email (String - Unique)",
        "• password (String - Bcrypt)",
        "• isMentor (Boolean)",
        "• skills (Array of Strings)",
        "• createdAt (Date)"
    ]
    for idx, f in enumerate(user_fields):
        draw.text((70, 195 + idx * 42), f, fill='#1F2937', font=field_font)

    # PROPOSALS Table Box
    draw_rounded_rect(draw, [510, 120, 890, 550], radius=10, fill='#FFFFFF', outline='#D97706', width=2)
    draw_rounded_rect(draw, [510, 120, 890, 170], radius=8, fill='#D97706', outline='#D97706')
    draw.text((700, 145), "PROPOSALS Collection", fill='#FFFFFF', font=tbl_title_font, anchor="mm")

    prop_fields = [
        "🔑 _id (ObjectId) [PK]",
        "🔗 student (FK ➔ User._id)",
        "🔗 mentor  (FK ➔ User._id)",
        "• studentEmail (String)",
        "• mentorEmail (String)",
        "• doubt (String)",
        "• status (pending/accepted/rejected)",
        "• createdAt (Date)"
    ]
    for idx, f in enumerate(prop_fields):
        draw.text((530, 195 + idx * 42), f, fill='#1F2937', font=field_font)

    # SESSIONS Table Box
    draw_rounded_rect(draw, [980, 120, 1360, 600], radius=10, fill='#FFFFFF', outline='#0D9488', width=2)
    draw_rounded_rect(draw, [980, 120, 1360, 170], radius=8, fill='#0D9488', outline='#0D9488')
    draw.text((1170, 145), "SESSIONS Collection", fill='#FFFFFF', font=tbl_title_font, anchor="mm")

    sess_fields = [
        "🔑 _id (ObjectId) [PK]",
        "🔗 proposal (FK ➔ Proposal._id)",
        "🔗 student  (FK ➔ User._id)",
        "🔗 mentor   (FK ➔ User._id)",
        "• studentEmail (String)",
        "• mentorEmail (String)",
        "• scheduledTime (Date)",
        "• meetingLink (Jitsi URL)",
        "• status (scheduled/completed)",
        "• createdAt (Date)"
    ]
    for idx, f in enumerate(sess_fields):
        draw.text((1000, 195 + idx * 40), f, fill='#1F2937', font=field_font)

    # Relationships Connectors
    # User -> Proposal Student FK
    draw_arrow(draw, (420, 235), (510, 235), color='#2563EB', width=3)
    draw.text((465, 220), "student", fill='#2563EB', font=get_font(12, bold=True), anchor="mm")

    # User -> Proposal Mentor FK
    draw_arrow(draw, (420, 275), (510, 275), color='#D97706', width=3)
    draw.text((465, 260), "mentor", fill='#D97706', font=get_font(12, bold=True), anchor="mm")

    # Proposal -> Session Proposal FK
    draw_arrow(draw, (890, 235), (980, 235), color='#0D9488', width=3)
    draw.text((935, 220), "accepted", fill='#0D9488', font=get_font(12, bold=True), anchor="mm")

    # Bottom Legend / Summary
    draw_rounded_rect(draw, [50, 680, 1360, 830], radius=10, fill='#F8FAFC', outline='#CBD5E1', width=2)
    legend_text = (
        "Mongoose ObjectId References & Integrity Rules:\n"
        "1. proposal.student & proposal.mentor store User ObjectIds (Mongoose populate('student mentor')).\n"
        "2. session.proposal stores Proposal ObjectId (links accepted doubt to scheduled time & Jitsi room).\n"
        "3. Decoupling rationale: Keeps user documents small and avoids 16MB document size limit."
    )
    draw.text((700, 755), legend_text, fill='#334155', font=get_font(15, bold=False), anchor="mm")

    img.save("diag4_database_er.png")
    print("Created diag4_database_er.png")

# -------------------------------------------------------------
# DIAGRAM 5: RELATIONSHIP FLOW DIAGRAM
# -------------------------------------------------------------
def build_diag5():
    img = Image.new('RGB', (1400, 700), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    title_font = get_font(24, bold=True)
    box_font = get_font(18, bold=True)
    text_font = get_font(15, bold=False)

    draw_rounded_rect(draw, [50, 20, 1350, 70], radius=8, fill='#1E3A8A', outline='#1E3A8A')
    draw.text((700, 45), "GyaanSetu Database Entity Relationships Summary", fill='#FFFFFF', font=title_font, anchor="mm")

    # USER Node
    draw_rounded_rect(draw, [550, 110, 850, 180], radius=10, fill='#EFF6FF', outline='#2563EB', width=3)
    draw.text((700, 145), "USER Collection", fill='#1E3A8A', font=box_font, anchor="mm")

    # Left & Right Branch to Proposal
    draw_arrow(draw, (620, 180), (450, 290), color='#2563EB', width=3)
    draw.text((515, 220), "student (1:N)", fill='#2563EB', font=text_font, anchor="mm")

    draw_arrow(draw, (780, 180), (950, 290), color='#D97706', width=3)
    draw.text((885, 220), "mentor (1:N)", fill='#D97706', font=text_font, anchor="mm")

    # PROPOSAL Node
    draw_rounded_rect(draw, [500, 290, 900, 360], radius=10, fill='#FEF3C7', outline='#D97706', width=3)
    draw.text((700, 325), "PROPOSAL Collection (status: pending/accepted/rejected)", fill='#92400E', font=box_font, anchor="mm")

    # Proposal to Session
    draw_arrow(draw, (700, 360), (700, 470), color='#16A34A', width=3)
    draw.text((770, 415), "if accepted (1:1)", fill='#16A34A', font=text_font, anchor="mm")

    # SESSION Node
    draw_rounded_rect(draw, [480, 470, 920, 540], radius=10, fill='#F0FDFA', outline='#0D9488', width=3)
    draw.text((700, 505), "SESSION Collection (scheduledTime + Jitsi URL)", fill='#0F766E', font=box_font, anchor="mm")

    img.save("diag5_relationships.png")
    print("Created diag5_relationships.png")

# -------------------------------------------------------------
# DIAGRAM 6: DATABASE STATE LIFECYCLE DIAGRAM
# -------------------------------------------------------------
def build_diag6():
    img = Image.new('RGB', (1400, 750), color='#FFFFFF')
    draw = ImageDraw.Draw(img)

    title_font = get_font(22, bold=True)
    box_font = get_font(16, bold=True)

    draw_rounded_rect(draw, [50, 20, 1350, 70], radius=8, fill='#1E3A8A', outline='#1E3A8A')
    draw.text((700, 45), "Database State Machine Lifecycle Flowchart", fill='#FFFFFF', font=title_font, anchor="mm")

    states = [
        ("1. USER CREATED\n(isMentor = false, skills = [])", 50, 150, 300, 230, '#EFF6FF', '#2563EB'),
        ("2. USER BECOMES MENTOR\n(isMentor = true, skills saved)", 380, 150, 680, 230, '#FEF3C7', '#D97706'),
        ("3. STUDENT SENDS DOUBT\n(Proposal created, status = 'pending')", 760, 150, 1100, 230, '#EFF6FF', '#2563EB'),
        
        ("6. SESSION COMPLETED\n(Session status = 'completed')", 760, 400, 1100, 480, '#F0FDF4', '#16A34A'),
        ("5. SESSION CREATED\n(Session status = 'scheduled')", 380, 400, 680, 480, '#F0FDFA', '#0D9488'),
        ("4. MENTOR ACCEPTS\n(Proposal status = 'accepted')", 50, 400, 300, 480, '#F0FDF4', '#16A34A'),
    ]

    for label, x1, y1, x2, y2, bg, border in states:
        draw_rounded_rect(draw, [x1, y1, x2, y2], radius=10, fill=bg, outline=border, width=2)
        lines = label.split('\n')
        if len(lines) == 1:
            draw.text(((x1+x2)//2, (y1+y2)//2), lines[0], fill='#1F2937', font=box_font, anchor="mm")
        else:
            draw.text(((x1+x2)//2, (y1+y2)//2 - 12), lines[0], fill='#1E3A8A', font=box_font, anchor="mm")
            draw.text(((x1+x2)//2, (y1+y2)//2 + 14), lines[1], fill='#374151', font=get_font(13, bold=False), anchor="mm")

    draw_arrow(draw, (300, 190), (380, 190), color='#2563EB', width=3)
    draw_arrow(draw, (680, 190), (760, 190), color='#D97706', width=3)
    draw_arrow(draw, (930, 230), (930, 320), color='#16A34A', width=3)
    draw_arrow(draw, (930, 320), (175, 320), color='#16A34A', width=3)
    draw_arrow(draw, (175, 320), (175, 400), color='#16A34A', width=3)
    draw_arrow(draw, (300, 440), (380, 440), color='#0D9488', width=3)
    draw_arrow(draw, (680, 440), (760, 440), color='#16A34A', width=3)

    img.save("diag6_db_lifecycle.png")
    print("Created diag6_db_lifecycle.png")

if __name__ == '__main__':
    build_diag1()
    build_diag2()
    build_diag3()
    build_diag4()
    build_diag5()
    build_diag6()
    print("All 6 PNG diagrams generated successfully!")
