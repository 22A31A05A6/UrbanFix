from django.db import models
from django.contrib.auth.models import User


class Complaint(models.Model):
    ISSUE_TYPES = [
        ('Garbage', 'Garbage'),
        ('Poor Hygiene', 'Poor Hygiene'),
        ('Drainage', 'Drainage'),
        ('Road Damage', 'Road Damage'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
    description = models.TextField()
    image = models.ImageField(upload_to='complaint_images/', blank=True, null=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_update = models.TextField(blank=True)
    resolved_image = models.ImageField(upload_to='resolved/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.issue_type} - {self.user.username}'
