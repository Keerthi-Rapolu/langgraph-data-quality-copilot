from __future__ import annotations
import duckdb


def validate_rules(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
    rules: list[dict],
) -> dict:
    """
    Applies data quality rules to a DuckDB table.
    """
    results = []

    for rule in rules:
        rtype = rule.get("type")
        column = rule.get("column")

        if not rtype or not column:
            continue

        if rtype == "not_null":
            count = con.execute(
                f"SELECT COUNT(*) FROM {table_name} WHERE {column} IS NULL"
            ).fetchone()[0]
            results.append(
                {
                    "rule": rule["name"],
                    "status": "FAIL" if count > 0 else "PASS",
                    "violations": count,
                }
            )

        elif rtype == "unique":
            dupes = con.execute(
                f"""
                SELECT COUNT(*) FROM (
                    SELECT {column}, COUNT(*) c
                    FROM {table_name}
                    GROUP BY {column}
                    HAVING c > 1
                )
                """
            ).fetchone()[0]
            results.append(
                {
                    "rule": rule["name"],
                    "status": "FAIL" if dupes > 0 else "PASS",
                    "violations": dupes,
                }
            )

        elif rtype == "range":
            min_v = rule.get("min")
            max_v = rule.get("max")

            if min_v is None or max_v is None:
                continue

            count = con.execute(
                f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE {column} < ? OR {column} > ?
                """,
                [min_v, max_v],
            ).fetchone()[0]

            results.append(
                {
                    "rule": rule["name"],
                    "status": "FAIL" if count > 0 else "PASS",
                    "violations": count,
                }
            )

        elif rtype == "allowed_values":
            allowed = rule.get("allowed")
            if not allowed:
                continue

            placeholders = ",".join("?" for _ in allowed)
            count = con.execute(
                f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE {column} NOT IN ({placeholders})
                """,
                allowed,
            ).fetchone()[0]

            results.append(
                {
                    "rule": rule["name"],
                    "status": "FAIL" if count > 0 else "PASS",
                    "violations": count,
                }
            )

    return {
        "total_rules": len(results),
        "failed_rules": sum(1 for r in results if r["status"] == "FAIL"),
        "details": results,
    }
