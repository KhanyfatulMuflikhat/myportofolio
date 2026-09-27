from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Achievement
from main.forms import AchievementForm, ExperienceForm
from django.conf import settings

PROFILE_NAME = "Khanyfatul Muflikhat"

def show_main(request):
    context = {
        "name": PROFILE_NAME,
        "npm": "2506589755",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Born and raised in South Jakarta, I'm Khanyfah, someone who balances a passion for robotics with a love for photography. "
            "These days I'm also deepening my understanding of Nahwu and Shorof and learning German."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [e.object for e in experiences]
    selected_category = request.GET.get("category")

    context = {
        "name": PROFILE_NAME,
        "experience_list": experience_list,
        "category_choices": Experience.EXPERIENCE_CHOICES,
        "selected_category": selected_category,
    }
    return render(request, "experience.html", context)


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            input_password = form.cleaned_data.get("password")
            if input_password != settings.PROJECT_SECRET:
                messages.error(request, "Wrong password bos!")
            else:
                form.save()
                messages.success(request, "New experience succesfully added!!")
                return redirect("main:show_experience")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST":
        if form.is_valid():
            input_password = form.cleaned_data.get("password")
            if input_password != settings.PROJECT_SECRET:
                messages.error(request, "Wrong password bos!")
            else:
                form.save()
                messages.success(request, "Experience succesfully updated!!")
                return redirect("main:show_experience")

    context = {
        "name": PROFILE_NAME,
        "form": form,
        "experience": experience,
        "mode": "edit",
    }
    return render(request, "experience_form.html", context)


def get_experiences_json(request):
    category_query = request.GET.get("category", "").strip()
    experiences = Experience.objects.all()

    if category_query:
        experiences = experiences.filter(category=category_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        input_password = request.POST.get("password", "")
        if input_password != settings.PROJECT_SECRET:
            messages.error(request, "Incorrect password, deletion canceled!")
        else:
            experience.delete()
            messages.success(request, "Experience succesfully deleted!")

    return redirect("main:show_experience")

def show_achievement(request):
    json_response = get_achievements_json(request)

    achievements = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    achievement_list = [a.object for a in achievements]
    selected_level = request.GET.get("level")

    context = {
        "name": PROFILE_NAME,
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
            if input_password != settings.PROJECT_SECRET:
                messages.error(request, "Wrong password bos!")
            else:
                form.save()
                messages.success(request, "New achievement succesfully added!!")
                return redirect("main:show_achievement")

    context = {
        "name": PROFILE_NAME,
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
        if input_password != settings.PROJECT_SECRET:
            messages.error(request, "Incorrect password, deletion canceled!")
        else:
            achievement.delete()
            messages.success(request, "Achievement succesfully deleted!")

    return redirect("main:show_achievement")

def update_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)
    form = AchievementForm(request.POST or None, instance=achievement)

    if request.method == "POST":
        if form.is_valid():
            input_password = form.cleaned_data.get("password")
            if input_password != settings.PROJECT_SECRET:
                messages.error(request, "Wrong password bos!")
            else:
                form.save()
                messages.success(request, "Achievement succesfully updated!!")
                return redirect("main:show_achievement")

    context = {
        "name": PROFILE_NAME,
        "form": form,
        "achievement": achievement,
        "mode": "edit",
    }
    return render(request, "achievement_form.html", context)