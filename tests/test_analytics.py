"""Tests for Text-to-SQL analytics assistant."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.executor import answer_question

DATA = ROOT / "data" / "sales.csv"


class AnalyticsTests(unittest.TestCase):
    def test_total_eu(self):
        result = answer_question("What are total sales in EU?", DATA)
        self.assertEqual(result["plan"], {"metric": "total", "region": "EU"})
        self.assertEqual(result["rows"][0][0], 22000)
        self.assertEqual(result["unit"], "paise")
        self.assertIn("?", result["sql_template"])

    def test_count_us(self):
        result = answer_question("How many orders in US", DATA)
        self.assertEqual(result["rows"][0][0], 2)
        self.assertEqual(result["unit"], "orders")

    def test_by_region(self):
        result = answer_question("sales by region", DATA)
        self.assertEqual(len(result["rows"]), 3)

    def test_rejects_unsupported(self):
        with self.assertRaises(ValueError):
            answer_question("profit by product", DATA)


if __name__ == "__main__":
    unittest.main()
