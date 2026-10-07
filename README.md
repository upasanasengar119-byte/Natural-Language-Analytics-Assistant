# Natural-Language Analytics Assistant (Text-to-SQL)

Portfolio project: turn business questions into a **validated semantic plan**, then execute **parameterized, read-only SQL** templates. The LLM/planner never emits raw SQL.

## Why this matters

Most text-to-SQL demos let a model write arbitrary SQL (injection + hallucinated joins). This project shows an enterprise-safe pattern:

1. Map NL → constrained plan `{metric, region}`
2. Validate allowlists in application code
3. Compile fixed SQL templates with `?` bindings
4. Run under SQLite `PRAGMA query_only=ON`

## Quick start

```bash
cd Natural-Language-Analytics-Assistant
python demo.py
python demo.py --interactive
python -m unittest discover -s tests -v
```

No third-party packages required (Python 3.10+).

## Example

```text
Q: What are total sales in EU?
plan: {metric: total, region: EU}
sql:  SELECT COALESCE(SUM(amount), 0) AS value FROM sales WHERE region=?
rows: [[22000]]  (unit: paise)
```

## Project layout

```text
data/sales.csv      # fixture orders (EU/US/IN)
src/planner.py      # NL → plan
src/executor.py     # plan → SQL → results
demo.py             # end-to-end CLI
tests/              # unit tests
INTERVIEW_PREP.md   # talk track + Q&A
```

## Architecture

```text
Business question
    → Plan interpreter (allowlisted metrics/regions)
    → Template compiler (code-owned SQL)
    → Read-only SQLite
    → Result + query trace (plan, sql_template, parameters, rows)
```

## Demo script for GitHub / interviews

1. Run `python demo.py` and show plan + SQL + rows for EU totals.
2. Show count + by-region.
3. Show rejection of `profit by product`.
4. Explain: *new capability requires schema + validator + template + tests together*.

## License

MIT — feel free to fork and extend.
