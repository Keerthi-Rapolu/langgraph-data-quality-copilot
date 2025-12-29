# 🐙 LangGraph Data Quality Copilot

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Local LLM](https://img.shields.io/badge/LLM-local--first-orange)

A **local-first, agentic data quality system** built with **LangGraph**, **DuckDB**, and **local LLMs (Ollama)**.

This project automates data profiling, rule generation, validation, and reporting — without cloud dependencies.

---

## 🎯 What Problem This Solves

You receive CSV data from vendors, ad‑hoc exports, or internal teams.

You expect:
- missing values
- duplicates
- invalid ranges
- inconsistent formats

But writing and maintaining dozens of validation queries is slow and brittle.

This project replaces that manual work with an **agent-based data quality pipeline**.

---

## ✨ What It Does

✅ Profiles datasets automatically  
✅ Uses an LLM to propose quality rules  
✅ Validates rules against real data using DuckDB  
✅ Produces a human‑readable Markdown report  
✅ Runs fully **offline** on your laptop

---

## 🧠 Why LangGraph (Not Traditional Scripts)

Traditional approach:
- Hard‑coded SQL checks
- Manual updates per dataset
- No reasoning or explanation

LangGraph approach:
- Stateful workflow
- Clear node responsibilities
- Deterministic execution
- LLM reasoning only where needed

This makes the system **inspectable, extensible, and production‑shaped**.

---

## 🏗 Architecture Overview

The system is implemented as a **LangGraph state machine**:

1. **Ingest Node** – loads CSV into DuckDB
2. **Profile Node** – computes nulls, ranges, distincts
3. **Rule Generator Node** – LLM proposes validation rules
4. **Validation Node** – rules executed via SQL
5. **Report Node** – generates Markdown output

Each node updates a shared state object passed through the graph.

### Core Components

#### 1. Input CSV
- Raw dataset provided by a user or vendor  
- Example: `customer_data.csv`

#### 2. LangGraph Workflow
- Orchestrates each step as an explicit state
- Controls execution order and shared state
- Makes the pipeline deterministic and debuggable

#### 3. DuckDB
- Embedded analytical database
- Used for profiling and validation queries
- Fast, local, zero setup

#### 4. Local LLM (Ollama)
- Generates data quality rules from profiling statistics
- Runs fully offline
- No external API calls or credentials required

#### 5. Output Report
- Human-readable Markdown report
- Summarizes checks, failures, and observations  
- Example: `quality_report.md`

![Architecture Diagram](docs/architecture.png)

---

## 📂 Project Structure

```
langgraph-data-quality-copilot/
├── data/
│   └── sample.csv
├── src/
│   ├── graph.py
│   ├── state.py
│   ├── nodes/
│   │   ├── ingest.py
│   │   ├── profile.py
│   │   ├── generate_rules.py
│   │   ├── validate.py
│   │   └── report.py
│   └── main.py
├── outputs/
│   └── data_quality_report.md
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1️⃣ Prerequisites

- Python **3.10+**
- Ollama installed and running

Pull a local model:
```bash
ollama pull llama3.1
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the Copilot

```bash
python -m src.main --input data/sample.csv
```

---

## 📄 Example Output

Console:
```
✔ Dataset loaded into DuckDB
✔ Profiling completed
✔ 14 rules generated
✖ 3 rule failures detected
✔ Report saved to outputs/data_quality_report.md
```

Report excerpt:
```
Column: age
- Rule: age must be between 0 and 120
- Failures: 7 rows
- Suggested Fix: investigate negative values
```

---

## ⚙️ Configuration

Supported CLI options:

| Option | Description |
|------|------------|
| `--input` | Path to CSV file |
| `--model` | Ollama model name (default: llama3.1) |
| `--output` | Output report path |

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 🔒 Privacy & Security

- No data leaves your machine
- No API keys required
- Fully offline execution

---

## 🛠 Extending the System

You can easily add:
- New validation strategies
- Different report formats (HTML / JSON)
- Cloud warehouses (Snowflake / BigQuery)
- CI validation on pull requests

---

## 📜 License

MIT License. See `LICENSE` file for details.

---

## 🙌 Acknowledgements

- LangGraph
- DuckDB
- Ollama

---

## ⭐ When This Is Useful

✔ Vendor data validation  
✔ One‑off CSV audits  
✔ Data engineering demos  
✔ Learning agentic workflows  

---

If you want this adapted for **Snowflake**, **Databricks**, or **CI pipelines**, the architecture already supports it.

