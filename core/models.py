from django.db import models
from django.contrib.auth.models import User

class Report(models.Model):
    STATUS_CHOICES = [
        ('Reported', 'Reported'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]

    TYPE_CHOICES = [
        ('Issue', 'Issue'),
        ('Lost', 'Lost'),
        ('Found', 'Found'),
    ]

    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='reports/', blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Reported')

    admin_reply = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report_type