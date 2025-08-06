import pandas as pd
import re
from collections import defaultdict

def normalize_name(raw_name: str) -> str:
    """
    Replace any token that contains a digit, '*' or '/' with '***',
    preserving the other tokens (in their original case).

    Example:
      "Hardcoded AWS Keys detected for AKI**************THC at organization's private repository cns-test-github/test-secret-scan"
      → "Hardcoded AWS Keys detected for *** at organization's private repository ***"
    """
    tokens = raw_name.split()
    normalized_tokens = []
    for tok in tokens:
        # If token has a digit, or an asterisk, or a slash, treat it as "unique" → replace
        if re.search(r'[0-9]', tok) or '*' in tok or '/' in tok:
            normalized_tokens.append("***")
        else:
            normalized_tokens.append(tok)
    return " ".join(normalized_tokens).strip()

def parse_csv(file_path):
    """
    Reads the CSV at `file_path`, filters for 'critical' and 'high' severities,
    and returns two dicts (critical_counts, high_counts). Each dict maps the
    fully‐normalized misconfiguration name (with unique tokens replaced by '***')
    to the number of rows in that severity. Duplicates are counted multiple times.
    """
    df = pd.read_csv(file_path)

    # Normalize 'Severity' to lowercase for filtering, but do NOT alter case of names
    df['Severity'] = df['Severity'].str.lower()

    critical_counts = defaultdict(int)
    high_counts     = defaultdict(int)

    for sev in ('critical', 'high'):
        sub_df = df[df['Severity'] == sev]

        for _, row in sub_df.iterrows():
            raw_name = str(row.get('Misconfiguration Name', "")).strip()
            if not raw_name:
                continue

            key = normalize_name(raw_name)
            if not key:
                # If normalization yields an empty string (unlikely), skip
                continue

            if sev == 'critical':
                critical_counts[key] += 1
            else:  # sev == 'high'
                high_counts[key] += 1

    return dict(critical_counts), dict(high_counts)
