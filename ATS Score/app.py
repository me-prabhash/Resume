# Run: streamlit run ".\ATS Score\app.py"

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from modules.parser import parse_resume
from modules.rules_engine import calculate_score
from modules.jd_matcher import extract_jd_keywords, match_keywords, score_jd_match
from modules.cortex_feedback import get_ai_feedback, CORTEX_AVAILABLE

st.set_page_config(page_title="ATS Score Checker", page_icon="📄", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    .score-big {
        font-size: 64px;
        font-weight: 700;
        text-align: center;
        line-height: 1.1;
    }
    .score-label {
        font-size: 16px;
        text-align: center;
        color: #888;
    }
    .matched-kw {
        display: inline-block;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 12px;
        font-size: 13px;
        background: #d4edda;
        color: #155724;
    }
    .missing-kw {
        display: inline-block;
        padding: 4px 10px;
        margin: 3px;
        border-radius: 12px;
        font-size: 13px;
        background: #f8d7da;
        color: #721c24;
    }
    .category-pass { color: #28a745; }
    .category-warn { color: #ffc107; }
    .category-fail { color: #dc3545; }
</style>
""", unsafe_allow_html=True)

st.title("ATS Score Checker")
st.markdown("Upload your resume and paste a job description to see how well they match.")

# --- Input section ---
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader(
        "Upload Resume (PDF, HTML, or TXT)",
        type=['pdf', 'html', 'htm', 'txt'],
    )

with col2:
    jd_text = st.text_area(
        "Paste Job Description",
        height=200,
        placeholder="Paste the full job description here...",
    )

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    parsed, error = parse_resume(file_bytes, uploaded_file.name)

    if error:
        st.error(f"Could not parse resume: {error}")
    elif parsed:
        # Rule-based score
        score_result = calculate_score(parsed)
        total = score_result['total_score']
        max_total = score_result['max_score']

        # JD match (if provided)
        jd_match = None
        jd_score = 0
        jd_max = 20
        if jd_text.strip():
            jd_keywords, skill_keywords = extract_jd_keywords(jd_text)
            jd_match = match_keywords(parsed['full_text'], jd_keywords)
            jd_score, jd_max = score_jd_match(jd_match)

        # Combined score
        combined_max = max_total + jd_max
        combined_score = total + jd_score
        combined_pct = round(combined_score / combined_max * 100) if combined_max > 0 else 0

        # --- Score display ---
        st.markdown("---")

        c1, c2, c3 = st.columns(3)

        with c1:
            color = "#28a745" if combined_pct >= 75 else "#ffc107" if combined_pct >= 50 else "#dc3545"
            st.markdown(f'<div class="score-big" style="color:{color}">{combined_pct}</div>', unsafe_allow_html=True)
            st.markdown('<div class="score-label">Overall ATS Score</div>', unsafe_allow_html=True)

        with c2:
            rule_pct = round(total / max_total * 100) if max_total > 0 else 0
            color2 = "#28a745" if rule_pct >= 75 else "#ffc107" if rule_pct >= 50 else "#dc3545"
            st.markdown(f'<div class="score-big" style="color:{color2}">{total}<span style="font-size:24px;color:#888">/{max_total}</span></div>', unsafe_allow_html=True)
            st.markdown('<div class="score-label">Resume Quality Score</div>', unsafe_allow_html=True)

        with c3:
            if jd_match:
                mpct = jd_match['match_percentage']
                color3 = "#28a745" if mpct >= 70 else "#ffc107" if mpct >= 40 else "#dc3545"
                st.markdown(f'<div class="score-big" style="color:{color3}">{mpct}%</div>', unsafe_allow_html=True)
                st.markdown('<div class="score-label">JD Keyword Match</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="score-big" style="color:#888">--</div>', unsafe_allow_html=True)
                st.markdown('<div class="score-label">Paste JD to see match</div>', unsafe_allow_html=True)

        # --- Category breakdown ---
        st.markdown("---")
        st.subheader("Score Breakdown")

        for cat_name, cat_data in score_result['categories'].items():
            s = cat_data['score']
            m = cat_data['max']
            pct = s / m if m > 0 else 0

            if pct >= 0.8:
                icon = "✅"
            elif pct >= 0.5:
                icon = "⚠️"
            else:
                icon = "❌"

            with st.expander(f"{icon} {cat_name}: {s}/{m}"):
                st.progress(pct)
                for detail_text, passed in cat_data['details']:
                    if passed:
                        st.markdown(f"✓ {detail_text}")
                    else:
                        st.markdown(f"✗ {detail_text}")

        # JD match as a category
        if jd_match:
            jd_pct = jd_score / jd_max if jd_max > 0 else 0
            jd_icon = "✅" if jd_pct >= 0.8 else "⚠️" if jd_pct >= 0.5 else "❌"
            with st.expander(f"{jd_icon} Keyword Match: {jd_score}/{jd_max}"):
                st.progress(jd_pct)
                st.markdown(f"**{len(jd_match['matched'])}** keywords matched, **{len(jd_match['missing'])}** missing out of **{jd_match['total_keywords']}** total")

        # --- Keyword chips ---
        if jd_match:
            st.markdown("---")
            st.subheader("Keyword Analysis")

            if jd_match['matched']:
                st.markdown("**Matched Keywords:**")
                chips = ''.join(f'<span class="matched-kw">{kw}</span>' for kw in jd_match['matched'])
                st.markdown(chips, unsafe_allow_html=True)

            if jd_match['missing']:
                st.markdown("**Missing Keywords:**")
                chips = ''.join(f'<span class="missing-kw">{kw}</span>' for kw in jd_match['missing'])
                st.markdown(chips, unsafe_allow_html=True)

        # --- AI Feedback ---
        st.markdown("---")
        st.subheader("AI Recommendations")

        if not CORTEX_AVAILABLE:
            st.info("Snowflake Cortex is not available. Install `snowflake-snowpark-python` and add credentials to `.streamlit/secrets.toml` to enable AI-powered feedback.")
        elif not jd_text.strip():
            st.info("Paste a job description above to get AI-powered recommendations.")
        else:
            if st.button("Get AI Feedback", type="primary"):
                with st.spinner("Analyzing with Snowflake Cortex..."):
                    missing_kws = jd_match['missing'] if jd_match else []
                    match_p = jd_match['match_percentage'] if jd_match else 0
                    feedback, fb_error = get_ai_feedback(
                        parsed['full_text'],
                        jd_text,
                        combined_pct,
                        match_p,
                        missing_kws,
                    )
                    if fb_error:
                        st.warning(fb_error)
                    elif feedback:
                        st.markdown(feedback)

        # --- Debug info ---
        with st.expander("Debug: Parsed Resume Data"):
            st.json({
                'word_count': parsed['word_count'],
                'sections_found': list(parsed['sections_found'].keys()),
                'bullet_count': len(parsed['bullets']),
                'metrics_count': parsed['metrics_count'],
                'contact': parsed['contact'],
                'verb_analysis': parsed['verb_analysis'],
            })
