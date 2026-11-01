import math
import unittest

from aicira.cases import Dent, case_manifest, default_cases


class GeometryTests(unittest.TestCase):
    def test_twelve_cases(self):
        cases = default_cases()
        self.assertEqual(len(cases), 12)
        self.assertEqual(len({(c.depth_mm, c.axial_width_mm) for c in cases}), 12)
        self.assertEqual([x.case_id for x in cases], [f"I{i:02d}" for i in range(1, 13)])

    def test_dent_center_and_periodicity(self):
        d = Dent("check", 0.04, 20, 20)
        self.assertAlmostEqual(d.radius_at(0, 225), 74.96, places=10)
        self.assertAlmostEqual(d.radius_at(2 * math.pi, 225), 74.96, places=10)
        self.assertGreater(d.radius_at(0, 300), 74.959999)
        self.assertLessEqual(d.radius_at(1, 225), 75)

    def test_manifest(self):
        manifest = case_manifest()
        self.assertEqual(len(manifest), 13)
        self.assertEqual(manifest[0]["case_id"], "P00")
        self.assertTrue(all(row["status"] == "not_run" for row in manifest))
