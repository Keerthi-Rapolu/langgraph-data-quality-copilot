from __future__ import annotations
import duckdb

def profile_table(con: duckdb.DuckDBPyConnection, table_name: str) -> dict:
    """
    Basic profiling:
    - row count
    - per-column null count
    - distinct count
    - numeric min/max/avg (when possible)
    """
    # row count
    row_count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]

    # get columns
    cols = con.execute(f"DESCRIBE {table_name}").fetchall()
    # DESCRIBE returns: (column_name, column_type, null, key, default, extra)
    col_info = [{"name": c[0], "type": c[1]} for c in cols]

    per_col = {}
    for c in col_info:
        name = c["name"]
        # nulls
        nulls = con.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {name} IS NULL").fetchone()[0]
        distincts = con.execute(f"SELECT COUNT(DISTINCT {name}) FROM {table_name}").fetchone()[0]

        stats = {"type": c["type"], "nulls": int(nulls), "distinct": int(distincts)}

        # numeric stats attempt
        try:
            min_v, max_v, avg_v = con.execute(
                f"SELECT MIN({name}), MAX({name}), AVG({name}) FROM {table_name}"
            ).fetchone()
            # avg might fail on non-numeric, so this is inside try
            stats.update({"min": min_v, "max": max_v, "avg": avg_v})
        except Exception:
            pass

        per_col[name] = stats

    return {"row_count": int(row_count), "columns": per_col}
