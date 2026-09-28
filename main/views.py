import datetime
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from main.models import Experience, Achievement
from main.forms import AchievementForm, ExperienceForm

PROFILE_NAME = "Khanyfatul Muflikhat"


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": PROFILE_NAME,
        "npm": "2506589755",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Born and raised in South Jakarta, I'm Khanyfah, someone who balances a passion for robotics with a love for photography. "
            "These days I'm also deepening my understanding of Nahwu and Shorof and learning German."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


# Experience

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


@login_required(login_url="/login/")
def create_experience(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = ExperienceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New experience succesfully added!!")
        return redirect("main:show_experience")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "experience_form.html", context)


@login_required(login_url="/login/")
def update_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
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

    experiences_json = serializers.serialize(
           "json", experiences, use_natural_foreign_keys=True
    )
    return HttpResponse(experiences_json, content_type="application/json")


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    experience = get_object_or_404(Experience, pk=experience_id)
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience succesfully deleted!")

    return redirect("main:show_experience")


# Achievement

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


@login_required(login_url="/login/")
def create_achievement(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = AchievementForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New achievement succesfully added!!")
        return redirect("main:show_achievement")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "achievement_form.html", context)


@login_required(login_url="/login/")
def update_achievement(request, achievement_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    achievement = get_object_or_404(Achievement, pk=achievement_id)
    form = AchievementForm(request.POST or None, instance=achievement)

    if request.method == "POST" and form.is_valid():
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


def get_achievements_json(request):
    level_query = request.GET.get("level", "").strip()
    achievements = Achievement.objects.all()

    if level_query:
        achievements = achievements.filter(level=level_query)

       # di get_achievements_json
    achievements_json = serializers.serialize(
       "json", achievements, use_natural_foreign_keys=True
    )
    return HttpResponse(achievements_json, content_type="application/json")


@login_required(login_url="/login/")
def delete_achievement(request, achievement_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    achievement = get_object_or_404(Achievement, pk=achievement_id)
    if request.method == "POST":
        achievement.delete()
        messages.success(request, "Achievement succesfully deleted!")

    return redirect("main:show_achievement")


# Auth
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": PROFILE_NAME,
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


@login_required(login_url="/login/")
def toggle_star_achievement(request, achievement_id):
    achievement = get_object_or_404(Achievement, pk=achievement_id)

    if request.method == "POST":
        if request.user in achievement.starred_by.all():
            achievement.starred_by.remove(request.user)
        else:
            achievement.starred_by.add(request.user)

    return redirect("main:show_achievement")


@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")