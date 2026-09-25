import re
from sklearn.feature_extraction.text import TfidfVectorizer

TECH_SKILLS = {
    'snowflake', 'dbt', 'python', 'sql', 'azure', 'aws', 'gcp', 'spark',
    'airflow', 'kafka', 'databricks', 'redshift', 'bigquery', 'terraform',
    'docker', 'kubernetes', 'git', 'jenkins', 'ci/cd', 'cicd',
    'power bi', 'tableau', 'looker', 'excel',
    'java', 'scala', 'go', 'rust', 'javascript', 'typescript', 'node',
    'react', 'angular', 'vue', 'django', 'flask', 'fastapi',
    'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
    'etl', 'elt', 'data warehouse', 'data lake', 'data mesh',
    'data vault', 'dimensional modeling', 'star schema',
    'medallion', 'scd', 'incremental', 'micro-batching',
    'rbac', 'rls', 'row-level security', 'data masking',
    'data governance', 'data quality', 'data lineage',
    'machine learning', 'ml', 'deep learning', 'nlp',
    'agile', 'scrum', 'jira', 'confluence',
    'azure data factory', 'adf', 'azure devops',
    'snowpipe', 'streams', 'tasks', 'stored procedures',
    'power automate', 'powerapps', 'logic apps',
    'sap', 'sap bw', 'sap hana', 'dax', 'm query',
}


def extract_jd_keywords(jd_text):
    jd_lower = jd_text.lower()

    # extract tech skills mentioned in JD
    skill_matches = set()
    for skill in TECH_SKILLS:
        if skill in jd_lower:
            skill_matches.add(skill)

    # TF-IDF to find important non-skill terms
    try:
        vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=50,
            min_df=1,
        )
        tfidf = vectorizer.fit_transform([jd_text])
        feature_names = vectorizer.get_feature_names_out()
        scores = tfidf.toarray()[0]
        top_indices = scores.argsort()[-30:][::-1]
        tfidf_keywords = set()
        for i in top_indices:
            if scores[i] > 0:
                term = feature_names[i].lower()
                if len(term) > 2 and not term.isdigit():
                    tfidf_keywords.add(term)
    except Exception:
        tfidf_keywords = set()

    all_keywords = skill_matches | tfidf_keywords
    return all_keywords, skill_matches


def match_keywords(resume_text, jd_keywords):
    resume_lower = resume_text.lower()
    matched = set()
    missing = set()

    for kw in jd_keywords:
        if kw in resume_lower:
            matched.add(kw)
        else:
            missing.add(kw)

    total = len(jd_keywords)
    match_pct = (len(matched) / total * 100) if total > 0 else 0

    return {
        'match_percentage': round(match_pct, 1),
        'matched': sorted(matched),
        'missing': sorted(missing),
        'total_keywords': total,
    }


def score_jd_match(match_result):
    pct = match_result['match_percentage']
    if pct >= 80:
        score = 20
    elif pct >= 60:
        score = 16
    elif pct >= 40:
        score = 12
    elif pct >= 20:
        score = 8
    else:
        score = 4
    return score, 20
