---
name: resume-updater
description: "Resume Updater - Update and format Prabhash Thakur's resume into a styled HTML document. Use when: user wants to update their resume, reformat resume content, generate a resume HTML, or apply resume template. Triggers: update resume, format resume, resume update, new resume, resume HTML, apply resume template, generate resume, resume updater."
---

# Resume Updater

Generate a professionally styled HTML resume from user-provided content, matching the established template format.

## Setup

**Load** `assets/template.html` to understand the exact HTML structure, CSS styling, and section layout.

## Template Structure

The resume uses a **single-column, ATS-optimized layout**. Section order is fixed:

```
+-----------------------------------------------+
| HEADER (left-aligned, white bg)                |
|   Name (Raleway 26pt, bold)                    |
|   Role (navy accent)                           |
|   Phone | Email | LinkedIn  (plain text)       |
|   ===== navy rule =====                        |
+-----------------------------------------------+
| SUMMARY        (full width paragraph)          |
| SKILLS         (bold label: comma-sep text)    |
| EXPERIENCE     (role left / dates right,       |
|                 company below, then bullets)   |
| CERTIFICATIONS (bulleted, linked)              |
| EDUCATION      (degree - school | year | score) |
| RECOGNITION    (bulleted)                      |
| LANGUAGES      (one comma-separated line)      |
+-----------------------------------------------+
```

**Design tokens:**
- Accent: `#16325c` (dark navy) -- used only on section rules, role subtitle, company names, bullet glyphs
- Text dark: `#111111`, medium: `#2b2b2b`, light: `#5a5a5a`
- Fonts: Raleway (name + section titles), Open Sans (body)
- Section headings: uppercase, letter-spacing 1.5px, thin bottom border
- Page: A4, 12mm margins on print
- No background fills, no column splits, no emoji, no skill chips/badges

## ATS Constraints (do not violate)

These rules exist because ATS parsers extract text by visual reading order. Breaking them silently destroys keyword matching:

1. **Single column only.** Never reintroduce `display: flex` or `display: grid` side-by-side content regions. Two columns cause parsers to interleave job titles with unrelated text.
2. **Skills as comma-separated plain text**, never one `<span>`/`<div>` per skill. Chips extract as `SnowflakedbtSQLPython` with no delimiters, making each skill unfindable.
3. **No emoji or icon characters in text nodes** (no `📞`, `✉`, `🔗`, `📅`, `◆`). They corrupt adjacent phone/email tokens. Use CSS `::before` glyphs if a bullet marker is needed.
4. **Summary first**, directly under contact, full width. It is the highest-value skim target.
5. **Standard section names** -- Summary, Skills, Experience, Certifications, Education. Do not rename to creative alternatives.
6. **No tables, text boxes, or absolutely positioned content** for layout.

## Tone Rules (avoid AI-sounding copy)

Bullets must read as written by a working engineer, not generated.

- **Banned verbs:** Spearheading, Pioneering, Revolutionized, Championing, Leveraged, Orchestrated, Engineered (as a filler verb), Architected (unless genuinely architecture work), Boosting, Empowering, Driving.
- **Use instead:** Led, Built, Set up, Wrote, Cut, Moved, Fixed, Ran, Rebuilt, Added, Owned, Handled, Tracked down.
- **Banned phrases:** "higher-value analysis", "reclaimed engineering bandwidth", "tribal knowledge", "ramp-up", "best-in-class", "cutting-edge", "seamlessly", "robust", "end-to-end" (as filler), "enterprise-grade".
- **No `--` em-dash strings** as connectors. Use a full stop and a new sentence.
- **Consistent voice.** Third-person implied subject throughout ("Led a team of 8"), not a mix of "I" and fragments.
- **No keyword-stuffed openers** like "Data Engineering Lead | Snowflake | dbt | Data Mesh". Write a real sentence.
- Keep concrete numbers (60%, 1TB daily, 50K+ records). Those are the strongest signal and are never the problem.

## Workflow

### Step 1: Receive Updated Content

The user will provide updated resume content either by:
- **Attaching a file** (docx, pdf, txt, or other format)
- **Pasting text** directly in the chat
- **Describing changes** to specific sections of the existing resume

**Actions:**
1. **Read** the attached file or parse the provided text to extract resume content
2. **Identify** the following sections:
   - Contact info (phone, email, LinkedIn)
   - Summary
   - Skills, grouped into categories
   - Work experience (role, company, dates, bullet points)
   - Certifications (name, issuer, credential URL)
   - Education (degree, school, location, year, score/GPA)
   - Recognition / awards
   - Languages
3. If the user provides partial updates (e.g., "add this new job" or "update my skills"), **read** the existing resume at `Resume/Prabhash_Thakur_Resume.html` and merge the changes

If any section is ambiguous or missing, ask the user for clarification.

### Step 1b: Auto-Calculate Experience

The user's career started in **March 2018**. Always calculate total years of experience dynamically:
- Compute: (current year and month) minus (March 2018)
- Round down to whole years and express as "X+ Years"
- Use this value in the Profile section text (e.g., "8+ Years" if current date is Sep 2026)

### Step 2: Generate HTML

**Actions:**
1. **Load** `assets/template.html` for the exact HTML structure and CSS
2. **Generate** a new HTML file by populating the template structure with the extracted content:
   - Keep all CSS exactly as-is from the template
   - Preserve the single-column flow and section order
   - Skills go in `<p class="skills-row">` with a bold `<span class="skills-label">Category:</span>` followed by comma-separated plain text
   - Certifications use `<div class="cert-item">` with the name as a link, then ` - Issuer`
   - Experience uses `<div class="exp-header">` (role left, dates right), `<div class="exp-company">`, then a flat `<ul>`
   - Wrap genuinely important terms in `<strong>` for human skim -- this is ATS-neutral and helps
3. **Check** every bullet against the Tone Rules above and reword anything that trips them
4. **Write** the HTML file to `Resume/Prabhash_Thakur_Resume.html`

**Rules:**
- Do NOT change fonts, colors, spacing, or CSS from the template
- Do NOT add or remove CSS classes
- Do NOT reintroduce a two-column layout, sidebar, skill chips, or emoji (see ATS Constraints)
- Experience header uses flex layout: role left, dates right
- Company name goes below the header in the navy accent
- Section titles use Raleway, uppercase, letter-spacing 1.5px, thin bottom border
- Print styles must be preserved for PDF export
- Length is not capped -- keep the detail. Prioritize accurate, plainly worded bullets over hitting a page count

### Step 3: Present and Confirm

**Actions:**
1. Tell the user the file has been written
2. Mention they can open it in a browser and print to PDF (Ctrl+P, save as PDF)
3. Ask if any adjustments are needed

**STOP**: Wait for user confirmation or revision requests.

### Step 4: Iterate (if needed)

If the user requests changes:
1. **Read** the current HTML file
2. **Apply** the requested modifications
3. **Write** the updated file
4. Return to Step 3

## Stopping Points

- After Step 1 if content is ambiguous or sections are missing
- After Step 3 for user review

## Output

A single HTML file at `Resume/Prabhash_Thakur_Resume.html` matching the template design, ready to print to PDF.

## Optional: Score the result

The repo has a local ATS checker at `ATS Score/app.py` (Streamlit). To verify a change improved the score, run:

```
streamlit run "ATS Score/app.py"
```

Then upload the exported PDF and paste a target job description.
