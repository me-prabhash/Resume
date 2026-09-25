REQUIRED_SECTIONS = ['summary', 'experience', 'skills', 'education']
NICE_SECTIONS = ['certifications', 'projects', 'recognition', 'languages']


def score_contact(contact):
    score = 0
    details = []
    if contact['email']:
        score += 5
        details.append(('Email', True))
    else:
        details.append(('Email', False))
    if contact['phone']:
        score += 5
        details.append(('Phone', True))
    else:
        details.append(('Phone', False))
    if contact['linkedin']:
        score += 5
        details.append(('LinkedIn', True))
    else:
        details.append(('LinkedIn', False))
    return score, 15, details


def score_sections(sections_found):
    score = 0
    details = []
    for s in REQUIRED_SECTIONS:
        if s in sections_found:
            score += 3
            details.append((s.title(), True))
        else:
            details.append((s.title(), False))
    for s in NICE_SECTIONS:
        if s in sections_found:
            score += 0.75
            details.append((s.title(), True))
    return min(score, 15), 15, details


def score_metrics(metrics_count, bullet_count):
    if bullet_count == 0:
        return 0, 15, [('No bullets found', False)]
    ratio = metrics_count / max(bullet_count, 1)
    if ratio >= 0.5:
        score = 15
    elif ratio >= 0.3:
        score = 12
    elif ratio >= 0.2:
        score = 9
    elif ratio >= 0.1:
        score = 6
    else:
        score = 3
    details = [
        (f'{metrics_count} numbers/metrics found in {bullet_count} bullets', ratio >= 0.3),
        (f'Ratio: {ratio:.0%} of bullets have metrics', ratio >= 0.3),
    ]
    return score, 15, details


def score_verbs(verb_analysis):
    score = 0
    details = []
    total = verb_analysis['total_bullets']
    if total == 0:
        return 0, 10, [('No bullets to analyze', False)]

    strong_ratio = verb_analysis['strong_count'] / total
    if strong_ratio >= 0.6:
        score += 5
        details.append((f'{verb_analysis["strong_count"]}/{total} bullets start with strong verbs', True))
    elif strong_ratio >= 0.3:
        score += 3
        details.append((f'{verb_analysis["strong_count"]}/{total} bullets start with strong verbs', False))
    else:
        score += 1
        details.append((f'Only {verb_analysis["strong_count"]}/{total} bullets use strong verbs', False))

    if verb_analysis['weak_count'] > 0:
        details.append((f'{verb_analysis["weak_count"]} bullets use weak verbs (worked, helped, assisted)', False))

    unique = verb_analysis['unique_verbs']
    if unique >= 10:
        score += 5
        details.append((f'{unique} unique leading verbs -- good variety', True))
    elif unique >= 6:
        score += 3
        details.append((f'{unique} unique leading verbs -- decent variety', True))
    else:
        score += 1
        details.append((f'Only {unique} unique leading verbs -- try more variety', False))

    return min(score, 10), 10, details


def score_formatting(full_text):
    score = 10
    details = []

    if len(full_text) < 200:
        score -= 5
        details.append(('Resume text is very short -- may not be parsing correctly', False))

    table_patterns = ['|---|', '+---+', '+-+-+']
    has_tables = any(p in full_text for p in table_patterns)
    if has_tables:
        score -= 3
        details.append(('Table-like formatting detected -- may confuse ATS parsers', False))

    if not details:
        details.append(('No formatting issues detected', True))

    return max(score, 0), 10, details


def score_structure(word_count, bullet_count):
    score = 0
    details = []

    if 300 <= word_count <= 1200:
        score += 5
        details.append((f'{word_count} words -- good length', True))
    elif 200 <= word_count < 300:
        score += 3
        details.append((f'{word_count} words -- a bit short', False))
    elif 1200 < word_count <= 1800:
        score += 3
        details.append((f'{word_count} words -- slightly long', False))
    else:
        score += 1
        details.append((f'{word_count} words -- {"too short" if word_count < 200 else "too long"}', False))

    if bullet_count >= 15:
        score += 5
        details.append((f'{bullet_count} bullet points -- well structured', True))
    elif bullet_count >= 8:
        score += 3
        details.append((f'{bullet_count} bullet points -- could use more', False))
    else:
        score += 1
        details.append((f'Only {bullet_count} bullet points -- add more detail', False))

    return min(score, 10), 10, details


def score_readability(full_text):
    score = 5
    details = []

    long_sentences = 0
    for line in full_text.split('\n'):
        if len(line.split()) > 40:
            long_sentences += 1
    if long_sentences > 5:
        score -= 2
        details.append((f'{long_sentences} very long lines -- consider breaking them up', False))

    if not details:
        details.append(('Text readability looks good', True))

    return max(score, 0), 5, details


def calculate_score(parsed_resume):
    results = {}

    s, m, d = score_contact(parsed_resume['contact'])
    results['Contact Info'] = {'score': s, 'max': m, 'details': d}

    s, m, d = score_sections(parsed_resume['sections_found'])
    results['Section Headings'] = {'score': s, 'max': m, 'details': d}

    s, m, d = score_metrics(parsed_resume['metrics_count'], len(parsed_resume['bullets']))
    results['Measurable Impact'] = {'score': s, 'max': m, 'details': d}

    s, m, d = score_verbs(parsed_resume['verb_analysis'])
    results['Action Verbs'] = {'score': s, 'max': m, 'details': d}

    s, m, d = score_formatting(parsed_resume['full_text'])
    results['Formatting'] = {'score': s, 'max': m, 'details': d}

    s, m, d = score_structure(parsed_resume['word_count'], len(parsed_resume['bullets']))
    results['Length & Structure'] = {'score': s, 'max': m, 'details': d}

    s, m, d = score_readability(parsed_resume['full_text'])
    results['ATS Readability'] = {'score': s, 'max': m, 'details': d}

    total = sum(r['score'] for r in results.values())
    max_total = sum(r['max'] for r in results.values())

    return {
        'total_score': round(total),
        'max_score': max_total,
        'categories': results,
    }
