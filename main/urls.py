from django.urls import path

from main.views import (
    show_main, show_experience, show_achievement,
    create_achievement, update_achievement,
    get_achievements_json, delete_achievement,
    create_experience, update_experience,
    delete_experience, get_experiences_json,
)
app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/edit/", update_experience, name="update_experience"),
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("achievement/", show_achievement, name="show_achievement"),
    path("achievement/add/", create_achievement, name="create_achievement"),
    path("achievement/<uuid:achievement_id>/edit/", update_achievement, name="update_achievement"),
    path("api/achievements/", get_achievements_json, name="get_achievements_json"),
    path("achievement/<uuid:achievement_id>/delete/", delete_achievement, name="delete_achievement"),
]