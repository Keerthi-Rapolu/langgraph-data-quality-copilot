from __future__ import annotations

from pathlib import Path
import duckdb


def load_csv_to_duckdb(
    dataset_path: str,
    table_name: str = "data",
    db_path: str = "outputs/dq.duckdb",
) -> tuple[str, str]:
    """
    Loads CSV into a DuckDB *file* (db_path) and returns (db_path, table_name).
    This avoids passing DuckDB connections through LangGraph state.
    """
    p = Path(dataset_path)
    if not p.is_absolute():
        p = (Path.cwd() / p).resolve()

    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {p}")

    db = Path(db_path)
    if not db.is_absolute():
        db = (Path.cwd() / db).resolve()
    db.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(database=str(db))
    # overwrite table each run to keep it deterministic
    con.execute(f"DROP TABLE IF EXISTS {table_name}")
    con.execute(
        f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto(?, HEADER=true);",
        [str(p)],
    )
    con.close()

    return str(db), table_name
