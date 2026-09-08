from django.shortcuts import render

from main.models import Experience


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