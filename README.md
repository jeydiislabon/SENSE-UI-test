================================================================================
                    SENSE - SENTIMENT FACULTY EVALUATION ANALYSIS SYSTEM
================================================================================

Version: 1.0.0
Python: 3.8+
Developed by: SENSE Team

================================================================================
ABOUT SENSE
================================================================================

SENSE is a web-based Student Portal that processes and analyzes open-ended
student feedback submitted through an integrated interface. The system addresses
the problem of unstructured faculty evaluation comments that may contain informal
language, Taglish, abbreviations, and meaningless inputs such as random
keystrokes and numerical gibberish.

The system performs three core NLP functions:

  1. Noise Filtration & Text Normalization
     Detects and discards invalid inputs before processing. Normalizes
     informal, code-mixed, and Taglish text into machine-readable format.

  2. Sentiment Analysis
     Classifies each meaningful comment as Positive, Neutral, or Negative
     using a fine-tuned RoBERTa model.

  3. Automatic Summarization
     Generates concise summaries of recurring feedback using a BART model,
     along with a quantitative report of filtered noise entries.

================================================================================
HOW TO USE THE SYSTEM
================================================================================

1. WELCOME PAGE
---------------
- Displays the system tagline and project description
- Click "Enter dashboard" to access the portal
- No login required for students submitting feedback

2. DASHBOARD
------------
- Displays an overview of evaluation activity across the department
- Shows three summary statistics:
    Total Feedback   — total number of submitted student comments
    Advisors         — total number of faculty listed in the system
    Noise Filtered   — total number of invalid inputs automatically removed
- Latest Comments section shows recently submitted feedback with sentiment tags
- Noise Audit Log shows automatically filtered responses with their reason
  (e.g., random characters, keyboard pattern, numbers only)

3. ADVISORS / FACULTY DIRECTORY
--------------------------------
- Lists all CpE faculty members in a searchable grid
- Each card shows the faculty member's name, role, and avatar initials
- Use the search bar to filter faculty by name
- Click any card to view the individual faculty profile

4. INDIVIDUAL FACULTY PAGE
---------------------------
- Displays the faculty member's profile information
- Sentiment Overview shows the Positive / Neutral / Negative percentage
  breakdown based on submitted comments, with a visual progress bar
- Sentiment Distribution shows a donut chart visualization
- Comment Summary displays an AI-generated summary of recurring feedback
  (noise entries are excluded from the summary)
- Share Your Feedback form allows students to submit anonymous comments
  directly — sentiment is analyzed automatically upon submission
- Recent Feedback section lists the latest comments with sentiment labels

================================================================================
KEY FEATURES
================================================================================

- Anonymous Feedback Submission — students submit comments without logging in
- Noise Filtration — automatically detects and discards gibberish, random
  keystrokes, numerical-only inputs, and placeholder values
- Text Normalization — processes Taglish, informal language, abbreviations,
  and student slang into machine-readable format
- Sentiment Classification — classifies feedback as Positive, Neutral, or
  Negative using RoBERTa
- Automatic Summarization — generates concise summaries of recurring student
  opinions using BART
- Noise Audit Log — quantitative report of filtered invalid inputs
- Faculty Directory — searchable grid of all CpE faculty members
- Sentiment Visualization — donut chart and percentage breakdown per faculty
- Admin Login — dashboard access restricted to authorized personnel
- Responsive UI — works across desktop and tablet screen sizes

================================================================================
GETTING STARTED
================================================================================

PREREQUISITES
-------------
- Python 3.8 or higher
- pip package manager
- XAMPP (for MariaDB database — handled by the backend team)

INSTALLATION
------------
1. Clone the repository:
   git clone https://github.com/<org>/sense.git

2. Switch to the frontend branch:
   git checkout feature/frontend-ui

3. Navigate to the project folder:
   cd sense-ui

4. Install required dependencies:
   python -m pip install -r requirements.txt

   Or manually install:
   python -m pip install flask==3.0.3

5. Run the application:
   python app.py

6. Open your browser at:
   http://127.0.0.1:5000

WINDOWS NOTE
------------
If "python" is not recognized, use the full path:
  C:\Users\<your-username>\AppData\Local\Programs\Python\Python312\python.exe app.py

To share with groupmates on the same Wi-Fi network, run:
  python -c "from app import app; app.run(host='0.0.0.0', port=5000, debug=True)"

Then share your local IP address (e.g., http://192.168.x.x:5000)

================================================================================
SYSTEM PAGES & ROUTES
================================================================================

  /               Welcome page
  /login          Admin login page
  /logout         Logs out and returns to welcome page
  /dashboard      Overview dashboard (protected)
  /advisors       Faculty directory (protected)
  /faculty/<id>   Individual faculty profile (protected)
  /submit_feedback/<id>   Anonymous feedback submission endpoint (public)

================================================================================
TECHNICAL INFORMATION
================================================================================

TECHNOLOGY STACK
----------------
- Python 3.x       — Core programming language
- Flask 3.0.3      — Web framework and routing
- Jinja2           — HTML templating (bundled with Flask)
- HTML / CSS / JS  — Frontend interface
- Chart.js         — Sentiment donut chart visualization (CDN)
- MariaDB          — Database for storing evaluation data (via XAMPP)
- FastAPI          — Backend API for NLP pipeline integration
- RoBERTa          — Sentiment classification model
- BART             — Automatic summarization model

BRANCH STRUCTURE
----------------
- feature/frontend-ui      Frontend dashboard UI (HTML/CSS/JS + Flask)
- feature/backend-db       Database schema and API routing (MariaDB + FastAPI)
- feature/nlp-training     Sentiment analysis and noise filtration (RoBERTa)
                           Summarization engine (BART)

DATA FLOW
---------
  Student submits feedback via frontend form
        ↓
  Frontend calls backend API (FastAPI)
        ↓
  API passes text through noise filtration and normalization
        ↓
  RoBERTa classifies sentiment (Positive / Neutral / Negative)
        ↓
  BART generates comment summary
        ↓
  Results stored in MariaDB and returned to the frontend dashboard

CURRENT STATE (Frontend Branch)
--------------------------------
- All sentiment data and summaries are currently mock/dummy values
- The /submit_feedback endpoint returns a randomized mock sentiment label
- Real API integration will replace mock data after branch merge

SYSTEM REQUIREMENTS
-------------------
- Python 3.8 or higher
- Windows, macOS, or Linux
- Modern web browser (Chrome, Firefox, Edge)
- Minimum 100MB free disk space

================================================================================
DEVELOPMENT TEAM
================================================================================

Developed by the SENSE Team:

  Frontend Dashboard UI    — John Donald Eslabon, Paul Daniel Arindaeng
  Database & Backend API   — Jamie Rose Kia Reyes
  NLP Sentiment Analysis   — Juan Miguel Tan
  NLP Summarization        — Frinz Darrel Tupaz

PROJECT PURPOSE
---------------
This system was developed to address the practical challenge of processing
large volumes of unstructured student faculty evaluation comments. Traditional
manual review is time-consuming and prone to inconsistency. SENSE provides an
automated, web-based solution with noise filtration, sentiment analysis, and
intelligent summarization to support authorized academic administrators in
reviewing qualitative faculty feedback efficiently.

================================================================================
VERSION HISTORY
================================================================================

v1.0.0 (2026)
  - Initial release
  - Frontend dashboard with mock data
  - Welcome, Dashboard, Advisors, and Individual Faculty pages
  - Sentiment donut chart visualization
  - Anonymous feedback submission form
  - Noise audit log display
  - Admin login system (currently disabled for development)

FUTURE ENHANCEMENTS
-------------------
  - Full integration with RoBERTa sentiment model
  - Full integration with BART summarization model
  - Live database connection via Jamie's FastAPI backend
  - Admin registration and user management
  - Export feedback reports as PDF or CSV
  - Email notifications for new feedback submissions
  - Mobile-responsive improvements

================================================================================

Developed by the SENSE Team
© 2026 SENSE Team

This system was developed as part of CPE412 — Development of a Sentiment
Faculty Evaluation Analysis System for a Student Portal.

================================================================================
