from __future__ import annotations

import os
from dotenv import load_dotenv
import duckdb

from langgraph.graph import StateGraph, END
from src.state import DQState
from src.tools.duckdb_loader import load_csv_to_duckdb
from src.tools.profiler import profile_table
from src.tools.rules_llm import generate_rules_from_profile
from src.tools.validator import validate_rules
from src.tools.reporter import write_markdown_report

load_dotenv()


def build_graph():
    g = StateGraph(DQState)

    def load_data(state: DQState) -> DQState:
        try:
            dataset_path = state["dataset_path"]
            table_name = state.get("table_name", "data")
            db_path = state.get("db_path", "outputs/dq.duckdb")

            db_path, table_name = load_csv_to_duckdb(dataset_path, table_name, db_path)

            state["db_path"] = db_path
            state["table_name"] = table_name
            return state
        except Exception as e:
            state.setdefault("errors", []).append(f"load_data failed: {e}")
            return state

    def profile_data(state: DQState) -> DQState:
        if "db_path" not in state:
            state.setdefault("errors", []).append("profile_data failed: missing db_path (load_data did not succeed)")
            return state

        try:
            con = duckdb.connect(state["db_path"])
            state["profile"] = profile_table(con, state["table_name"])
            con.close()
            return state
        except Exception as e:
            state.setdefault("errors", []).append(f"profile_data failed: {e}")
            return state

    def generate_rules(state: DQState) -> DQState:
        if "profile" not in state:
            state.setdefault("errors", []).append("generate_rules failed: missing profile")
            return state

        try:
            model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            state["rules"] = generate_rules_from_profile(state["profile"], model)
            return state
        except Exception as e:
            state.setdefault("errors", []).append(f"generate_rules failed: {e}")
            return state

    def validate(state: DQState) -> DQState:
        if "db_path" not in state or "rules" not in state:
            state.setdefault("errors", []).append("validate failed: missing db_path or rules")
            return state

        try:
            con = duckdb.connect(state["db_path"])
            state["validation"] = validate_rules(con, state["table_name"], state["rules"])
            con.close()
            return state
        except Exception as e:
            state.setdefault("errors", []).append(f"validate failed: {e}")
            return state

    def report(state: DQState) -> DQState:
        try:
            out_path = state.get("report_path", "outputs/report.md")
            state["report_path"] = write_markdown_report(
                state.get("profile", {}),
                state.get("rules", []),
                state.get("validation", {}),
                out_path,
            )
            return state
        except Exception as e:
            state.setdefault("errors", []).append(f"report failed: {e}")
            return state

    g.add_node("load_data", load_data)
    g.add_node("profile_data", profile_data)
    g.add_node("generate_rules", generate_rules)
    g.add_node("validate", validate)
    g.add_node("report", report)

    g.set_entry_point("load_data")
    g.add_edge("load_data", "profile_data")
    g.add_edge("profile_data", "generate_rules")
    g.add_edge("generate_rules", "validate")
    g.add_edge("validate", "report")
    g.add_edge("report", END)

    return g.compile()
