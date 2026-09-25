import re
import logging
from bs4 import BeautifulSoup

logging.getLogger('pdfminer').setLevel(logging.ERROR)

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

SECTION_PATTERNS = [
    (r'\b(professional\s+summary|summary|profile|objective|about\s+me)\b', 'summary'),
    (r'\b(work\s+experience|experience|employment\s+history|work\s+history)\b', 'experience'),
    (r'\b(skills|technical\s+skills|core\s+competencies|competencies)\b', 'skills'),
    (r'\b(education|academic|qualifications)\b', 'education'),
    (r'\b(certifications?|certificates?|licenses?)\b', 'certifications'),
    (r'\b(projects?|project\s+achievements?)\b', 'projects'),
    (r'\b(recognition|awards?|achievements?|honors?)\b', 'recognition'),
    (r'\b(languages?)\b', 'languages'),
    (r'\b(contact|contact\s+info|contact\s+information)\b', 'contact'),
]

STRONG_VERBS = {
    'led', 'managed', 'built', 'designed', 'developed', 'implemented', 'created',
    'delivered', 'architected', 'reduced', 'increased', 'automated', 'optimized',
    'established', 'launched', 'drove', 'spearheaded', 'owned', 'scaled',
    'migrated', 'configured', 'deployed', 'integrated', 'streamlined',
    'trained', 'mentored', 'coordinated', 'negotiated', 'resolved',
    'introduced', 'rewrote', 'refactored', 'maintained', 'oversaw',
    'authored', 'wrote', 'defined', 'set', 'ran', 'handled',
    'investigated', 'prototyped', 'engineered', 'constructed',
    'running', 'leading', 'got', 'switched', 'made', 'took',
    'put', 'do', 'brought', 'solved', 'fixed', 'cut',
    'redesigned', 'consolidated', 'simplified', 'standardized',
}

WEAK_VERBS = {
    'worked', 'helped', 'assisted', 'participated', 'involved',
    'responsible', 'tasked', 'utilized', 'leveraged',
}


def parse_pdf(file_bytes):
    import io
    text = ''

    # Try pdfplumber first
    if pdfplumber is not None:
        try:
            text_parts = []
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text_parts.append(t)
            text = '\n'.join(text_parts)
        except Exception:
            pass

    # If pdfplumber got nothing, try PyMuPDF
    if not text.strip():
        try:
            import pymupdf
            doc = pymupdf.open(stream=file_bytes, filetype="pdf")
            parts = []
            for page in doc:
                t = page.get_text()
                if t:
                    parts.append(t)
            text = '\n'.join(parts)
            doc.close()
        except ImportError:
            pass
        except Exception:
            pass

    # If still nothing, the PDF has no extractable text (vector/image based)
    if not text.strip():
        return None

    return text


def parse_html(file_bytes):
    html = file_bytes.decode('utf-8', errors='replace')
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup(['style', 'script', 'svg', 'meta', 'link']):
        tag.decompose()
    return soup.get_text(separator='\n', strip=True)


def extract_text(file_bytes, filename):
    ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    if ext == 'pdf':
        text = parse_pdf(file_bytes)
        if text is None:
            return None, "Could not extract text from this PDF. Your PDF was likely generated with Chrome/Edge print-to-PDF using web fonts, which embeds text as vector shapes instead of real characters. Fix: open the HTML resume in your browser, press Ctrl+P, and under 'More settings' make sure 'Background graphics' is checked. Alternatively, upload the HTML file directly -- it parses much more reliably."
        return text, None
    elif ext in ('html', 'htm'):
        return parse_html(file_bytes), None
    elif ext == 'txt':
        return file_bytes.decode('utf-8', errors='replace'), None
    else:
        return None, f"Unsupported file type: .{ext}"


def detect_sections(text):
    lines = text.split('\n')
    found = {}
    for line in lines:
        clean = line.strip().lower()
        if len(clean) < 3 or len(clean) > 60:
            continue
        for pattern, name in SECTION_PATTERNS:
            if re.search(pattern, clean, re.IGNORECASE):
                if name not in found:
                    found[name] = True
                break
    return found


def extract_bullets(text):
    bullets = []
    for line in text.split('\n'):
        line = line.strip()
        # remove common bullet markers
        cleaned = re.sub(r'^[\u2022\u25CF\u25CB\u25AA\u25C6\u2023\-\*\>]+\s*', '', line)
        if cleaned and len(cleaned) > 30 and len(cleaned) < 500:
            if any(c.isalpha() for c in cleaned):
                # filter out section headings, short labels, skill items
                word_count = len(cleaned.split())
                if word_count >= 6:
                    bullets.append(cleaned)
    return bullets


def count_metrics(text):
    patterns = [
        r'\d+\s*%',
        r'\$\s*\d+',
        r'\d+\s*\+',
        r'\d+x\b',
        r'\b\d{2,}\b',
    ]
    count = 0
    for p in patterns:
        count += len(re.findall(p, text, re.IGNORECASE))
    return count


def extract_contact_info(text):
    email = bool(re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', text))
    phone = bool(re.search(r'[\+]?\d[\d\s\-\(\)]{7,}\d', text))
    linkedin = bool(re.search(r'linkedin\.com', text, re.IGNORECASE))
    return {'email': email, 'phone': phone, 'linkedin': linkedin}


def classify_bullets(bullets):
    strong = 0
    weak = 0
    verbs_used = set()
    for b in bullets:
        words = b.strip().split()
        if not words:
            continue
        first_word = words[0].lower().rstrip('.,;:')
        # try first two words if first is a short word like "I" or "This"
        check_words = [first_word]
        if len(words) > 1 and first_word in ('i', 'also', 'the', 'this', 'that', 'my', 'our', 'we'):
            check_words.append(words[1].lower().rstrip('.,;:'))

        matched_strong = False
        matched_weak = False
        for w in check_words:
            # check exact match
            if w in STRONG_VERBS:
                matched_strong = True
                verbs_used.add(w)
                break
            # check common past tense: managed -> manage, built -> built
            stem = re.sub(r'(ed|ing|s)$', '', w)
            if stem in STRONG_VERBS:
                matched_strong = True
                verbs_used.add(stem)
                break
            if w in WEAK_VERBS or stem in WEAK_VERBS:
                matched_weak = True
                verbs_used.add(w)
                break

        if matched_strong:
            strong += 1
        elif matched_weak:
            weak += 1
    return {
        'strong_count': strong,
        'weak_count': weak,
        'unique_verbs': len(verbs_used),
        'total_bullets': len(bullets),
    }


def parse_resume(file_bytes, filename):
    text, error = extract_text(file_bytes, filename)
    if error:
        return None, error

    sections = detect_sections(text)
    bullets = extract_bullets(text)
    metrics_count = count_metrics(text)
    contact = extract_contact_info(text)
    verb_analysis = classify_bullets(bullets)

    return {
        'full_text': text,
        'sections_found': sections,
        'bullets': bullets,
        'metrics_count': metrics_count,
        'contact': contact,
        'verb_analysis': verb_analysis,
        'word_count': len(text.split()),
    }, None
