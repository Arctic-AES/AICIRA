import csv
import tempfile
import unittest
from pathlib import Path

from aicira.fea import assess_history, read_history


class FEATests(unittest.TestCase):
    def test_incomplete_is_not_peak(self):
        values = [{"shortening_mm": n/100, "top_compression_N": n*200}
                  for n in range(0, 135)]
        got = assess_history(values)
        self.assertFalse(got["reached_target"])
        self.assertIsNone(got["accepted_peak_force_n"])

    def test_complete_with_postpeak(self):
        values = [
            {"shortening_mm": 0.0, "top_compression_N": 0},
            {"shortening_mm": 1.3, "top_compression_N": 38000},
            {"shortening_mm": 1.48, "top_compression_N": 43000},
            {"shortening_mm": 1.6, "top_compression_N": 11000},
        ]
        got = assess_history(values)
        self.assertTrue(got["peak_eligible_for_comparison"])
        self.assertEqual(got["accepted_peak_force_n"], 43000)

    def test_rejects_monotonic_force_as_collapse_peak(self):
        values = [{"shortening_mm": 0, "top_compression_N": 0},
                  {"shortening_mm": 1.6, "top_compression_N": 40000}]
        self.assertIsNone(assess_history(values)["accepted_peak_force_n"])

    def test_reader(self):
        with tempfile.TemporaryDirectory() as dirname:
            p = Path(dirname) / "history.csv"
            p.write_text("time,shortening_mm,top_compression_N\n0,0,0\n1,1.6,10000\n")
            self.assertEqual(len(read_history(p)), 2)

    def test_bad_shortening_order(self):
        with self.assertRaises(ValueError):
            assess_history([{"shortening_mm": 1, "top_compression_N": 5},
                            {"shortening_mm": 0, "top_compression_N": 4}])
