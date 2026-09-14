from django.shortcuts import render

from main.models import Experience, Achievement


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
    achievement_list = Achievement.objects.all()
    selected_level = request.GET.get('level')
    if selected_level:
        achievement_list = achievement_list.filter(level=selected_level)

    context = {
        "name": "Khanyfatul Muflikhat",
        "achievement_list": achievement_list,
        "level_choices": Achievement.LEVEL_CHOICES,
        "selected_level": selected_level,
    }
    return render(request, "achievement.html", context)