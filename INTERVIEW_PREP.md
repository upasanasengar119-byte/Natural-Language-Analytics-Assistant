# Interview prep — Text-to-SQL Analytics Assistant

## 60-second pitch

I built a natural-language analytics assistant that does **not** let an LLM write SQL. It maps a question to a small semantic plan (`metric`, `region`), validates allowlists in code, then compiles a reviewed SQL template with bound parameters under a read-only SQLite session. That keeps language flexible while keeping database capability auditable.

## Live demo commands

```bash
python demo.py
python demo.py --question "How many orders in US"
python -m unittest discover -s tests -v
```

## Architecture talking points

- **Trust boundary:** model output is untrusted data; SQL is owned by application code.
- **Parameters** stop string injection; they do **not** replace authorization.
- **Integer paise** avoid float rounding for money.
- **Unsupported intents fail closed** instead of guessing a query.

## Likely interview Q&A

**Q: Why generate a plan instead of SQL?**  
A: A small plan only exposes capabilities we intentionally support. Code compiles reviewed templates. Easier to validate than arbitrary model SQL.

**Q: What do SQL parameters protect?**  
A: They keep values out of SQL syntax. They do not grant table access or validate business meaning — you still need permissions + semantic validation.

**Q: Can read-only SQL still be risky?**  
A: Yes — data leakage and expensive scans. Production needs scoped credentials, RLS, timeouts, row limits, and audited metrics.

**Q: How do you test NL correctness?**  
A: Pair questions with expected plans + expected rows. Cover paraphrases, punctuation, ambiguity, and unsupported asks separately.

**Q: How would you add a new metric?**  
A: Update allowlist, planner phrases, SQL template, and tests together. Prompt-only changes must not unlock new DB power.

## Failure cases to mention

- `profit by product` → `ValueError` (unsupported)
- Ambiguous questions → prefer clarification in production
- Wrong plan + valid SQL = still a wrong answer → always inspect the plan

## Production next steps (say this in interviews)

Semantic layer / metric catalog, read-only DB role, row-level security, query timeouts, paraphrase evaluation harness, optional Ollama/LLM planner with the **same** JSON schema validation.
