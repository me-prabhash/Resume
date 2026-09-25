import streamlit as st

try:
    from snowflake.snowpark import Session
    import snowflake.cortex as cortex
    CORTEX_AVAILABLE = True
except ImportError:
    CORTEX_AVAILABLE = False


def get_snowflake_session():
    if not CORTEX_AVAILABLE:
        return None
    try:
        session = Session.builder.configs({
            "account": st.secrets.get("snowflake", {}).get("account", ""),
            "user": st.secrets.get("snowflake", {}).get("user", ""),
            "password": st.secrets.get("snowflake", {}).get("password", ""),
            "role": st.secrets.get("snowflake", {}).get("role", ""),
            "warehouse": st.secrets.get("snowflake", {}).get("warehouse", ""),
        }).create()
        return session
    except Exception:
        return None


FEEDBACK_PROMPT = """You are an expert ATS resume reviewer. Analyze this resume against the job description and give specific, actionable feedback.

RESUME TEXT:
{resume_text}

JOB DESCRIPTION:
{jd_text}

CURRENT ATS SCORE: {score}/100
KEYWORD MATCH: {match_pct}%
MISSING KEYWORDS: {missing_keywords}

Give your feedback in exactly this format:

STRENGTHS:
1. [specific strength]
2. [specific strength]
3. [specific strength]

IMPROVEMENTS:
1. [specific improvement with example rewrite if applicable]
2. [specific improvement with example rewrite if applicable]
3. [specific improvement with example rewrite if applicable]
4. [specific improvement with example rewrite if applicable]
5. [specific improvement with example rewrite if applicable]

PRIORITY KEYWORDS TO ADD:
List the top 5 missing keywords that would have the biggest impact, and suggest where in the resume to add them naturally.

Keep your language direct and practical. No filler."""


def get_ai_feedback(resume_text, jd_text, score, match_pct, missing_keywords):
    if not CORTEX_AVAILABLE:
        return None, "Snowflake Cortex not available. Install snowflake-snowpark-python to enable AI feedback."

    session = get_snowflake_session()
    if session is None:
        return None, "Could not connect to Snowflake. Check your credentials in .streamlit/secrets.toml"

    prompt = FEEDBACK_PROMPT.format(
        resume_text=resume_text[:4000],
        jd_text=jd_text[:2000],
        score=score,
        match_pct=match_pct,
        missing_keywords=', '.join(missing_keywords[:15]),
    )

    try:
        response = cortex.Complete('llama3.1-70b', prompt, session=session)
        return response, None
    except Exception as e:
        return None, f"Cortex API error: {str(e)}"
