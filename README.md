# SENSE — Sentiment Faculty Evaluation Analysis System
**Student Portal** | Version 1.0.0 | Python 3.8+

> Development of a Sentiment Faculty Evaluation Analysis System for a Student Portal — CPE412

---

## About

SENSE is a web-based Student Portal that processes and analyzes open-ended student feedback submitted through an integrated interface. The system addresses the problem of unstructured faculty evaluation comments that may contain informal language, Taglish, abbreviations, and meaningless inputs such as random keystrokes and numerical gibberish.

The system performs three core NLP functions:

1. **Noise Filtration & Text Normalization** — detects and discards invalid inputs before processing, then normalizes informal, code-mixed, and Taglish text into machine-readable format
2. **Sentiment Analysis** — classifies each meaningful comment as Positive, Neutral, or Negative using a fine-tuned RoBERTa model
3. **Automatic Summarization** — generates concise summaries of recurring feedback using a BART model, along with a quantitative report of filtered noise entries

---

## How to Use the System

### 1. Welcome Page
- Displays the system tagline and project description
- Click **"Enter dashboard"** to access the portal
- No login required for students submitting feedback

### 2. Dashboard
- Displays an overview of evaluation activity across the department
- Shows three summary statistics:
  - **Total Feedback** — total number of submitted student comments
  - **Advisors** — total number of faculty listed in the system
  - **Noise Filtered** — total number of invalid inputs automatically removed
- **Latest Comments** section shows recently submitted feedback with sentiment tags
- **Noise Audit Log** shows automatically filtered responses with their reason (e.g., random characters, keyboard pattern, numbers only)

### 3. Advisors / Faculty Directory
- Lists all CpE faculty members in a searchable grid
- Each card shows the faculty member's name, role, and avatar initials
- Use the search bar to filter faculty by name
- Click any card to view the individual faculty profile

### 4. Individual Faculty Page
- Displays the faculty member's profile information
- **Sentiment Overview** shows the Positive / Neutral / Negative percentage breakdown with a visual progress bar
- **Sentiment Distribution** shows a donut chart visualization
- **Comment Summary** displays an AI-generated summary of recurring feedback (noise entries excluded)
- **Share Your Feedback** form allows students to submit anonymous comments — sentiment is analyzed automatically
- **Recent Feedback** section lists the latest comments with sentiment labels

---

## Key Features

- **Anonymous Feedback Submission** — students submit comments without logging in
- **Noise Filtration** — automatically detects and discards gibberish, random keystrokes, numerical-only inputs, and placeholder values
- **Text Normalization** — processes Taglish, informal language, abbreviations, and student slang into machine-readable format
- **Sentiment Classification** — classifies feedback as Positive, Neutral, or Negative using RoBERTa
- **Automatic Summarization** — generates concise summaries of recurring student opinions using BART
- **Noise Audit Log** — quantitative report of filtered invalid inputs
- **Faculty Directory** — searchable grid of all CpE faculty members
- **Sentiment Visualization** — donut chart and percentage breakdown per faculty
- **Admin Login** — dashboard access restricted to authorized personnel
- **Responsive UI** — works across desktop and tablet screen sizes

---

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- XAMPP (for MariaDB database — handled by the backend team)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/jeydiislabon/SENSE-UI-test.git

# 2. Switch to the frontend branch
git checkout feature/frontend-ui

# 3. Navigate to the project folder
cd sense-ui

# 4. Install dependencies
python -m pip install -r requirements.txt

# 5. Run the application
python app.py

# 6. Open your browser at http://127.0.0.1:5000
```

> **Windows note:** If `python` is not recognized, use the full path:
> ```
> C:\Users\<your-username>\AppData\Local\Programs\Python\Python312\python.exe app.py
> ```

> **Share with groupmates on the same Wi-Fi:**
> ```
> python -c "from app import app; app.run(host='0.0.0.0', port=5000, debug=True)"
> ```
> Then share your local IP (e.g., `http://192.168.x.x:5000`)

---

## Pages & Routes

| Route | Page | Access |
|---|---|---|
| `/` | Welcome Page | Public |
| `/login` | Admin Login | Public |
| `/logout` | Logout | Public |
| `/dashboard` | Overview Dashboard | Protected |
| `/advisors` | Faculty Directory | Protected |
| `/faculty/<id>` | Individual Faculty Profile | Protected |
| `/submit_feedback/<id>` | Feedback Submission Endpoint | Public |

---

## Technical Information

### Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.x | Core programming language |
| Flask 3.0.3 | Web framework and routing |
| Jinja2 | HTML templating |
| HTML / CSS / JS | Frontend interface |
| Chart.js | Sentiment donut chart (CDN) |
| MariaDB | Database via XAMPP |
| FastAPI | Backend API for NLP integration |
| RoBERTa | Sentiment classification model |
| BART | Automatic summarization model |

### Branch Structure

| Branch | Responsibility |
|---|---|
| `feature/frontend-ui` | Frontend dashboard UI |
| `feature/backend-db` | Database schema and API routing |
| `feature/nlp-training` | Sentiment analysis, noise filtration, summarization |

### Data Flow

```
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
```

> **Current state (this branch):** All sentiment data and summaries use mock/dummy values. The `/submit_feedback` endpoint returns a randomized mock label. Real API integration will replace mock data after branch merge.

### System Requirements
- Python 3.8 or higher
- Windows, macOS, or Linux
- Modern web browser (Chrome, Firefox, Edge)
- Minimum 100MB free disk space

---

## Development Team

| Name | Role |
|---|---|
| John Donald Eslabon | Frontend Developer |
| Paul Daniel Arindaeng | UI Designer |
| Jamie Rose Kia Reyes | Database & Backend API |
| Juan Miguel Tan | NLP Sentiment Analysis |
| Frinz Darrel Tupaz | NLP Summarization |

---

## Version History

**v1.0.0 (2026)**
- Initial release
- Frontend dashboard with mock data
- Welcome, Dashboard, Advisors, and Individual Faculty pages
- Sentiment donut chart visualization
- Anonymous feedback submission form
- Noise audit log display
- Admin login system (currently disabled for development)

### Future Enhancements
- Full integration with RoBERTa sentiment model
- Full integration with BART summarization model
- Live database connection via FastAPI backend
- Admin registration and user management
- Export feedback reports as PDF or CSV
- Email notifications for new feedback submissions
- Mobile-responsive improvements

---

*CPE412 — Development of a Sentiment Faculty Evaluation Analysis System for a Student Portal*
*© 2026 SENSE Team*
