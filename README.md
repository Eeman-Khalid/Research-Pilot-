# 🔎 ResearchPilot

## AI-Powered Autonomous Research Agent

ResearchPilot is an AI-powered autonomous research agent that researches a user-provided topic by generating research questions, searching the web, collecting source content, analyzing multiple sources, and producing a structured research report with references.

Unlike a simple chatbot that generates an answer from a single prompt, ResearchPilot follows a multi-stage research workflow that combines **LLM reasoning, web search, webpage extraction, source analysis, and report generation**.

---

## ✨ Features

* 🧠 Automatically generates research questions
* 🌐 Searches the web for relevant sources
* 📄 Extracts content from webpages
* 🔄 Uses search snippets as a fallback when webpages cannot be accessed
* 📊 Analyzes information from multiple sources
* 🔎 Provides source-based citations during analysis
* 📝 Generates structured research reports
* 📚 Includes references and source URLs
* 📈 Provides research pipeline statistics
* ⚠️ Handles API, search, and source-fetching failures
* 🖥️ Interactive Streamlit interface
* 📥 Allows users to download generated reports
* 🐳 Dockerized for reproducible deployment

---

## 🧠 How ResearchPilot Works

```text
User enters research topic
            ↓
Generate research questions
            ↓
Search the web
            ↓
Collect search results
            ↓
Fetch webpage content
            ↓
Fallback to snippets if necessary
            ↓
Analyze multiple sources
            ↓
Generate structured research report
            ↓
Display report + references
            ↓
Download report
```

---

## 🏗️ Architecture

```text
                ┌──────────────────────┐
                │     User Topic       │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Research Question    │
                │ Generation           │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │    Web Search        │
                │       DDGS           │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Webpage Extraction   │
                │ Requests + BS4       │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Source Analysis      │
                │ Gemini LLM            │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Report Generation    │
                │ Gemini LLM            │
                └──────────┬───────────┘
                           ↓
                ┌──────────────────────┐
                │ Streamlit Interface  │
                └──────────────────────┘
```

---

## 🛠️ Tech Stack

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Core programming language       |
| Google Gemini API | LLM reasoning and generation    |
| `google-genai`    | Gemini API integration          |
| DDGS              | Web search                      |
| Requests          | Webpage retrieval               |
| BeautifulSoup     | HTML content extraction         |
| Streamlit         | Web interface                   |
| python-dotenv     | Environment variable management |
| Docker            | Containerization                |
| Git & GitHub      | Version control                 |

---

## 📁 Project Structure

```text
research-pilot/
│
├── app/
│   ├── research_agent.py
│   ├── streamlit_app.py
│   └── evaluation.py
│
├── notebooks/
│
├── tests/
│
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/Eeman-Khalid/Research-Pilot-.git
```

Move into the project directory:

```bash
cd Research-Pilot-
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

Or in Windows Command Prompt:

```cmd
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 API Key Setup

ResearchPilot uses the **Google Gemini API**.

Create a Gemini API key through Google AI Studio.

Then create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

### Important

Never commit your `.env` file to GitHub.

The project `.gitignore` already excludes environment files.

---

# ▶️ Running ResearchPilot Locally

From the **project root**:

```bash
streamlit run app/streamlit_app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser.

---

# 🧪 Testing the Research Agent

The backend pipeline can also be tested without the Streamlit interface.

From the project root:

```bash
python test_agent.py
```

The test runs the complete research pipeline:

```text
Topic
 ↓
Research Questions
 ↓
Web Search
 ↓
Source Extraction
 ↓
Source Analysis
 ↓
Final Report
 ↓
Pipeline Evaluation
```

The evaluation checks:

* Whether a topic was provided
* Number of questions generated
* Number of research questions searched
* Number of sources found
* Number of analyses completed
* Whether the final report was generated
* Overall pipeline success

---

# 🐳 Running with Docker

Docker is supported for containerized execution.

## 1. Build the Docker Image

From the project root:

```bash
docker build -t researchpilot .
```

---

## 2. Run the Container

The application requires the Gemini API key.

Make sure your `.env` file exists in the project root.

Then run:

```bash
docker run --rm -p 8501:8501 --env-file .env researchpilot
```

Open:

```text
http://localhost:8501
```

The ResearchPilot Streamlit application should now be running inside the Docker container.

---

# 🔬 Example

Example research topic:

```text
Impact of Remote Work on Employee Productivity
```

ResearchPilot will automatically:

1. Generate research questions
2. Search the web
3. Collect relevant sources
4. Extract webpage content
5. Analyze the collected information
6. Generate a structured research report
7. Display references
8. Allow the report to be downloaded

ResearchPilot is **domain-independent**, so it can be used for topics across areas such as:

* Technology
* Healthcare
* Education
* Business
* Environment
* Psychology
* Economics
* History
* Energy
* Social sciences

---

# 📊 Evaluation

ResearchPilot includes a basic pipeline evaluation module.

Example evaluation output:

```text
============================================================
RESEARCHPILOT EVALUATION
============================================================
Topic provided: ✓
Questions generated: 5
Research questions searched: 5
Total sources found: 15
Analyses completed: 5
Report generated: ✓
------------------------------------------------------------
Overall pipeline: SUCCESS ✓
============================================================
```

This provides visibility into the different stages of the autonomous research workflow.

---

# ⚠️ Error Handling

ResearchPilot includes handling for common runtime problems such as:

* Gemini API failures
* Temporary server errors
* Web search failures
* Webpage access restrictions
* Missing webpage content
* Empty search results
* Failed source analysis
* Failed report generation

When a webpage cannot be accessed directly, the system can fall back to the search result snippet instead of immediately stopping the entire research process.

---

# 🔐 Environment Variables

The application currently requires:

```text
GEMINI_API_KEY
```

Example:

```text
GEMINI_API_KEY=your_api_key_here
```

Do not expose API keys in source code or commit them to GitHub.

---

# 📌 Current Status

ResearchPilot currently supports:

* Autonomous research question generation
* Web search
* Webpage content extraction
* Multi-source analysis
* Structured report generation
* Source references
* Research pipeline evaluation
* Streamlit interface
* Docker deployment

---

# 🔮 Future Improvements

Potential future improvements include:

* Improved source quality filtering
* More advanced citation verification
* Better topic/typo handling
* PDF and DOCX report export
* Research history
* More detailed evaluation metrics
* Advanced source credibility analysis
* Cloud deployment
* Persistent research storage

---

# 👩‍💻 Author

**Eeman Khalid**

BS Artificial Intelligence

GitHub:

```text
https://github.com/Eeman-Khalid
```

---

## 📄 License

This project is intended for educational, portfolio, and research purposes.
