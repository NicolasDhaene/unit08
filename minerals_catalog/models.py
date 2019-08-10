from django.db import models
from collections import defaultdict


class Mineral(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255, null=True)
    image_caption = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True)
    formula = models.CharField(max_length=255, null=True)
    strunz_classification = models.CharField(max_length=255, null=True)
    crystal_system = models.CharField(max_length=255, null=True)
    unit_cell = models.CharField(max_length=255, null=True)
    color = models.CharField(max_length=255, null=True)
    crystal_symmetry = models.CharField(max_length=255, null=True)
    cleavage = models.CharField(max_length=255, null=True)
    mohs_scale_hardness = models.CharField(max_length=255, null=True)
    luster = models.CharField(max_length=255, null=True)
    streak = models.CharField(max_length=255, null=True)
    diaphaneity = models.CharField(max_length=255, null=True)
    optical_properties = models.CharField(max_length=255, null=True)
    refractive_index = models.CharField(max_length=255, null=True)
    crystal_habit = models.CharField(max_length=255, null=True)
    specific_gravity = models.CharField(max_length=255, null=True)
    group = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    def attributes_sorted_most_common(self):
        attributes_occurences_counted = defaultdict(int)
        # excluded fields are not relevant to characterize the minerals
        excluded_fields = ["id", "name",  "image_filename",  "image_caption"]
        minerals = Mineral.objects.all()
        for mineral in minerals:
            for field in Mineral._meta.get_fields():
                if field.name not in excluded_fields and \
                        getattr(mineral, field.name):
                    attributes_occurences_counted[field.name] += 1
        attributes_sorted = sorted(attributes_occurences_counted, key=attributes_occurences_counted.get, reverse=True)
        most_common_attributes = []
        for attribute in attributes_sorted:
            key = self._meta.get_field(attribute).verbose_name
            value = getattr(self, attribute)
            if value :
                most_common_attributes.append({"key": key, "value": value})
        return most_common_attributes

