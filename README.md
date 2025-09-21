Here’s a focused **README.md** you can drop in your repo. It just explains how to get the app running.

---

# Contract Reviewer App

AI-powered contract analyzer that highlights risks, flags missing clauses, suggests edits, and summarizes in plain English.

---

## Setup

### 1. Clone & enter

```bash
git clone <your-repo-url>
cd contract-reviewer
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/` (copy from `.env.example`):

```
GROQ_API_KEY=your_real_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

Run the API server:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

The backend runs at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

### 3. Frontend

In another terminal:

```bash
cd frontend
python3 -m http.server 3001
```

Open [http://127.0.0.1:3001](http://127.0.0.1:3001) in your browser.

---

## Usage

* **Paste Text:** Enter contract text in the textarea → click **Analyze**.
* **Upload File:** Choose a PDF/DOCX/TXT → click **Analyze File**.
* Results show:

  * **Heuristic Flags** (quick keyword checks)
  * **Risks** (LLM findings)
  * **Missing/Unclear** checklist items
  * **Fix Suggestions**
  * **Plain-English Summary**

---

## Notes

* Requires a valid **Groq API Key**.
* Use `llama-3.3-70b-versatile` (previous `3.1` models are deprecated).
* Only extracts **selectable text**; scanned PDFs won’t work unless you add OCR.

---

Want me to also add quick **cURL test commands** so you can verify the backend without touching the frontend?
