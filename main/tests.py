import uuid

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from main.models import Experience, Achievement


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")

class AchievementTest(TestCase):
    def setUp(self):
        self.achievement = Achievement.objects.create(
            title="KIHAJAR STEM 2023",
            issuer="Kemendikbudristek",
            description="Penghargaan atas proyek SIPELAN, sistem pendeteksi lawan arah.",
            level="national",
            date_achieved="2023-10-01",
        )

    def test_achievement_url_is_accessible(self):
        response = self.client.get(reverse("main:show_achievement"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement.html")

    def test_achievement_data_appears(self):
        response = self.client.get(reverse("main:show_achievement"))

        self.assertContains(response, self.achievement.title)
        self.assertContains(response, self.achievement.issuer)
        self.assertContains(response, self.achievement.description)
        self.assertContains(response, "National")

    def test_empty_achievement_page(self):
        Achievement.objects.all().delete()
        response = self.client.get(reverse("main:show_achievement"))

        self.assertContains(response, "Belum ada penghargaan yang ditambahkan.")

    def test_filter_by_level(self):
        Achievement.objects.create(
            title="Regional Robotics Competition",
            issuer="Dinas Pendidikan",
            description="Juara di kompetisi robotika tingkat regional.",
            level="regional",
            date_achieved="2022-05-01",
        )

        response = self.client.get(reverse("main:show_achievement"), {"level": "national"})

        self.assertContains(response, self.achievement.title)
        self.assertNotContains(response, "Regional Robotics Competition")

class AchievementFormTest(TestCase):
    def test_create_achievement_page_accessible(self):
        response = self.client.get(reverse("main:create_achievement"))
        self.assertEqual(response.status_code, 200)

    def test_create_achievement_post_valid(self):
        response = self.client.post(reverse("main:create_achievement"), {
            "title": "Test Achievement",
            "issuer": "Test Issuer",
            "description": "Test desc",
            "level": "school",
            "date_achieved": "2026-01-01",
            "certificate_url": "",
            "password": settings.ACHIEVEMENT_SECRET,
        })
        self.assertEqual(Achievement.objects.count(), 1)
        self.assertRedirects(response, reverse("main:show_achievement"))

    def test_create_achievement_post_wrong_password(self):
        response = self.client.post(reverse("main:create_achievement"), {
            "title": "Test Achievement",
            "issuer": "Test Issuer",
            "description": "Test desc",
            "level": "school",
            "date_achieved": "2026-01-01",
            "certificate_url": "",
            "password": "wrong-secret",
        })
        self.assertEqual(Achievement.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_json_endpoint_returns_valid_json(self):
        response = self.client.get(reverse("main:get_achievements_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")

    def test_delete_achievement(self):
        achievement = Achievement.objects.create(
            title="To Delete", issuer="X", description="Y",
            level="school", date_achieved="2026-01-01",
        )
        response = self.client.post(
            reverse("main:delete_achievement", args=[achievement.id]),
            {"password": settings.ACHIEVEMENT_SECRET},
        )
        self.assertEqual(Achievement.objects.count(), 0)

    def test_delete_achievement_wrong_password(self):
        achievement = Achievement.objects.create(
            title="Not Deleted", issuer="X", description="Y",
            level="school", date_achieved="2026-01-01",
        )
        response = self.client.post(
            reverse("main:delete_achievement", args=[achievement.id]),
            {"password": "wrong-secret"},
        )
        self.assertEqual(Achievement.objects.count(), 1)

class AchievementUpdateTest(TestCase):
    def setUp(self):
        self.achievement = Achievement.objects.create(
            title="KIHAJAR STEM 2023",
            issuer="Kemendikbudristek",
            description="Penghargaan atas proyek SIPELAN.",
            level="national",
            date_achieved="2023-10-01",
        )

    def _valid_payload(self, **overrides):
        payload = {
            "title": self.achievement.title,
            "issuer": self.achievement.issuer,
            "description": self.achievement.description,
            "level": self.achievement.level,
            "date_achieved": self.achievement.date_achieved,
            "certificate_url": "",
            "password": settings.ACHIEVEMENT_SECRET,
        }
        payload.update(overrides)
        return payload

    def test_update_achievement_page_accessible_get(self):
        response = self.client.get(
            reverse("main:update_achievement", args=[self.achievement.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement_form.html")

    def test_update_form_prefilled_with_existing_data(self):
        response = self.client.get(
            reverse("main:update_achievement", args=[self.achievement.id])
        )
        self.assertContains(response, self.achievement.title)
        self.assertContains(response, self.achievement.issuer)

    def test_update_achievement_post_valid_correct_password(self):
        response = self.client.post(
            reverse("main:update_achievement", args=[self.achievement.id]),
            self._valid_payload(title="Updated Title"),
        )
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "Updated Title")
        self.assertRedirects(response, reverse("main:show_achievement"))

    def test_update_achievement_post_wrong_password(self):
        response = self.client.post(
            reverse("main:update_achievement", args=[self.achievement.id]),
            self._valid_payload(title="Should Not Update", password="wrong-secret"),
        )
        self.achievement.refresh_from_db()
        self.assertNotEqual(self.achievement.title, "Should Not Update")
        self.assertEqual(response.status_code, 200)  # form dirender ulang, tidak redirect

    def test_update_nonexistent_achievement_returns_404(self):
        fake_id = uuid.uuid4()
        response = self.client.get(
            reverse("main:update_achievement", args=[fake_id])
        )
        self.assertEqual(response.status_code, 404)

    def test_edit_link_appears_on_achievement_page(self):
        response = self.client.get(reverse("main:show_achievement"))
        expected_url = reverse("main:update_achievement", args=[self.achievement.id])
        self.assertContains(response, f'href="{expected_url}"')