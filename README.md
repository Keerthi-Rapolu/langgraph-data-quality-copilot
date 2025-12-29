# 🐙 LangGraph Data Quality Copilot (Local LLM + DuckDB)

AI-assisted Data Quality Workflow using DuckDB, LangGraph, and a local LLM (Ollama)
Automated dataset profiling, rule generation, validation, and reporting.

Imagine this:
You receive a dataset — maybe a vendor file, a client CSV, or a quick export from S3.
You suspect there will be missing values, duplicates, inconsistent ranges, and other quality issues.

Instead of manually writing dozens of validation scripts, this project automates the process by:
- Profiling a dataset
- Letting an AI suggest quality rules
- Validating the data using those rules
- Producing a clear report

---

## 🏗️ Architecture 

## Core Components

### 1. Input CSV
- Raw dataset provided by a user or vendor  
- Example: `customer_data.csv`

### 2. LangGraph Workflow
- Orchestrates each processing step as a state  
- Ensures predictable, step-by-step execution

### 3. DuckDB
- Local analytical database  
- Used for data profiling and validation

### 4. Local LLM (Ollama)
- Generates data quality rules from dataset statistics  
- No external API calls required

### 5. Output Report
- Markdown file summarizing data quality issues  
- Example: `report.md`

- **DuckDB** – local analytics engine (no setup)
- **LangGraph** – orchestration / workflow graph
- **Ollama** – local LLM for rule generation
- **Markdown report** – simple output anyone can read
  
---

## ✨ What it does

✅ **Profiles** a dataset (types, nulls, ranges, cardinality)  
✅ **Generates DQ rules** using an LLM (Ollama)  
✅ **Validates rules** inside DuckDB (fast SQL checks)  
✅ **Outputs a report** as Markdown (`outputs/report.md`)  
✅ Built as a **LangGraph workflow** (clear, modular, extensible)

---

## 🧠 Why LangGraph?

This workflow is not a single script. It is a sequence of steps with shared state.
LangGraph makes the pipeline explicit:
`load → profile → propose_rules → validate → report`
Each step is a node, state flows through the graph, and errors are captured instead of crashing the run.

---

## 📂 Input & Output
**📥 Input**: 
examples/sample_data.csv

**📤 Output**: 
outputs/report.md

---

## 🚀 Why this approach
- Rule discovery is automated
- Runs fully offline
- Easy to extend or replace components
- Useful for exploration, validation, and learning

---

## 🚫 Non-goals
- Not a production data quality platform
- Not distributed or real-time
- Not multi-user
