from django.db import models

class Email(models.Model):
    class PriorityChoices(models.TextChoices):
        HIGH = 'HIGH', 'High'
        MEDIUM = 'MEDIUM', 'Medium'
        LOW = 'LOW', 'Low'

    email_id = models.CharField(max_length=255, unique=True)
    sender = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_important = models.BooleanField(default=False, db_index=True)
    priority = models.CharField(
        max_length=10,
        choices=PriorityChoices.choices,
        default=PriorityChoices.LOW,
    )
    category = models.CharField(max_length=100, blank=True)
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.subject} from {self.sender}"

class Configuration(models.Model):
    key = models.CharField(max_length=50, unique=True)
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

