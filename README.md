# 🐙 LangGraph Data Quality Copilot (Local LLM + DuckDB)

Imagine this.

You just got a CSV from “somewhere” (email, S3 export, vendor drop, quick extract).
You *know* it’s going to have duplicates, missing values, weird ranges…  
But you don’t want to spend your evening writing 20 validation queries.

So I built a copilot.

This project is a **local-first Data Quality agent** that:
1) loads a dataset into DuckDB  
2) profiles the data like a curious analyst  
3) asks a local LLM (Ollama) to propose quality rules  
4) validates those rules against the dataset  
5) produces a human-readable report you can share

No cloud keys needed. No paid APIs. Just **you + your laptop**.

---

## ✨ What it does

✅ **Profiles** a dataset (types, nulls, ranges, cardinality)  
✅ **Generates DQ rules** using an LLM (Ollama)  
✅ **Validates rules** inside DuckDB (fast SQL checks)  
✅ **Outputs a report** as Markdown (`outputs/report.md`)  
✅ Built as a **LangGraph workflow** (clear, modular, extensible)

---

## 🧠 Why LangGraph?

Because data engineering pipelines aren’t “one big script”.

They are **steps**, **state**, **guardrails**, and **retries**.

LangGraph makes that explicit:

`load → profile → propose_rules → validate → report`

Each step is a node.
The shared state moves through the graph.
Failures don’t crash everything — they get captured as structured errors.

---

## 🏗️ Architecture (High level)

- **DuckDB** = local analytics engine (no setup)
- **LangGraph** = orchestration / workflow graph
- **Ollama** = local LLM for rule generation
- **Markdown report** = simple output anyone can read

---

## 🚀 Quickstart

### 1) Start Ollama + pull a model
Install Ollama, then:

```bash
ollama pull qwen2.5:7b
