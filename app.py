from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "sense-secret-key-change-in-production"

# ---------------------------------------------------------------------------
# MOCK ADMIN CREDENTIALS — replace with DB lookup after Jamie's backend merges
# ---------------------------------------------------------------------------
ADMIN_CREDENTIALS = {
    "admin": "sense2024",
}

# ---------------------------------------------------------------------------
# AUTH HELPERS
# ---------------------------------------------------------------------------

def login_required(f):
    """Decorator — redirects to login if not authenticated.
    NOTE: temporarily disabled for development. Re-enable by uncommenting the check below.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        # if not session.get("logged_in"):
        #     return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated

# ---------------------------------------------------------------------------
# MOCK DATA — replace with real NLP pipeline results later
# ---------------------------------------------------------------------------

FACULTY = [
    {
        "id": 1,
        "initials": "RV",
        "name": "Engr. Robin Valenzuela",
        "role": "CpE Faculty",
        "email": "rvalenzuela@university.edu",
        "location": "CpE Department",
        "color": "#6C5CE7",
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
        "initials": "NL",
        "name": "Engr. Noel Jason Lusung",
        "role": "CpE Faculty",
        "email": "njlusung@university.edu",
        "location": "CpE Department",
        "color": "#6C5CE7",
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
        "initials": "LP",
        "name": "Engr. Lloyd Aldrin Pornobi",
        "role": "CpE Faculty",
        "email": "lapornobi@university.edu",
        "location": "CpE Department",
        "color": "#6C5CE7",
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
        "initials": "JG",
        "name": "Engr. Ji Han Gang",
        "role": "CpE Faculty",
        "email": "jhgang@university.edu",
        "location": "CpE Department",
        "color": "#6C5CE7",
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
        "initials": "MR",
        "name": "Engr. Menchie Rosales",
        "role": "CpE Faculty",
        "email": "mrosales@university.edu",
        "location": "CpE Department",
        "color": "#E84393",
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
        "initials": "JQ",
        "name": "Engr. Jimlord Quejado",
        "role": "CpE Faculty",
        "email": "jquejado@university.edu",
        "location": "CpE Department",
        "color": "#6C5CE7",
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
        "initials": "VN",
        "name": "Engr. Verlyn Nojor",
        "role": "CpE Faculty",
        "email": "vnojor@university.edu",
        "location": "CpE Department",
        "color": "#6C5CE7",
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
        "initials": "LB",
        "name": "Engr. Leah Balaya",
        "role": "CpE Faculty",
        "email": "lbalaya@university.edu",
        "location": "CpE Department",
        "color": "#E84393",
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

NOISE_LOG = [
    {"text": '"grr"',         "reason": "Numbers only"},
    {"text": '"asdasdasd"',   "reason": "Random characters"},
    {"text": '"DINOROBONG"',  "reason": "Keyboard pattern"},
    {"text": '"67"',          "reason": "Numbers only"},
    {"text": '"........."',   "reason": "Punctuation only"},
    {"text": '"lkjhgfdsa"',   "reason": "Keyboard pattern"},
    {"text": '"123456"',      "reason": "Numbers only"},
    {"text": '"n/a"',         "reason": "Placeholder value"},
]

LATEST_COMMENTS = [
    {"initials": "RV", "color": "#6C5CE7", "name": "Engr. Robin Valenzuela",    "label": "Positive", "text": "Explains concepts clearly and always makes time for questions after class."},
    {"initials": "NL", "color": "#6C5CE7", "name": "Engr. Noel Jason Lusung",   "label": "Neutral",  "text": "The lessons are organized, but the project deadlines sometimes feel too close together."},
    {"initials": "MR", "color": "#E84393", "name": "Engr. Menchie Rosales",     "label": "Positive", "text": "Best class of the semester. Makes every topic feel relevant and interesting."},
    {"initials": "LP", "color": "#6C5CE7", "name": "Engr. Lloyd Aldrin Pornobi","label": "Negative", "text": "Laboratory instructions could be posted earlier so we have more time to prepare."},
]

STATS = {
    "total_feedback": 248,
    "total_advisors": len(FACULTY),
    "noise_filtered": len(NOISE_LOG),
}

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def welcome():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        if ADMIN_CREDENTIALS.get(username) == password:
            session["logged_in"] = True
            session["username"] = username
            next_page = request.args.get("next", "/dashboard")
            return redirect(next_page)
        else:
            error = "Invalid username or password."
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("welcome"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html",
                           stats=STATS,
                           latest_comments=LATEST_COMMENTS,
                           noise_log=NOISE_LOG)


@app.route("/advisors")
@login_required
def advisors():
    query = request.args.get("q", "").lower()
    results = [f for f in FACULTY if query in f["name"].lower()] if query else FACULTY
    return render_template("advisors.html", faculty=results, query=query)


@app.route("/faculty/<int:faculty_id>")
@login_required
def faculty(faculty_id):
    member = next((f for f in FACULTY if f["id"] == faculty_id), None)
    if not member:
        return redirect(url_for("advisors"))
    return render_template("faculty.html", member=member)


@app.route("/submit_feedback/<int:faculty_id>", methods=["POST"])
def submit_feedback(faculty_id):
    """
    Stub endpoint — in production this would run noise filtration,
    normalization, sentiment classification, and summarization.
    For now it just echoes back a mock sentiment result.
    Students do NOT need to be logged in to submit feedback.
    """
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"error": "Empty feedback"}), 400

    # Mock sentiment (rotate through for demo purposes)
    import random
    label = random.choice(["Positive", "Neutral", "Negative"])
    return jsonify({"label": label, "message": "Feedback submitted successfully."})


if __name__ == "__main__":
    app.run(debug=True)
