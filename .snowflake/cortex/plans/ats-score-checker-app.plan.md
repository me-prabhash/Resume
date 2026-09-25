# Plan: ATS Score Checker App

## Overview
A local Streamlit app that lets you upload a resume (PDF or HTML), paste a job description, and get:
1. A **rule-based ATS score** (0-100) with section-by-section breakdown
2. A **keyword match score** against the JD
3. **AI-powered recommendations** from Snowflake Cortex for improvements

## Architecture

```
ATS Score/
  app.py                  # Streamlit entry point + UI
  requirements.txt        # Dependencies
  modules/
    parser.py             # Resume text extraction (PDF + HTML)
    rules_engine.py       # Rule-based ATS scoring
    jd_matcher.py         # Job description keyword matching
    cortex_feedback.py    # Snowflake Cortex AI feedback
```

## Scoring Logic (Rule-Based, 100 points)

| Category | Points | What it checks |
|---|---|---|
| Contact Info | 15 | Email found, phone found, LinkedIn found |
| Section Headings | 15 | Has standard headings: Summary, Experience, Skills, Education, Certifications |
| Measurable Impact | 15 | Count of numbers/percentages/dollar amounts in experience bullets |
| Action Verbs | 10 | Variety of leading verbs (not repeating same verb), strong vs weak verbs |
| Keyword Match | 20 | % of JD keywords found in resume |
| Formatting | 10 | No tables/columns detected, no images, parseable text structure |
| Length & Structure | 10 | Reasonable length, bullet points used, not walls of text |
| ATS Readability | 5 | Standard fonts, no headers/footers that confuse parsers |

## JD Matching
- Extract nouns, skills, and phrases from pasted job description using basic NLP (TF-IDF or keyword extraction)
- Compare against resume text
- Show: match %, matched keywords (green), missing keywords (red)

## Cortex AI Feedback
- Sends resume text + JD to `snowflake.cortex.Complete('llama3.1-70b', prompt)`
- Prompt asks for: top 3 strengths, top 5 specific improvements, suggested rewordings for weak bullets
- Displayed in an expandable panel below the score

## UI Layout
```
+------------------------------------------+
|  ATS Score Checker                       |
+------------------------------------------+
| [Upload Resume]  [Paste Job Description] |
+------------------------------------------+
| Overall Score: 82/100    JD Match: 74%   |
|  [===========================---]        |
+------------------------------------------+
| Section Breakdown:                       |
|  Contact Info:    15/15  ✓               |
|  Section Headings: 12/15                 |
|  Measurable Impact: 10/15               |
|  Action Verbs:     8/10                  |
|  Keyword Match:   14/20                  |
|  Formatting:      10/10  ✓              |
|  Structure:        8/10                  |
|  ATS Readability:  5/5   ✓             |
+------------------------------------------+
| Missing Keywords: [chip] [chip] [chip]   |
+------------------------------------------+
| AI Recommendations:                      |
|  1. Your summary should lead with...     |
|  2. Add metrics to Tech Mahindra...      |
|  3. Consider rewording bullet X to...    |
+------------------------------------------+
```

## Dependencies
- `streamlit` - UI
- `pdfplumber` - PDF text extraction
- `beautifulsoup4` - HTML parsing
- `snowflake-snowpark-python` - Cortex AI connection
- `scikit-learn` - TF-IDF for keyword extraction

## Steps

### 1. Set up project structure
Create the folder layout, `app.py`, `requirements.txt`, and module files.

### 2. Build resume parser
- PDF: use `pdfplumber` to extract text page by page
- HTML: use `BeautifulSoup` to strip tags and get clean text
- Section detection: regex for common headings (Experience, Skills, Education, Summary, etc.)
- Return structured dict: `{sections: {...}, full_text: str, bullets: [...], metrics_count: int}`

### 3. Build rule-based scoring engine
- Each category is a function returning `(score, max_score, details)`
- Contact check: regex for email, phone patterns, linkedin URL
- Section check: match against standard ATS heading names
- Metrics check: count numbers, percentages, dollar signs in bullet text
- Verb check: extract first word of each bullet, check variety and strength
- Format check: detect table/column patterns, image references
- Structure check: bullet count, text-to-bullet ratio, resume length

### 4. Build JD matcher
- TF-IDF vectorizer on JD text to extract top keywords
- Also extract explicit skill names (Snowflake, Python, dbt, etc.) via a curated tech skills list
- Compare against resume full text
- Return match %, matched list, missing list

### 5. Add Cortex AI feedback
- Connect via Snowpark session
- Send a structured prompt with resume text + JD + current score breakdown
- Parse the response into actionable items
- Fallback: if no Snowflake connection, skip AI section gracefully

### 6. Build Streamlit UI
- Two-column top: file uploader (left), JD text area (right)
- Score gauge using `st.metric` or custom progress bars
- Section breakdown as a table with color coding
- Missing keywords as colored chips
- AI recommendations in an expander

### 7. Test with your resume
- Load Prabhash_Thakur_Resume.html
- Paste a sample Senior Data Engineer JD
- Verify scores make sense, tweak weights if needed
