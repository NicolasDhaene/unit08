from django.conf.urls import url
from . import views
urlpatterns = [
    url(r"upload/", views.add_json_to_db, name="upload"),
    url(r"^$", views.mineral_list, name="home"),
    url(r"^list/(?P<selected_letter>[a-z])$", views.mineral_list, name="alphabetically_filtered_list_view"),
    url(r"^group/(?P<selected_group>\w+)/$", views.mineral_list, name="group_filtered_list_view"),
    url(r"search/$", views.search, name="search"),
    url(r"^detail/(?P<pk>\d+)/$", views.mineral_detail, name="detail"),
]