import os
import re
import argparse
from datetime import datetime
import PyPDF2
import pandas as pd

# Branding and report configuration
REPORT_FILE = "PII_Report.txt"
BRAND_HEADER = """
=== PII-Hunter ===
Scan Date: {date}
Target PII Types: {types}
"""

# Regex patterns with validation
CC_PATTERN = r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9]{2})[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11})\b'
EMAIL_PATTERN = r'\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b'
PHONE_PATTERN = r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})\b'

def luhn_check(card_num):
    """Validate credit card using Luhn algorithm"""
    digits = list(map(int, str(card_num)))
    odd_sum = sum(digits[-1::-2])
    even_sum = sum([sum(divmod(2*d, 10)) for d in digits[-2::-2]])
    return (odd_sum + even_sum) % 10 == 0

def scan_text(content, pattern, validator=None):
    matches = []
    for match in re.finditer(pattern, content):
        if not validator or validator(match.group()):
            matches.append({
                'value': match.group(),
                'pos': match.start(),
                'line': content.count('\n', 0, match.start()) + 1
            })
    return matches

def process_pdf(file_path, patterns):
    matches = []
    try:
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page_num, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                for ptype, pattern in patterns.items():
                    found = scan_text(text, pattern['regex'], pattern['validator'])
                    matches.extend([(ptype, m) for m in found])
    except Exception as e:
        pass
    return matches

def process_sheet(file_path, patterns):
    matches = []
    try:
        df = pd.read_excel(file_path)
        for idx, row in df.iterrows():
            for cell in row:
                for ptype, pattern in patterns.items():
                    found = scan_text(str(cell), pattern['regex'], pattern['validator'])
                    matches.extend([(ptype, m) for m in found])
    except:
        pass
    return matches

def scan_file(file_path, selected_types):
    patterns = {}
    if '1' in selected_types:
        patterns['CreditCard'] = {'regex': CC_PATTERN, 'validator': luhn_check}
    if '2' in selected_types:
        patterns['Email'] = {'regex': EMAIL_PATTERN, 'validator': None}
    if '3' in selected_types:
        patterns['Phone'] = {'regex': PHONE_PATTERN, 'validator': None}

    ext = os.path.splitext(file_path)[1].lower()
    matches = []

    try:
        if ext == '.pdf':
            return process_pdf(file_path, patterns)
        elif ext in ('.xls', '.xlsx'):
            return process_sheet(file_path, patterns)
        else:  # Text-based files
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for ptype, pattern in patterns.items():
                    found = scan_text(content, pattern['regex'], pattern['validator'])
                    matches.extend([(ptype, m) for m in found])
    except:
        pass
    return matches

def generate_report(findings):
    report = []
    for file_path, pii_data in findings.items():
        report.append(f"\nFile: {file_path}")
        for ptype, details in pii_data.items():
            report.append(f"  {ptype} found:")
            for detail in details:
                report.append(f"    Line {detail['line']}: {detail['value']}")
    return '\n'.join(report)

def main():
    parser = argparse.ArgumentParser(description='PII-Hunter: Data Discovery Tool')
    parser.add_argument('-t', '--types', required=True, 
        help='Comma-separated PII types: 1=CC, 2=Email, 3=Phone')
    parser.add_argument('-p', '--path', default='.', help='Root directory to scan')
    
    args = parser.parse_args()
    selected_types = args.types.split(',')
    
    findings = {}
    for root, _, files in os.walk(args.path):
        for file in files:
            file_path = os.path.join(root, file)
            file_matches = scan_file(file_path, selected_types)
            
            if file_matches:
                findings[file_path] = {}
                for ptype, match in file_matches:
                    if ptype not in findings[file_path]:
                        findings[file_path][ptype] = []
                    findings[file_path][ptype].append(match)

    # Generate report
    report_content = BRAND_HEADER.format(
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        types=", ".join(selected_types)
    )
    report_content += generate_report(findings)
    
    with open(REPORT_FILE, 'w') as f:
        f.write(report_content)

if __name__ == "__main__":
    main()
