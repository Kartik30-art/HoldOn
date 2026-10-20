# HoldOn - Your Digital Safety Assistant

**Pause. Check. Protect yourself.**

HoldOn is a web-based scam message checker that identifies common warning signs in SMS messages, WhatsApp messages, and other text. It combines transparent rule-based detection with an experimental machine-learning model and practical safety advice.

## Features

- **Scam detection:** Identifies suspicious urgency, prize claims, payment requests, requests for sensitive information, suspicious app installations, and links.
- **Risk assessment:** Classifies messages as low, medium, or high risk based on detected indicators.
- **Evidence:** Shows the phrases that triggered each warning.
- **Safety advice:** Suggests practical next steps based on the message.
- **Experimental ML classification:** Uses TF-IDF features and Logistic Regression to produce a separate prediction.
- **MCP integration:** Exposes scam detection and safety-advice tools through the Model Context Protocol.
- **Simple web interface:** Test sample messages or paste your own.

## Technology Stack

- Python
- FastAPI
- HTML, CSS, and JavaScript
- Model Context Protocol (MCP)
- scikit-learn
- TF-IDF and Logistic Regression
- Joblib

## Project Structure

```text
HoldOn_Clean/
â”œâ”€â”€ data/
â”‚   â””â”€â”€ messages.csv
â”œâ”€â”€ models/
â”‚   â””â”€â”€ holdon_text_model.joblib
â”œâ”€â”€ server/
â”‚   â”œâ”€â”€ __init__.py
â”‚   â”œâ”€â”€ engine.py
â”‚   â”œâ”€â”€ engine_backup.py
â”‚   â”œâ”€â”€ mcp_server.py
â”‚   â”œâ”€â”€ ml_engine.py
â”‚   â””â”€â”€ web_app.py
â”œâ”€â”€ static/
â”‚   â”œâ”€â”€ index.html
â”‚   â”œâ”€â”€ script.js
â”‚   â””â”€â”€ style.css
â”œâ”€â”€ tests/
â”‚   â”œâ”€â”€ check_mcp.py
â”‚   â”œâ”€â”€ test_engine.py
â”‚   â””â”€â”€ test_mcp_client.py
â”œâ”€â”€ train_model.py
â”œâ”€â”€ requirements.txt
â””â”€â”€ README.md
```

## Requirements

- Python 3.10 or a compatible version supported by the installed dependencies
- pip
- A Windows, macOS, or Linux terminal
- The packages listed in `requirements.txt`

## Installation

Clone or download the project, then open a terminal in the project directory.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Train the Experimental ML Model

Run:

```bash
python train_model.py
```

The model is saved to:

```text
models/holdon_text_model.joblib
```

A trained model file is already included in the project, so retraining is not required if that file is present and usable.

## Run HoldOn

Open **two terminals** in the project root and activate the virtual environment in each.

**Terminal 1 - Start the MCP server:**

```bash
python -m server.mcp_server
```

**Terminal 2 - Start the web application:**

```bash
python -m uvicorn server.web_app:app --reload --port 8001
```

Open this address in your browser:

http://127.0.0.1:8001

Keep both terminals running while using the website.

## Run Tests

Run the rule-based engine tests:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Check Python syntax:

```bash
python -m compileall server tests train_model.py
```

Check installed dependency consistency:

```bash
python -m pip check
```

Test the MCP tools:

```bash
python tests/check_mcp.py
```

The MCP server should be running for any tests that connect to its live endpoint.

## How It Works

1. The user submits a message through the website.
2. The FastAPI application sends it to the MCP scam-detection tool.
3. The rule-based engine looks for configured warning phrases and links.
4. The application retrieves practical safety advice.
5. The experimental ML model separately classifies the message.
6. The website displays the risk level, detected evidence, advice, and ML signal.

## Limitations and Responsible Use

- A warning is not proof that a message is fraudulent.
- No detected warning signs does not guarantee a message is safe.
- The current ML model was trained on only 20 sample messages. It is experimental and has not been validated on a representative real-world dataset.
- The model score is not calibrated and must not be presented as verified accuracy or the probability that a message is fraudulent.
- Rule-based checks may miss new scams or flag legitimate messages.
- Avoid submitting private information, passwords, OTPs, banking credentials, or other sensitive personal data to a demo.

For suspected cyber fraud in India, call **1930** or visit https://cybercrime.gov.in/.

## Future Improvements

- Expand and validate the dataset using diverse, appropriately sourced messages.
- Evaluate precision, recall, F1 score, and false-positive and false-negative rates on held-out data.
- Improve URL analysis and detection of impersonation attempts.
- Add multilingual message analysis.
- Improve accessibility and mobile usability.
- Add privacy-conscious reporting and evaluation features.

## Disclaimer

HoldOn is an educational and demonstration project. It does not guarantee scam detection, replace professional advice, or establish whether a message is safe or fraudulent.

