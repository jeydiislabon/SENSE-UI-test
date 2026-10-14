from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from functools import wraps
import re

app = Flask(__name__)
app.secret_key = "sense-secret-key-change-in-production"

# ---------------------------------------------------------------------------
# FIXED CREDENTIALS — replace with DB lookup after Jamie's backend merges
# ---------------------------------------------------------------------------
USERS = {
    # Student
    "student":    {"password": "student123",  "role": "student",  "faculty_id": None},
    # Admin
    "admin":      {"password": "admin123",    "role": "admin",    "faculty_id": None},
    # Teachers — each tied to their faculty profile
    "acruz":      {"password": "teacher123",  "role": "teacher",  "faculty_id": 1},
    "mlim":       {"password": "teacher123",  "role": "teacher",  "faculty_id": 2},
    "rsantos":    {"password": "teacher123",  "role": "teacher",  "faculty_id": 3},
    "jdelarosa":  {"password": "teacher123",  "role": "teacher",  "faculty_id": 4},
    "ctorres":    {"password": "teacher123",  "role": "teacher",  "faculty_id": 5},
    "bvillanueva":{"password": "teacher123",  "role": "teacher",  "faculty_id": 6},
    "agomez":     {"password": "teacher123",  "role": "teacher",  "faculty_id": 7},
    "ereyes":     {"password": "teacher123",  "role": "teacher",  "faculty_id": 8},
}

# ---------------------------------------------------------------------------
# AUTH HELPERS
# ---------------------------------------------------------------------------

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not session.get("logged_in"):
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                # Allow admin to access teacher routes too
                if not (role == "teacher" and session.get("role") == "admin"):
                    return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated
    return decorator

# ---------------------------------------------------------------------------
# MOCK FACULTY DATA
# ---------------------------------------------------------------------------
FACULTY = [
    {
        "id": 1,
        "initials": "AC",
        "name": "Engr. Adrian Cruz",
        "role": "CpE Faculty",
        "email": "acruz@tip.edu.ph",
        "location": "CpE Department",
        "color": "#1A1A1A",
        "subject": "Embedded Systems",
        "accepting": True,
        "sentiment": {"positive": 65, "neutral": 20, "negative": 15},
        "summary": (
            "Students consistently appreciate the clear and structured teaching style. "
            "Feedback highlights approachable consultations and well-prepared lessons."
        ),
        "comments": [
            {"label": "Positive", "text": "Explains concepts clearly and always makes time for questions after class."},
            {"label": "Negative", "text": "Laboratory instructions could be posted earlier so we have more time to prepare."},
            {"label": "Neutral",  "text": "The course is challenging but fair, and the activities match the lesson."},
            {"label": "Positive", "text": "Very patient with students who ask follow-up questions."},
            {"label": "Neutral",  "text": "Some topics feel rushed near the end of the semester but overall it's manageable."},
        ],
    },
    {
        "id": 2,
        "initials": "ML",
        "name": "Engr. Maria Lim",
        "role": "CpE Faculty",
        "email": "mlim@tip.edu.ph",
        "location": "CpE Department",
        "color": "#1A1A1A",
        "subject": "Computer Networks 2",
        "accepting": True,
        "sentiment": {"positive": 58, "neutral": 28, "negative": 14},
        "summary": (
            "Feedback indicates well-organized and systematic lessons. "
            "Students note that project deadlines are sometimes clustered, but "
            "overall teaching delivery is rated positively."
        ),
        "comments": [
            {"label": "Neutral",  "text": "The lessons are organized, but the project deadlines sometimes feel too close together."},
            {"label": "Positive", "text": "Always explains the theory before the lab. It really helps to understand what we're doing."},
            {"label": "Negative", "text": "Grading rubrics could be clearer. It's hard to know what is expected in the output."},
            {"label": "Positive", "text": "Very responsive. Replies fast even outside of class hours."},
        ],
    },
    {
        "id": 3,
        "initials": "RS",
        "name": "Engr. Ramon Santos",
        "role": "CpE Faculty",
        "email": "rsantos@tip.edu.ph",
        "location": "CpE Department",
        "color": "#1A1A1A",
        "subject": "Data Structures & Algorithms",
        "accepting": True,
        "sentiment": {"positive": 72, "neutral": 18, "negative": 10},
        "summary": (
            "Receives strong positive feedback regarding practical guidance "
            "and project support. Students value the structured approach to "
            "teaching and availability during consultation hours."
        ),
        "comments": [
            {"label": "Positive", "text": "The code reviews were very helpful. I finally understood how to structure our final project."},
            {"label": "Positive", "text": "Gives detailed feedback on our outputs. It actually helps me improve."},
            {"label": "Neutral",  "text": "The pace is a bit fast but the slides are detailed enough to catch up."},
        ],
    },
    {
        "id": 4,
        "initials": "JD",
        "name": "Engr. Jose Dela Rosa",
        "role": "CpE Faculty",
        "email": "jdelarosa@tip.edu.ph",
        "location": "CpE Department",
        "color": "#1A1A1A",
        "subject": "Microprocessors & Microcontrollers",
        "accepting": True,
        "sentiment": {"positive": 60, "neutral": 25, "negative": 15},
        "summary": (
            "Students appreciate the technical depth of the lessons. "
            "Feedback highlights strong subject knowledge and clear "
            "explanations of complex engineering topics."
        ),
        "comments": [
            {"label": "Positive", "text": "Explains difficult topics in a very straightforward way."},
            {"label": "Negative", "text": "Laboratory instructions could be posted earlier so we have more time to prepare."},
            {"label": "Neutral",  "text": "The course is challenging but fair, and the activity matches the lesson."},
        ],
    },
    {
        "id": 5,
        "initials": "CT",
        "name": "Engr. Clara Torres",
        "role": "CpE Faculty",
        "email": "ctorres@tip.edu.ph",
        "location": "CpE Department",
        "color": "#FFD100",
        "subject": "Digital Signal Processing",
        "accepting": True,
        "sentiment": {"positive": 70, "neutral": 20, "negative": 10},
        "summary": (
            "Widely appreciated for an engaging and student-centered teaching style. "
            "Students feel comfortable asking questions and report high satisfaction "
            "with lesson delivery."
        ),
        "comments": [
            {"label": "Positive", "text": "Best class of the semester. Makes every topic feel relevant and interesting."},
            {"label": "Positive", "text": "Very approachable and understanding. Never makes you feel dumb for asking questions."},
            {"label": "Neutral",  "text": "Readings are a bit long but the discussions make up for it."},
        ],
    },
    {
        "id": 6,
        "initials": "BV",
        "name": "Engr. Bernard Villanueva",
        "role": "CpE Faculty",
        "email": "bvillanueva@tip.edu.ph",
        "location": "CpE Department",
        "color": "#1A1A1A",
        "subject": "Engineering Mathematics",
        "accepting": True,
        "sentiment": {"positive": 55, "neutral": 30, "negative": 15},
        "summary": (
            "Feedback reflects a knowledgeable instructor with real-world insights. "
            "Some students find the pace challenging, but appreciate the practical "
            "examples used in lectures."
        ),
        "comments": [
            {"label": "Neutral",  "text": "Topics are heavy but explains them step by step."},
            {"label": "Positive", "text": "Real-world examples make the subject feel practical and relevant."},
            {"label": "Negative", "text": "Quizzes are sometimes difficult and not fully aligned with the lecture slides."},
        ],
    },
    {
        "id": 7,
        "initials": "AG",
        "name": "Engr. Angela Gomez",
        "role": "CpE Faculty",
        "email": "agomez@tip.edu.ph",
        "location": "CpE Department",
        "color": "#1A1A1A",
        "subject": "Logic Circuits & Design",
        "accepting": True,
        "sentiment": {"positive": 62, "neutral": 22, "negative": 16},
        "summary": (
            "Students report a well-structured course with clear objectives. "
            "Consultation hours are appreciated and feedback highlights "
            "consistent and fair assessment practices."
        ),
        "comments": [
            {"label": "Positive", "text": "Always prepared for class and explains topics with good examples."},
            {"label": "Neutral",  "text": "The workload is manageable but deadlines could be spread out more."},
            {"label": "Negative", "text": "Would appreciate more feedback on submitted outputs."},
        ],
    },
    {
        "id": 8,
        "initials": "ER",
        "name": "Engr. Eduardo Reyes",
        "role": "CpE Faculty",
        "email": "ereyes@tip.edu.ph",
        "location": "CpE Department",
        "color": "#FFD100",
        "subject": "Computer Architecture",
        "accepting": True,
        "sentiment": {"positive": 68, "neutral": 22, "negative": 10},
        "summary": (
            "Receives consistently positive feedback for patience and clarity "
            "in teaching. Students highlight approachable teaching style and "
            "helpful guidance during laboratory sessions."
        ),
        "comments": [
            {"label": "Positive", "text": "Very patient and thorough. Always makes sure everyone understands before moving on."},
            {"label": "Positive", "text": "Lab sessions are well-guided and the instructions are clear."},
            {"label": "Neutral",  "text": "The course content is dense but the teaching style makes it easier to follow."},
        ],
    },
]

# ---------------------------------------------------------------------------
# MOCK NOISE LOG (Obj 1.1) — grows as students submit filtered feedback
# ---------------------------------------------------------------------------
NOISE_LOG = [
    {"faculty": "Engr. Adrian Cruz",      "text": "grr",           "reason": "Numbers/symbols only",   "type": "gibberish"},
    {"faculty": "Engr. Maria Lim",        "text": "asdasdasd",     "reason": "Random characters",      "type": "gibberish"},
    {"faculty": "Engr. Ramon Santos",     "text": "DINOROBONG",    "reason": "Keyboard pattern",       "type": "gibberish"},
    {"faculty": "Engr. Jose Dela Rosa",   "text": "67",            "reason": "Numbers only",           "type": "gibberish"},
    {"faculty": "Engr. Clara Torres",     "text": "Magaling siya naman", "reason": "Tagalog detected", "type": "tagalog"},
    {"faculty": "Engr. Bernard Villanueva","text": "okay lang po", "reason": "Tagalog detected",       "type": "tagalog"},
    {"faculty": "Engr. Angela Gomez",     "text": "lkjhgfdsa",     "reason": "Keyboard pattern",       "type": "gibberish"},
    {"faculty": "Engr. Eduardo Reyes",    "text": "Mahirap yung subjects", "reason": "Tagalog detected","type": "tagalog"},
    {"faculty": "Engr. Adrian Cruz",      "text": "n/a",           "reason": "Placeholder value",      "type": "gibberish"},
    {"faculty": "Engr. Maria Lim",        "text": "123456",        "reason": "Numbers only",           "type": "gibberish"},
]

# Valid submissions received during this session
VALID_SUBMISSIONS = [
    {"faculty": "Engr. Adrian Cruz",  "initials": "AC", "color": "#1A1A1A", "text": "Explains concepts clearly and always makes time for questions after class.", "rating": 5},
    {"faculty": "Engr. Maria Lim",    "initials": "ML", "color": "#1A1A1A", "text": "The lessons are organized but deadlines feel too close together.", "rating": 3},
    {"faculty": "Engr. Clara Torres", "initials": "CT", "color": "#FFD100", "text": "Best class this semester. Very engaging and practical.", "rating": 5},
]

LATEST_COMMENTS = [
    {"initials": "AC", "color": "#1A1A1A", "name": "Engr. Adrian Cruz",       "label": "Positive", "text": "Explains concepts clearly and always makes time for questions after class."},
    {"initials": "ML", "color": "#1A1A1A", "name": "Engr. Maria Lim",         "label": "Neutral",  "text": "The lessons are organized, but the project deadlines sometimes feel too close together."},
    {"initials": "CT", "color": "#FFD100", "name": "Engr. Clara Torres",      "label": "Positive", "text": "Best class of the semester. Makes every topic feel relevant and interesting."},
    {"initials": "RS", "color": "#1A1A1A", "name": "Engr. Ramon Santos",      "label": "Negative", "text": "Laboratory instructions could be posted earlier so we have more time to prepare."},
]

STATS = {
    "total_feedback": 248,
    "total_advisors": len(FACULTY),
    "noise_filtered": len(NOISE_LOG),
}

# ---------------------------------------------------------------------------
# NOISE DETECTION (Obj 1.1) — frontend-side validation
# ---------------------------------------------------------------------------

# Common Tagalog words/markers
TAGALOG_WORDS = {
    "yung","ng","mga","naman","kasi","po","ako","siya","niya","nila",
    "kami","kayo","tayo","ito","iyon","dito","doon","at","sa","na",
    "ang","mga","pero","kaya","lang","din","rin","pala","talaga",
    "parang","kahit","kung","dahil","para","may","wala","hindi",
    "oo","opo","nope","yep","yep","sige","okay","ok","grabe",
    "sobra","lagi","palagi","minsan","madalas","basta","ganon",
    "ganyan","ganito","pwede","di","daw","raw","ba","nga","eh",
    "ay","ha","huh","ano","bakit","saan","kailan","sino",
    "magaling","mahirap","madali","masaya","malungkot","maganda",
    "pangit","mahal","mura","bago","luma","mabuti","masama",
    "okay lang","hindi naman","maayos","marami","konti","lahat",
    "walang","mayroong","gustong","gusto","ayaw","kailangan",
    "nagtuturo","nagtuturo","nagpapaliwanag","inirerekumenda",
    "sinasabi","sinabi","binibigay","ibinigay","tinuturuan",
    "itinuturo","ginagawa","ginawa","gagawin"
}

def detect_noise(text):
    """
    Returns a dict: { "is_noise": bool, "reason": str, "type": str }
    Types: "tagalog", "gibberish", "too_short", "numbers_only", "clean"
    """
    t = text.strip()

    # Too short
    if len(t) < 5:
        return {"is_noise": True, "reason": "Response is too short", "type": "too_short"}

    # Numbers / symbols only
    if re.match(r'^[\d\s\W]+$', t):
        return {"is_noise": True, "reason": "Numbers or symbols only", "type": "gibberish"}

    # Repeated characters (e.g. aaaaaaa, lkjhgfds)
    if re.match(r'^(.)\1{4,}$', t):
        return {"is_noise": True, "reason": "Repeated characters", "type": "gibberish"}

    # No vowels at all (keyboard spam)
    letters = re.sub(r'[^a-zA-Z]', '', t)
    if len(letters) > 4:
        vowels = re.sub(r'[^aeiouAEIOU]', '', letters)
        if len(vowels) == 0:
            return {"is_noise": True, "reason": "Keyboard pattern detected", "type": "gibberish"}

    # Tagalog detection
    words = re.findall(r'\b\w+\b', t.lower())
    tagalog_hits = [w for w in words if w in TAGALOG_WORDS]
    if len(tagalog_hits) >= 2 or (len(tagalog_hits) >= 1 and len(words) <= 4):
        return {"is_noise": True, "reason": f"Tagalog detected: {', '.join(tagalog_hits)}", "type": "tagalog"}

    return {"is_noise": False, "reason": "", "type": "clean"}

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    if session.get("logged_in"):
        if session.get("role") == "student":
            return redirect(url_for("student_dashboard"))
        elif session.get("role") == "teacher":
            return redirect(url_for("teacher_dashboard"))
        else:
            return redirect(url_for("admin_dashboard"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        selected_role = request.form.get("selected_role", "student").strip()
        user = USERS.get(username)

        if user and user["password"] == password:
            # Block if selected role doesn't match account role
            if user["role"] != selected_role:
                role_labels = {"student": "Student", "teacher": "Teacher", "admin": "Admin"}
                error = f"This account is not a {role_labels.get(selected_role, selected_role)} account. Please select the correct role."
            else:
                session["logged_in"] = True
                session["username"] = username
                session["role"] = user["role"]
                session["faculty_id"] = user.get("faculty_id")
                if user["role"] == "student":
                    return redirect(url_for("student_dashboard"))
                elif user["role"] == "teacher":
                    return redirect(url_for("teacher_dashboard"))
                else:
                    return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---- STUDENT ROUTES ----

@app.route("/student/dashboard")
@login_required(role="student")
def student_dashboard():
    return render_template("student_dashboard.html", faculty=FACULTY)


@app.route("/student/evaluate/<int:faculty_id>", methods=["GET"])
@login_required(role="student")
def evaluate(faculty_id):
    member = next((f for f in FACULTY if f["id"] == faculty_id), None)
    if not member:
        return redirect(url_for("student_dashboard"))
    return render_template("evaluate.html", member=member)


@app.route("/student/submit/<int:faculty_id>", methods=["POST"])
@login_required(role="student")
def submit_evaluation(faculty_id):
    """
    Obj 1.1 — Noise filtration on submission.
    Checks for Tagalog, gibberish, too-short, numbers-only.
    """
    data = request.json
    text = data.get("text", "").strip()
    rating = data.get("rating", 0)

    if not text:
        return jsonify({"status": "error", "message": "Please enter your feedback."}), 400

    noise = detect_noise(text)

    if noise["is_noise"]:
        # Log it (in production this goes to DB)
        member = next((f for f in FACULTY if f["id"] == faculty_id), None)
        if member:
            NOISE_LOG.append({
                "faculty": member["name"],
                "text": text,
                "reason": noise["reason"],
                "type": noise["type"]
            })
            STATS["noise_filtered"] = len(NOISE_LOG)

        if noise["type"] == "tagalog":
            return jsonify({
                "status": "noise",
                "type": "tagalog",
                "message": "Please write your feedback in English. Tagalog responses cannot be processed by our system."
            })
        else:
            return jsonify({
                "status": "noise",
                "type": "gibberish",
                "message": "Your response appears to be invalid. Please write a meaningful evaluation in English."
            })

    # Valid — store in VALID_SUBMISSIONS
    import random
    label = random.choice(["Positive", "Neutral", "Negative"])
    member = next((f for f in FACULTY if f["id"] == faculty_id), None)
    if member:
        VALID_SUBMISSIONS.append({
            "faculty":  member["name"],
            "initials": member["initials"],
            "color":    member["color"],
            "text":     text,
            "rating":   rating,
            "label":    label,
        })
        STATS["total_feedback"] = 248 + len(VALID_SUBMISSIONS)
    return jsonify({
        "status": "success",
        "label": label,
        "message": "Thank you for completing this semester's evaluation. Your feedback has been recorded."
    })


# ---- TEACHER ROUTES ----

@app.route("/teacher/dashboard")
@login_required(role="teacher")
def teacher_dashboard():
    faculty_id = session.get("faculty_id")
    member = next((f for f in FACULTY if f["id"] == faculty_id), None)
    if not member:
        return redirect(url_for("logout"))

    # Get this teacher's noise entries
    my_noise = [n for n in NOISE_LOG if n["faculty"] == member["name"]]
    tagalog_count  = sum(1 for n in my_noise if n["type"] == "tagalog")
    gibberish_count = sum(1 for n in my_noise if n["type"] != "tagalog")

    return render_template("teacher_dashboard.html",
                           member=member,
                           my_noise=my_noise,
                           tagalog_count=tagalog_count,
                           gibberish_count=gibberish_count)


# ---- ADMIN ROUTES ----

@app.route("/admin/dashboard")
@login_required(role="admin")
def admin_dashboard():
    # Noise stats for Obj 1.1
    tagalog_count  = sum(1 for n in NOISE_LOG if n["type"] == "tagalog")
    gibberish_count = sum(1 for n in NOISE_LOG if n["type"] != "tagalog")

    return render_template("admin_dashboard.html",
                           stats=STATS,
                           latest_comments=LATEST_COMMENTS,
                           noise_log=NOISE_LOG,
                           valid_submissions=VALID_SUBMISSIONS,
                           tagalog_count=tagalog_count,
                           gibberish_count=gibberish_count,
                           faculty=FACULTY)


@app.route("/admin/faculty/<int:faculty_id>")
@login_required(role="admin")
def admin_faculty(faculty_id):
    member = next((f for f in FACULTY if f["id"] == faculty_id), None)
    if not member:
        return redirect(url_for("admin_dashboard"))
    faculty_noise = [n for n in NOISE_LOG if n["faculty"] == member["name"]]
    return render_template("faculty.html", member=member, faculty_noise=faculty_noise)


@app.route("/admin/advisors")
@login_required(role="admin")
def advisors():
    query = request.args.get("q", "").lower()
    results = [f for f in FACULTY if query in f["name"].lower()] if query else FACULTY
    return render_template("advisors.html", faculty=results, query=query)


# ---- NOISE CHECK API (called by JS before submit) ----
@app.route("/api/check_noise", methods=["POST"])
def check_noise_api():
    text = request.json.get("text", "").strip()
    result = detect_noise(text)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
