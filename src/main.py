from __future__ import annotations
import argparse
from rich import print

from src.graph import build_graph

def run(dataset_path: str, out_path: str):
    app = build_graph()
    final_state = app.invoke(
        {
            "dataset_path": dataset_path,
            "table_name": "data",
            "report_path": out_path
        }
    )

    print("[bold green]Done.[/bold green]")
    if final_state.get("errors"):
        print("[bold yellow]Errors:[/bold yellow]")
        for e in final_state["errors"]:
            print("-", e)

    print("Report:", final_state.get("report_path"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="examples/sample_data.csv")
    parser.add_argument("--out", default="outputs/report.md")
    args = parser.parse_args()
    run(args.dataset, args.out)

if __name__ == "__main__":
    main()
