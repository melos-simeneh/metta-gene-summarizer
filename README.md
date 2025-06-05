# Gene Data Summarization with Metta using Gemini

This project provides a workflow for extracting, summarizing, and formatting gene data using Metta knowledge base expressions, integrated with Gemini-based AI summarization. It saves enriched gene knowledge in Metta and exports human-readable summaries for easy review.

## Features

- Extract structured gene data from Metta facts.
- Summarize gene information using Google Gemini AI.
- Format gene data into clear, readable text blocks.
- Save summaries to text files and Metta knowledge spaces.
- Integrated Metta operations for easy invocation.

## Requirements

- Python 3.8+
- hyperon Python library for Metta integration
- Google Gemini API key (set GENAI_API_KEY in .env)

## Setup

### 1. Clone the repository:

```bash
git clone https://github.com/melos-simeneh/metta-gene-summarizer.git
cd metta-gene-summarizer
```

### 2. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up environment variables:

Create a .env file in the root directory and add your Gemini API key:

```env
GENAI_API_KEY=your_api_key_here
```

### 4. Run the Metta workflow

```bash
metta main.metta
```

## Alternative: Run with Docker

If you're unable to install `hyperon` locally, you can use Docker:

```bash
docker compose build  gene-image-builder
docker comose up -d
```
