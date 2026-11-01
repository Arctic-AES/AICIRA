import math
import unittest

from aicira.physics import Cylinder, analytical_reference


class PhysicsTests(unittest.TestCase):
    def test_reference_values(self):
        result = analytical_reference()
        self.assertAlmostEqual(result["membrane_area_mm2"], 188.495559, places=5)
        self.assertAlmostEqual(result["elastic_shortening_mm"], 0.0345989, places=6)
        self.assertAlmostEqual(result["ideal_buckling_load_n"], 42425, delta=50)
        self.assertAlmostEqual(result["ideal_mass_kg"], 0.22902, places=4)

    def test_load_scaling(self):
        one, two = analytical_reference(), analytical_reference(force_n=2000)
        self.assertAlmostEqual(two["elastic_shortening_mm"], 2*one["elastic_shortening_mm"])
        self.assertAlmostEqual(one["ideal_buckling_load_n"], two["ideal_buckling_load_n"])

    def test_invalid_dimensions(self):
        with self.assertRaises(ValueError):
            Cylinder(thickness_mm=80)
        with self.assertRaises(ValueError):
            Cylinder(poisson_ratio=0.5)
