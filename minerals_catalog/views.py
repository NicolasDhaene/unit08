from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from minerals_catalog.models import Mineral
import json
import random


def add_json_to_db(request):
    """Function used to populate db from json file"""
    csv_file = "minerals.json"
    with open(csv_file, encoding="utf-8") as csv_file:
        minerals = json.load(csv_file)
        for mineral in minerals:
            # create a blank dict
            full_mineral_dict = {
                "name": None,
                "image_filename": None,
                "image_caption": None,
                "category": None,
                "formula": None,
                "strunz_classification": None,
                "crystal_system": None,
                "unit_cell": None,
                "color": None,
                "crystal_symmetry": None,
                "cleavage": None,
                "mohs_scale_hardness": None,
                "luster": None,
                "streak": None,
                "diaphaneity": None,
                "optical_properties": None,
                "refractive_index": None,
                "crystal_habit": None,
                "specific_gravity": None,
                "group": None
            }
            # populate blank dict when information available
            for key, value in mineral.items():
                full_mineral_dict[key] = value
            # check if mineral already outstanding, create if not
            try:
                Mineral.objects.get(name=full_mineral_dict["name"])
                continue
            except Mineral.DoesNotExist:
                Mineral(
                    name=full_mineral_dict["name"],
                    image_filename=full_mineral_dict["image_filename"],
                    image_caption=full_mineral_dict["image_caption"],
                    category=full_mineral_dict["category"],
                    formula=full_mineral_dict["formula"],
                    strunz_classification=full_mineral_dict["strunz_classification"],
                    crystal_system=full_mineral_dict["crystal_system"],
                    unit_cell=full_mineral_dict["unit_cell"],
                    color=full_mineral_dict["color"],
                    crystal_symmetry=full_mineral_dict["crystal_symmetry"],
                    cleavage=full_mineral_dict["cleavage"],
                    mohs_scale_hardness=full_mineral_dict["mohs_scale_hardness"],
                    luster=full_mineral_dict["luster"],
                    streak=full_mineral_dict["streak"],
                    diaphaneity=full_mineral_dict["diaphaneity"],
                    optical_properties=full_mineral_dict["optical_properties"],
                    refractive_index=full_mineral_dict["refractive_index"],
                    crystal_habit=full_mineral_dict["crystal_habit"],
                    specific_gravity=full_mineral_dict["specific_gravity"],
                    group=full_mineral_dict["group"]
                ).save()
    return HttpResponse("It is done.")


def random_mineral():
    """Function used to select a random mineral"""
    all_minerals = Mineral.objects.all()
    return random.choice(all_minerals)


def setup_group_list():
    """Function used to populate a list of all groups in db"""
    all_minerals = Mineral.objects.all()
    group_list = []
    for each in all_minerals:
        if each.group.replace(" ", "_") not in group_list:
            group_list.append(each.group.replace(" ", "_"))
    return group_list


def setup_alphabet_list():
    """Function used to populate a list of first letter of all the minerals name in db"""
    all_minerals = Mineral.objects.all()
    alphabet_list = []
    for each in all_minerals:
        if each.name[0].lower() not in alphabet_list:
            alphabet_list += each.name[0].lower()
    return alphabet_list


def mineral_list(request, selected_letter=None, selected_group=None):
    """View that renders a list of minerals based on the selected letter or group"""
    """Random mineral also rendered"""
    random_mineral()
    if selected_group in setup_group_list():
        minerals = Mineral.objects.filter(group=selected_group.replace("_"," "))
    elif selected_letter in setup_alphabet_list():
        minerals = Mineral.objects.filter(name__startswith=selected_letter)
    else:
        selected_letter = "a"
        minerals = Mineral.objects.filter(name__startswith=selected_letter)
    return render(request, "minerals_catalog/index.html", {"minerals": minerals, "random_mineral": random_mineral,
                                                           "alphabet_list": setup_alphabet_list(),
                                                           "group_list": setup_group_list(),
                                                           "selected_letter": selected_letter,
                                                           "selected_group": selected_group})


def search(request):
    """View that renders a list of minerals based on searched term and scope applicable to searched term"""
    term = request.GET.get("q")
    scope = request.GET.get("scope")
    if scope == "name_search":
        minerals = Mineral.objects.filter(name__icontains=term)
    elif scope == "color_search":
        minerals = Mineral.objects.filter(color__icontains=term)
    else:
        query = Q()
        for field in Mineral._meta.get_fields():
            query |= Q(**{field.name + "__icontains": term})
            minerals = Mineral.objects.filter(query).distinct()
    random_mineral()
    return render(request, "minerals_catalog/index.html", {"minerals": minerals, "random_mineral": random_mineral,
                                                           "alphabet_list": setup_alphabet_list(),
                                                           "group_list": setup_group_list()})


def mineral_detail(request, pk):
    """View that renders a mineral and its attributes"""
    """The attributes are displayed starting with the most commons"""
    mineral = get_object_or_404(Mineral, pk=pk)
    random_mineral()
    attributes_sorted_most_common = mineral.attributes_sorted_most_common()
    return render(request, "minerals_catalog/detail.html", {'mineral': mineral, "random_mineral": random_mineral,
                                                            "alphabet_list": setup_alphabet_list(),
                                                            "group_list": setup_group_list(),
                                                            "attributes": attributes_sorted_most_common})
