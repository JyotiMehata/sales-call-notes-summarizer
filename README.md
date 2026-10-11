# Sales Call Notes Summarizer

## Project Overview

The Sales Call Notes Summarizer is a Python-based NLP application that converts unstructured sales-call notes into concise summaries, key discussion points, action items, and next actions.

The application provides a simple Streamlit interface and saves processed CRM records to a CSV file.

## Features

- Accepts customer or prospect names and sales-call notes.
- Cleans text using Python regular expressions.
- Performs sentence and word tokenization using NLTK.
- Extracts key discussion points using keyword-based rules.
- Identifies action items from sales-call notes.
- Generates a concise summary.
- Identifies the next recommended action.
- Creates a structured CRM record.
- Saves CRM records to CSV storage.
- Provides a browser-based interface using Streamlit.

## Technology Stack

- **Language:** Python
- **NLP Library:** NLTK
- **Text Processing:** Regular Expressions (`re`)
- **Frontend:** Streamlit
- **Storage:** CSV
- **Development Environment:** Visual Studio Code

## Project Structure

```text
sales-call-notes-summarizer/
├── app.py
├── extractor.py
├── text_processor.py
├── storage.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `crm_records.csv` file is generated or updated when the application saves processed call records. It is not listed as a tracked project file because it may contain customer information.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd sales-call-notes-summarizer
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows Command Prompt:**

```bash
.venv\Scripts\activate
```

**PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Download NLTK tokenizer data if needed

If NLTK reports that tokenizer data is missing, run:

```bash
python -m nltk.downloader punkt punkt_tab
```

### 6. Run the application

```bash
streamlit run app.py
```

Streamlit will provide a local URL to open the application in your browser.

## How to Use

1. Open the application in your browser.
2. Enter the customer or prospect name.
3. Paste the sales-call notes into the text area.
4. Click **Process Call**.
5. Review the generated summary, key discussion points, action items, next action, and CRM status.
6. The processed CRM record is saved to `crm_records.csv`.

## Example Input

**Customer:** John Smith

**Sales Call Notes:**

> Customer is interested in the reporting feature. They asked about pricing and requested a product demo. Sales representative will send pricing information.

## Example Output

- **Key Discussion Points:** Reporting requirement, product feature discussion, customer interest, pricing discussion, product demo.
- **Action Items:** Schedule product demo, send pricing information.
- **Next Action:** Confirm demo date.
- **CRM Status:** Follow-up Required.

The generated summary and extracted actions depend on the wording of the input notes and the application's keyword-based rules.

## Current Limitations

- Uses rule-based extraction rather than a trained machine-learning model.
- May miss actions expressed in unfamiliar wording.
- Does not integrate directly with external CRM platforms.
- Does not process audio recordings or perform speech-to-text conversion.

## Future Enhancements

- Improve action extraction and summary quality.
- Add date and deadline identification.
- Add action-owner detection.
- Integrate with external CRM platforms.
- Explore LLM-based summarization.

## Author

Developed as a Python and Natural Language Processing project to simplify the processing of sales-call notes and CRM follow-up information.