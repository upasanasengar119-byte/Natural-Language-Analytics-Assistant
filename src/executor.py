"""Compile validated plans into parameterized read-only SQL templates."""
import csv
import sqlite3
from pathlib import Path

from .planner import plan_question, validate_plan


def load_sales(csv_path: Path) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def compile_sql(plan: dict) -> tuple[str, tuple]:
    params = (plan["region"],) if plan["region"] else ()
    where = " WHERE region=?" if params else ""
    if plan["metric"] == "by_region":
        sql = (
            "SELECT region, SUM(amount) AS value FROM sales"
            + where
            + " GROUP BY region ORDER BY region"
        )
    elif plan["metric"] == "total":
        sql = "SELECT COALESCE(SUM(amount), 0) AS value FROM sales" + where
    else:
        sql = "SELECT COUNT(*) AS value FROM sales" + where
    return sql, params


def answer_question(question: str, csv_path: Path, backend: str = "local") -> dict:
    plan = validate_plan(plan_question(question))
    sql, params = compile_sql(plan)
    rows_data = load_sales(csv_path)
    connection = sqlite3.connect(":memory:")
    try:
        connection.execute(
            "CREATE TABLE sales (id TEXT, region TEXT, amount INTEGER)"
        )
        connection.executemany(
            "INSERT INTO sales VALUES (?, ?, ?)",
            [(r["order_id"], r["region"], int(r["amount_paise"])) for r in rows_data],
        )
        connection.commit()
        connection.execute("PRAGMA query_only=ON")
        rows = connection.execute(sql, params).fetchall()
    finally:
        connection.close()
    unit = "orders" if plan["metric"] == "count" else "paise"
    return {
        "question": question,
        "plan": plan,
        "sql_template": sql,
        "parameters": list(params),
        "rows": [list(r) for r in rows],
        "unit": unit,
        "backend": f"{backend}-baseline",
        "explanation": (
            "Planner emits a constrained plan only. Application code owns SQL templates "
            "and binds region as a parameter under a read-only SQLite session."
        ),
    }
