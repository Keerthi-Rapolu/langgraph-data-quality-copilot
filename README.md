# 🐙 LangGraph Data Quality Copilot (Local LLM + DuckDB)

You get a CSV from somewhere — an email, a vendor export, a quick pull.
You expect missing values, duplicates, and odd ranges.

Instead of writing manual validation queries, this project lets the data describe its own quality rules.

This is a local-first data quality workflow that profiles a dataset, generates validation rules using a local LLM, runs checks in DuckDB, and produces a readable report.

No cloud setup. No paid APIs.

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

## 🏗️ Architecture (High level)

- **DuckDB** – local analytics engine (no setup)
- **LangGraph** – orchestration / workflow graph
- **Ollama** – local LLM for rule generation
- **Markdown report** – simple output anyone can read

---

## 📂 Input & Output
**📥 Input**
examples/sample_data.csv

**📤 Output**
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
