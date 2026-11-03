import uuid

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Achievement

def make_users():
    owner = User.objects.create_superuser("owner", "o@example.com", "pw-test")
    editor = User.objects.create_user("editor", password="pw-test")
    editor.user_permissions.add(Permission.objects.get(codename="change_achievement"))
    regular = User.objects.create_user("regular", password="pw-test")
    return owner, editor, regular

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
        self.assertEqual(self.client.get("/halaman-yang-tidak-ada/").status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, "Part-Time")  # filter pill
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_experience_data_in_json(self):
        response = self.client.get(reverse("main:get_experiences_json"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, '"is_ongoing": true')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:get_experiences_json"))
        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, '"is_ongoing": false')


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
        self.assertContains(response, "National")  # filter pill

    def test_achievement_data_in_json(self):
        response = self.client.get(reverse("main:get_achievements_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "application/json")
        self.assertContains(response, self.achievement.title)
        self.assertContains(response, self.achievement.issuer)
        self.assertContains(response, self.achievement.description)

    def test_empty_achievement_page(self):
        Achievement.objects.all().delete()
        response = self.client.get(reverse("main:show_achievement"))
        self.assertContains(response, "Belum ada penghargaan yang ditambahkan.")

    def test_filter_by_level_in_json(self):
        Achievement.objects.create(
            title="Regional Robotics Competition",
            issuer="Dinas Pendidikan",
            description="Juara di kompetisi robotika tingkat regional.",
            level="regional",
            date_achieved="2022-05-01",
        )
        response = self.client.get(
            reverse("main:get_achievements_json"), {"level": "national"}
        )
        self.assertContains(response, self.achievement.title)
        self.assertNotContains(response, "Regional Robotics Competition")


class AchievementCreateDeleteTest(TestCase):
    def setUp(self):
        self.owner, self.editor, self.regular = make_users()
        self.payload = {
            "title": "Test Achievement", "issuer": "Test Issuer",
            "description": "Test desc", "level": "school",
            "date_achieved": "2026-01-01", "certificate_url": "",
        }

    def test_create_ajax_by_superuser(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("main:create_achievement_ajax"), self.payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Achievement.objects.count(), 1)

    def test_create_ajax_invalid_returns_400(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("main:create_achievement_ajax"), {**self.payload, "title": ""}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Achievement.objects.count(), 0)

    def test_create_ajax_forbidden_for_non_superuser(self):
        for user in (self.regular, self.editor):
            self.client.force_login(user)
            response = self.client.post(reverse("main:create_achievement_ajax"), self.payload)
            self.assertEqual(response.status_code, 403)
        self.assertEqual(Achievement.objects.count(), 0)

    def test_delete_by_superuser(self):
        achievement = Achievement.objects.create(
            title="To Delete", issuer="X", description="Y",
            level="school", date_achieved="2026-01-01",
        )
        self.client.force_login(self.owner)
        self.client.post(reverse("main:delete_achievement", args=[achievement.id]))
        self.assertEqual(Achievement.objects.count(), 0)

    def test_delete_blocked_for_non_superuser(self):
        achievement = Achievement.objects.create(
            title="Not Deleted", issuer="X", description="Y",
            level="school", date_achieved="2026-01-01",
        )
        for user in (None, self.regular, self.editor):
            if user:
                self.client.force_login(user)
            self.client.post(reverse("main:delete_achievement", args=[achievement.id]))
        self.assertEqual(Achievement.objects.count(), 1)


class AchievementUpdateTest(TestCase):
    def setUp(self):
        self.owner, self.editor, self.regular = make_users()
        self.achievement = Achievement.objects.create(
            title="KIHAJAR STEM 2023", issuer="Kemendikbudristek",
            description="Penghargaan atas proyek SIPELAN.",
            level="national", date_achieved="2023-10-01",
        )
        self.url = reverse("main:update_achievement", args=[self.achievement.id])

    def _payload(self, **overrides):
        payload = {
            "title": self.achievement.title, "issuer": self.achievement.issuer,
            "description": self.achievement.description, "level": self.achievement.level,
            "date_achieved": "2023-10-01", "certificate_url": "",
        }
        payload.update(overrides)
        return payload

    def test_guest_is_redirected_to_login(self):
        self.assertEqual(self.client.get(self.url).status_code, 302)

    def test_regular_user_forbidden(self):
        self.client.force_login(self.regular)
        self.assertEqual(self.client.get(self.url).status_code, 403)
        self.client.post(self.url, self._payload(title="Hacked"))
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "KIHAJAR STEM 2023")

    def test_editor_can_open_prefilled_form(self):
        self.client.force_login(self.editor)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievement_form.html")
        self.assertContains(response, self.achievement.title)
        self.assertContains(response, self.achievement.issuer)

    def test_editor_can_update(self):
        self.client.force_login(self.editor)
        response = self.client.post(self.url, self._payload(title="Updated Title"))
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "Updated Title")
        self.assertRedirects(response, reverse("main:show_achievement"))

    def test_update_nonexistent_returns_404(self):
        self.client.force_login(self.editor)
        url = reverse("main:update_achievement", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_edit_button_enabled_for_editor_only(self):
        self.client.force_login(self.editor)
        response = self.client.get(reverse("main:show_achievement"))
        self.assertContains(response, 'const CAN_EDIT = "true" === "true"')
        self.client.force_login(self.regular)
        response = self.client.get(reverse("main:show_achievement"))
        self.assertContains(response, 'const CAN_EDIT = "false" === "true"')


class ExperienceViewTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Backend Intern", description="Worked on API development",
            category="internship",
        )

    def test_show_experience_uses_correct_template(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

    def test_experience_data_in_json(self):
        response = self.client.get(reverse("main:get_experiences_json"))
        self.assertContains(response, "Backend Intern")

    def test_empty_state_shown_when_no_experience(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))
        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")