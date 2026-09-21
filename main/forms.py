from django import forms

from main.models import Achievement


class AchievementForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Masukkan kode rahasia"}),
        label="Kode Rahasia",
        required=True,
    )

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