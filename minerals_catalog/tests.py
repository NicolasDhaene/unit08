from django.test import TestCase
from django.urls import reverse
from .models import Mineral


mineral1 = {
    "name": "Alabandite",
    "image_filename": "Alabandite.jpg",
    "image_caption": "Group of octahedral alabandite crystals partially coated with pink rhodochrosite, from Uchucchacua Mine, Oyon, Lima, Peru (size: 60 mm x 59 mm x 46 mm, 204 g)",
    "category": "Sulfide",
    "formula": "MnS",
    "strunz_classification": "02.CD.10II/C.15-30 (8 ed)",
    "crystal_system": "Cubic hexoctahedral",
    "unit_cell": "a = 5.2236 \u00c5; Z = 4",
    "color": "black, steelgray, brownish-black",
    "crystal_symmetry": "Cubic 4/m 3 2/m",
    "cleavage": "Perfect on {100}",
    "mohs_scale_hardness": "3.5 to 4",
    "luster": "Sub-metallic",
    "streak": "Green",
    "diaphaneity": "Opaque, translucent in thin fragments",
    "optical_properties": "Isotropic",
    "refractive_index": "n = 2.70",
    "crystal_habit": "mostly massive or granular; cubic or octahedral crystals to 1 cm",
    "specific_gravity": "4.053",
    "group": "Sulfides"
  }

mineral2 = {
    "name": "Bayleyite",
    "image_filename": "Bayleyite.jpg",
    "image_caption": "Bayleyite sample from the Ambrosia area, Grants District, New Mexico (size: 4.6 x 2.4 x 1.6 cm)",
    "category": "Carbonate",
    "formula": "Mg<sub>2</sub>(UO<sub>2</sub>)(CO<sub>3</sub>)<sub>3</sub>\u00b7<sub>18</sub>(H<sub>2</sub>O)",
    "strunz_classification": "05.ED.05",
    "crystal_system": "Monoclinic",
    "unit_cell": "a = 26.65 \u00c5, b = 15.31 \u00c5, c = 6.53 \u00c5; \u03b2 = 93.07\u00b0; Z=4",
    "color": "Sulfur yellow",
    "crystal_symmetry": "Monoclinic prismaticH-M symbol: (2/m)Space group: P 21/a",
    "mohs_scale_hardness": "2 - 2.5",
    "luster": "Vitreous",
    "diaphaneity": "Semitransparent",
    "optical_properties": "Biaxial (-)",
    "refractive_index": "n\u03b1 = 1.453 - 1.455 n\u03b2 = 1.490 - 1.492 n\u03b3 = 1.498 - 1.502",
    "crystal_habit": "Clusters of prismatic crystals, crusts",
    "specific_gravity": "2.05",
    "group": "Carbonates"
  }


class MineralModelTest(TestCase):
    def test_mineral_creation(self):
        mineral = Mineral.objects.create(**mineral1)
        self.assertEqual(mineral.name, "Alabandite")


class ViewsTest(TestCase):
    def setUp(self):
        self.mineral = Mineral.objects.create(**mineral1)
        self.mineral2 = Mineral.objects.create(**mineral2)

    def test_mineral_list_view(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context["minerals"])
        self.assertNotIn(self.mineral2, resp.context["minerals"])
        self.assertTemplateUsed(resp, 'minerals_catalog/index.html')
        self.assertContains(resp, self.mineral.name)

    def test_mineral_detail_view(self):
        resp = self.client.get(
            reverse("detail", kwargs={"pk": self.mineral.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.mineral, resp.context["mineral"])
        self.assertTemplateUsed(resp, "minerals_catalog/detail.html")

    def test_alphabetically_filtered_list_view(self):
        resp = self.client.get(
            reverse("alphabetically_filtered_list_view", kwargs={"selected_letter": "b"})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.mineral, resp.context["minerals"])
        self.assertIn(self.mineral2, resp.context["minerals"])

    def test_group_filtered_list_view(self):
        resp = self.client.get(
            reverse(
                "group_filtered_list_view",
                kwargs={"selected_group": "Carbonates"}
            )
        )
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(self.mineral, resp.context["minerals"])
        self.assertIn(self.mineral2, resp.context["minerals"])

    def test_search_name_view(self):
        resp = self.client.get(reverse("search"), {"q": "alab", "scope": "name_search"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context["minerals"])
        self.assertNotIn(self.mineral2, resp.context["minerals"])
        self.assertTemplateUsed(resp, "minerals_catalog/index.html")

    def test_search_color_view(self):
        resp = self.client.get(reverse("search"), {"q": "black", "scope": "color_search"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context["minerals"])
        self.assertNotIn(self.mineral2, resp.context["minerals"])

    def test_search_all_view(self):
        resp = self.client.get(reverse("search"), {"q": "05", "scope": "all_search"})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.mineral, resp.context["minerals"])
        self.assertIn(self.mineral2, resp.context["minerals"])