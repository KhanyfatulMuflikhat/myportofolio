from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Achievement
from main.forms import AchievementForm
from django.conf import settings

def show_main(request):
    context = {
        "name": "Khanyfatul Muflikhat",
        "npm": "2506589755",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Born and raised in South Jakarta, I'm Khanyfah, someone who balances a passion for robotics with a love for photography. "
            "These days I'm also deepening my understanding of Nahwu and Shorof and learning German."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Khanyfatul Muflikhat",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_achievement(request):
    json_response = get_achievements_json(request)

    achievements = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    achievement_list = [a.object for a in achievements]
    selected_level = request.GET.get("level")

    context = {
        "name": "Khanyfatul Muflikhat",
        "achievement_list": achievement_list,
        "level_choices": Achievement.LEVEL_CHOICES,
        "selected_level": selected_level,
    }
    return render(request, "achievement.html", context)

def create_achievement(request):
    form = AchievementForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            input_password = form.cleaned_data.get("password")
            if input_password != settings.ACHIEVEMENT_SECRET:
                messages.error(request, "Wrong password🤷‍♂️!")
            else:
                achievement = form.save(commit=False)
                achievement.save()
                messages.success(request, "New achievement succesfully added!!")
                return redirect("main:show_achievement")

    context = {
        "name": "Khanyfatul Muflikhat",
        "form": form,
    }
    return render(request, "achievement_form.html", context)

def get_achievements_json(request):
    level_query = request.GET.get("level", "").strip()
    achievements = Achievement.objects.all()

    if level_query:
        achievements = achievements.filter(level=level_query)

    achievements_json = serializers.serialize("json", achievements)
    return HttpResponse(achievements_json, content_type="application/json")

def delete_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        input_password = request.POST.get("password", "")
        if input_password != settings.ACHIEVEMENT_SECRET:
            messages.error(request, "Incorrect password, deletion canceled!")
        else:
            achievement.delete()
            messages.success(request, "Achievement succesfully deleted!")

    return redirect("main:show_achievement")