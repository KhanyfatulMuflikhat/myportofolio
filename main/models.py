import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateField(default=timezone.now)
    ended_at = models.DateTimeField(blank=True, null=True)
    starred_by = models.ManyToManyField(
        User, related_name="starred_experiences", blank=True
    )
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Achievement(models.Model):
    LEVEL_CHOICES = [
        ('school', 'School'),
        ('regional', 'Regional'),
        ('national', 'National'),
        ('international', 'International'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    issuer = models.CharField(max_length=255)
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='school')
    date_achieved = models.DateField()
    certificate_url = models.URLField(blank=True, null=True)
    starred_by = models.ManyToManyField(
        User, related_name="starred_achievements", blank=True
    )

    def __str__(self):
        return self.title