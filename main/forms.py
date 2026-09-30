from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

from main.models import Achievement, Experience

class AchievementForm(forms.ModelForm):

    class Meta:
        model = Achievement
        fields = [
            "title",
            "issuer",
            "description",
            "level",
            "date_achieved",
            "certificate_url",
        ]

        labels = {
            "title": "Nama Pencapaian",
            "issuer": "Penyelenggara",
            "description": "Deskripsi",
            "level": "Tingkat",
            "date_achieved": "Tanggal Diraih",
            "certificate_url": "URL Sertifikat",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Juara 1 Hackathon Nasional",
                    "maxlength": 255,
                }
            ),
            "issuer": forms.TextInput(
                attrs={
                    "placeholder": "Kementerian Pendidikan",
                    "maxlength": 255,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Ceritakan pencapaianmu",
                    "rows": 3,
                }
            ),
            "level": forms.Select(),
            "date_achieved": forms.DateInput(
                attrs={"type": "date"}
            ),
            "certificate_url": forms.URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/...",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Judul achievement tidak boleh hanya berisi tag HTML.")
        return title

    def clean_issuer(self):
        return strip_tags(self.cleaned_data["issuer"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()

class ExperienceForm(forms.ModelForm):

    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "ended_at",
        ]

        labels = {
            "title": "Judul",
            "description": "Deskripsi",
            "category": "Kategori",
            "thumbnail": "URL Thumbnail",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Software Engineer Intern",
                    "maxlength": 255,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": forms.Select(),
            "thumbnail": forms.URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
            "ended_at": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError("Judul experience tidak boleh hanya berisi tag HTML.")
        return title

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()