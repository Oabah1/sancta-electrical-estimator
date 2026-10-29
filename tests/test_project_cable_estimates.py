import unittest

from app import create_app, db
from app.models import Cable, Project, ProjectCableEstimate


class TestProjectCableEstimateRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        })
        self.context = self.app.app_context()
        self.context.push()

        db.create_all()

        self.project = Project(
            project_name="Cable Test Project",
            customer_name="Test Customer",
            location="Otukpo",
            building_type="Residential",
            number_of_floors=1,
        )
        db.session.add(self.project)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()

    def test_manual_cable_estimate_saves_specifications(self):
        response = self.client.post(
            f"/projects/{self.project.id}/cable-estimates",
            data={
                "entry_mode": "manual",
                "manual_cable_type": "Single Core PVC Copper",
                "manual_brand": "Test Brand",
                "manual_size": "2.5 mm²",
                "manual_colour": "Red",
                "manual_function": "Live",
                "manual_conductor_material": "Copper",
                "manual_insulation": "PVC",
                "manual_coil_length": "100",
                "manual_unit_price": "25000",
                "required_metres": "150",
            },
        )

        self.assertEqual(response.status_code, 302)

        estimate = ProjectCableEstimate.query.one()
        self.assertEqual(estimate.conductor_material, "Copper")
        self.assertEqual(estimate.insulation, "PVC")
        self.assertEqual(estimate.required_metres, 150)
        self.assertIsNone(estimate.cable_id)

    def test_edit_updates_conductor_and_insulation(self):
        estimate = ProjectCableEstimate(
            project_id=self.project.id,
            cable_type="Single Core",
            size="2.5 mm²",
            colour="Red",
            conductor_material="Copper",
            insulation="PVC",
            required_metres=100,
            coil_length=100,
            unit_price=25000,
        )
        db.session.add(estimate)
        db.session.commit()

        response = self.client.post(
            (
                f"/projects/{self.project.id}/cable-estimates/"
                f"{estimate.id}/edit"
            ),
            data={
                "entry_mode": "manual",
                "manual_cable_type": "Single Core",
                "manual_brand": "Test Brand",
                "manual_size": "2.5 mm²",
                "manual_colour": "Black",
                "manual_function": "Neutral",
                "manual_conductor_material": "Aluminium",
                "manual_insulation": "XLPE",
                "manual_coil_length": "100",
                "manual_unit_price": "30000",
                "required_metres": "200",
            },
        )

        self.assertEqual(response.status_code, 302)

        db.session.refresh(estimate)
        self.assertEqual(estimate.conductor_material, "Aluminium")
        self.assertEqual(estimate.insulation, "XLPE")
        self.assertEqual(estimate.colour, "Black")
        self.assertEqual(estimate.required_metres, 200)

    def test_catalogue_entry_copies_cable_specifications(self):
        cable = Cable(
            cable_type="Single Core PVC",
            brand="Catalogue Brand",
            conductor_material="Copper",
            insulation="PVC",
            size="4 mm²",
            colour="Green-Yellow",
            function="Earth",
            coil_length=100,
            unit_price=32000,
        )
        db.session.add(cable)
        db.session.commit()

        response = self.client.post(
            f"/projects/{self.project.id}/cable-estimates",
            data={
                "entry_mode": "catalogue",
                "cable_id": str(cable.id),
                "required_metres": "75",
            },
        )

        self.assertEqual(response.status_code, 302)

        estimate = ProjectCableEstimate.query.one()
        self.assertEqual(estimate.cable_id, cable.id)
        self.assertEqual(estimate.conductor_material, "Copper")
        self.assertEqual(estimate.insulation, "PVC")
        self.assertEqual(estimate.size, "4 mm²")
        self.assertEqual(estimate.colour, "Green-Yellow")

    def test_invalid_required_length_does_not_save_estimate(self):
        response = self.client.post(
            f"/projects/{self.project.id}/cable-estimates",
            data={
                "entry_mode": "manual",
                "manual_cable_type": "Single Core",
                "manual_size": "2.5 mm²",
                "manual_colour": "Red",
                "manual_conductor_material": "Copper",
                "manual_insulation": "PVC",
                "manual_coil_length": "100",
                "manual_unit_price": "25000",
                "required_metres": "0",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ProjectCableEstimate.query.count(), 0)


if __name__ == "__main__":
    unittest.main()
