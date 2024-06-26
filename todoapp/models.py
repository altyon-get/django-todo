from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    LOW = 'L'
    HIGH = 'H'
    MEDIUM = 'M'
    PRIORITY_CHOICES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
