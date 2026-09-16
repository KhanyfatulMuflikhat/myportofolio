from django.forms import ModelForm, TextInput, Textarea, URLInput, Select, DateInput

from main.models import Achievement


class AchievementForm(ModelForm):
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
            "title": TextInput(
                attrs={
                    "placeholder": "Juara 1 Hackathon Nasional",
                    "maxlength": 255,
                }
            ),
            "issuer": TextInput(
                attrs={
                    "placeholder": "Kementerian Pendidikan",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan pencapaianmu",
                    "rows": 3,
                }
            ),
            "level": Select(),
            "date_achieved": DateInput(
                attrs={"type": "date"}
            ),
            "certificate_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/...",
                }
            ),
        }