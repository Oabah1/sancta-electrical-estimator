import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.services.cable_service import (
    calculate_coils,
    estimate_circuit_conductor_length,
    estimate_circuit_cable_cost,
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


class TestCircuitCableCostEstimate(unittest.TestCase):

    @patch("app.services.cable_service.calculate_cable_cost")
    @patch("app.services.cable_service.db.session.get")
    def test_estimates_cable_quantity_and_cost(
        self, mock_get, mock_calculate_cost
    ):
        circuit = SimpleNamespace(
            id=1,
            project_id=1,
            circuit_name="Test Lighting Circuit",
            circuit_type="Lighting",
            route_length=20,
        )
        cable = SimpleNamespace(id=1)

        mock_get.side_effect = [circuit, cable]
        mock_calculate_cost.return_value = {
            "required_metres": 44,
            "number_of_coils": 1,
            "total_cost": 25000,
        }

        result = estimate_circuit_cable_cost(
            circuit_id=1,
            cable_id=1,
            conductor_count=2,
            allowance_percent=10,
        )

        self.assertEqual(result["project_id"], 1)
        self.assertEqual(result["circuit_id"], 1)
        self.assertEqual(
            result["length_estimate"]["estimated_length"], 44
        )
        self.assertEqual(result["cable_cost"]["number_of_coils"], 1)
        self.assertEqual(result["cable_cost"]["total_cost"], 25000)
        mock_calculate_cost.assert_called_once_with(cable, 44)

    @patch("app.services.cable_service.db.session.get", return_value=None)
    def test_missing_circuit_is_rejected(self, mock_get):
        with self.assertRaisesRegex(ValueError, "Circuit record 99"):
            estimate_circuit_cable_cost(99, 1, 2)

    @patch("app.services.cable_service.db.session.get")
    def test_missing_cable_is_rejected(self, mock_get):
        circuit = SimpleNamespace(
            id=1,
            project_id=1,
            circuit_name="Test Circuit",
            circuit_type="Lighting",
            route_length=20,
        )
        mock_get.side_effect = [circuit, None]

        with self.assertRaisesRegex(ValueError, "Cable record 99"):
            estimate_circuit_cable_cost(1, 99, 2)


if __name__ == "__main__":
    unittest.main()
