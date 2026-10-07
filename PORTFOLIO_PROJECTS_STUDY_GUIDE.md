# Portfolio projects — study + GitHub publish guide

Three end-to-end demos aligned with your resume Key Projects.

| Folder on D:\ | Resume name | Skill signal |
|---------------|-------------|--------------|
| Natural-Language-Analytics-Assistant | Text-to-SQL Analytics Assistant | Safe GenAI + SQL trust boundary |
| Durable-Multi-Agent-Research-Assistant | Durable Multi-Agent Research Assistant | Agentic orchestration + durability |
| RAG-Evaluation-Workbench | RAG Evaluation Workbench | Measurement / ML maturity |

Each folder has `README.md` + `INTERVIEW_PREP.md` + `demo.py` + `tests/`.

## Run everything (sanity check)

```powershell
cd D:\Natural-Language-Analytics-Assistant
python demo.py
python -m unittest discover -s tests -v

cd D:\RAG-Evaluation-Workbench
python demo.py
python -m unittest discover -s tests -v

cd D:\Durable-Multi-Agent-Research-Assistant
python demo.py --run-all
python demo.py --reset --step-budget 1
python demo.py --step-budget 1
python demo.py --step-budget 1
python -m unittest discover -s tests -v
```

## Publish to GitHub (3 separate repos — recommended)

```powershell
cd D:\Natural-Language-Analytics-Assistant
git init
git add .
git commit -m "Initial commit: Text-to-SQL analytics assistant portfolio demo"
gh repo create Natural-Language-Analytics-Assistant --public --source=. --remote=origin --push
```

Repeat for the other two folders.

Suggested repo names:
- Natural-Language-Analytics-Assistant
- Durable-Multi-Agent-Research-Assistant
- RAG-Evaluation-Workbench

Then pin them on GitHub and link from LinkedIn / resume.

## 3-day interview prep plan

### Day 1 — Text-to-SQL
1. Read INTERVIEW_PREP.md
2. Run demo; explain why plan is not SQL
3. Memorize: parameters, read-only risk, how to add a metric

### Day 2 — RAG Eval
1. Read INTERVIEW_PREP.md
2. Run `python demo.py --k 3` and `--k 1`
3. Memorize: recall vs precision vs MRR, unanswerable abstention, retrieval is not answer quality

### Day 3 — Multi-Agent Research
1. Read INTERVIEW_PREP.md
2. Do stepwise resume demo live
3. Memorize: state machine, SQLite checkpoints, compare-and-swap, fingerprint, bounded vs autonomous agent
4. Practice bridging to Data Dynamics multi-agent PII work

## One story that ties all three

At work I build enterprise document intelligence (PII, RAG chat, classification). In my portfolio I show three complementary production skills: safe tool use (Text-to-SQL plans, not raw SQL), agent durability (checkpointed multi-step research), and evaluation (golden-set RAG retrieval metrics). Together they show I can ship GenAI that is explainable, resumable, and measurable.

## Honesty tip

These are portfolio demos (local TF-IDF / SQLite / stdlib). In interviews say you implemented them end-to-end as portfolio systems and apply the same principles at work on larger NLP/RAG/Kafka stacks. Do not claim these folders ran in production at Data Dynamics.
