"""End-to-end demo for Natural-Language Analytics Assistant."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.executor import answer_question

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "sales.csv"


def main() -> None:
    parser = argparse.ArgumentParser(description="Text-to-SQL analytics demo")
    parser.add_argument("--question", default="What are total sales in EU?")
    parser.add_argument("--interactive", action="store_true")
    args = parser.parse_args()

    if args.interactive:
        print("Ask total sales / order count / sales by region (Ctrl+C to exit)")
        while True:
            try:
                q = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not q:
                continue
            try:
                print(json.dumps(answer_question(q, DATA), indent=2))
            except ValueError as exc:
                print(f"ERROR: {exc}")
        return

    questions = [
        args.question,
        "How many orders in US",
        "sales by region",
    ]
    for q in questions:
        print("=" * 72)
        print(f"Q: {q}")
        print(json.dumps(answer_question(q, DATA), indent=2))

    print("=" * 72)
    print("Unsupported intent demo:")
    try:
        print(json.dumps(answer_question("profit by product", DATA), indent=2))
    except ValueError as exc:
        print(f"ERROR (expected): {exc}")


if __name__ == "__main__":
    main()
