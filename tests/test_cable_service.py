import unittest

from app.services.cable_service import (
    calculate_coils,
    estimate_circuit_conductor_length,
)


class TestCalculateCoils(unittest.TestCase):

    def test_one_coil_is_enough(self):
        result = calculate_coils(44, 100)
        self.assertEqual(result["number_of_coils"], 1)
        self.assertEqual(result["supplied_metres"], 100)
        self.assertEqual(result["spare_metres"], 56)

    def test_exact_coil_length(self):
        result = calculate_coils(100, 100)
        self.assertEqual(result["number_of_coils"], 1)
        self.assertEqual(result["spare_metres"], 0)

    def test_multiple_coils(self):
        result = calculate_coils(201, 100)
        self.assertEqual(result["number_of_coils"], 3)
        self.assertEqual(result["supplied_metres"], 300)

    def test_zero_required_length(self):
        result = calculate_coils(0, 100)
        self.assertEqual(result["number_of_coils"], 0)
        self.assertEqual(result["supplied_metres"], 0)

    def test_negative_required_length_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_coils(-1, 100)

    def test_zero_coil_length_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_coils(50, 0)


class TestCircuitConductorEstimate(unittest.TestCase):

    def test_estimate_with_allowance(self):
        result = estimate_circuit_conductor_length(20, 2, 10)
        self.assertEqual(result["base_length"], 40)
        self.assertEqual(result["allowance_length"], 4)
        self.assertEqual(result["estimated_length"], 44)

    def test_estimate_without_allowance(self):
        result = estimate_circuit_conductor_length(20, 2, 0)
        self.assertEqual(result["estimated_length"], 40)

    def test_zero_route_length(self):
        result = estimate_circuit_conductor_length(0, 2, 10)
        self.assertEqual(result["estimated_length"], 0)

    def test_negative_route_length_is_rejected(self):
        with self.assertRaises(ValueError):
            estimate_circuit_conductor_length(-1, 2, 10)

    def test_zero_conductors_is_rejected(self):
        with self.assertRaises(ValueError):
            estimate_circuit_conductor_length(20, 0, 10)

    def test_negative_allowance_is_rejected(self):
        with self.assertRaises(ValueError):
            estimate_circuit_conductor_length(20, 2, -1)


if __name__ == "__main__":
    unittest.main()
