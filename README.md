# PII-Hunter   
**A Command-Line Tool for Scanning Files and Folders for Sensitive PII Data**

---

## Overview

**PII-Hunter ** is a Python-based command-line utility designed to help you discover sensitive Personally Identifiable Information (PII) such as credit card numbers, email addresses, and phone numbers within files and folders on your machine.  
It recursively scans directories, processes common file types (including PDFs, Excel files, CSVs, and text files), and generates a branded report listing all detected PII.

---

## Features

- **Recursive Directory Scanning:** Scans all files within a specified directory and its subdirectories.
- **Multiple PII Types:** Detects Credit Card numbers (with Luhn validation), Email addresses, and Phone numbers.
- **File Type Support:** Works with PDF, Excel (.xls, .xlsx), CSV, and plain text files.
- **Flexible Search:** Choose which PII types to scan for via command-line options.
- **Branded Reporting:** Outputs results to a text file with custom branding ("PII-Hunter ").
- **Extensible:** Easily add new PII types or file handlers.

---

## Requirements

- Python 3.x
    - [PyPDF2](https://pypi.org/project/PyPDF2/)
    - [pandas](https://pandas.pydata.org/)

Install dependencies with: pip install {{Module_Name}}
---

## Usage

### 1. Command-Line Arguments

| Argument | Description                                                                 |
|----------|-----------------------------------------------------------------------------|
| `-t`/`--types` | **Required.** Comma-separated PII types: `1`=Credit Card, `2`=Email, `3`=Phone |
| `-p`/`--path`  | **Optional.** Directory path to scan (default: current directory)           |

### 2. Example Commands

Scan for credit card numbers only in current directory:
    `python pii_hunter.py -t 1`

Scan for emails and phones in /home/user/docs:
    `python pii_hunter.py -t 2,3 -p /home/user/docs`

Full system scan for all PII types:
    `python pii_hunter.py -t 1,2,3 -p /`



### 3. Output

- Results saved to `PII_Report.txt`
- Report includes:
  - Scan date and selected PII types
  - File paths containing PII
  - Type of PII found
  - Location details (line number, value)

---

## Extending the Tool

To add new PII types or file handlers:
1. Edit the `scan_file` function
2. Add new regex patterns and validation functions

---

## Disclaimer

❗ **Important:**  
- Use only for authorized security/compliance purposes
- Obtain proper permissions before scanning files/directories

---

## Limitations

It currently doesn't support all the file types like DOC/DOCX, HTML/HTM

---



**Author:** Surya Teja Koka (Vibe Coding 😉) \
**Happy Hunting!** 🕵️
