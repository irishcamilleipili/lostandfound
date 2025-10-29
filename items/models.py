from django.db import models
from django.utils import timezone

class Item(models.Model):
    CATEGORY_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Claimed', 'Claimed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='found')
    location = models.CharField(max_length=200)
    date_reported = models.DateTimeField(default=timezone.now)
    contact_info = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='item_images/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        ordering = ['-date_reported']

    def __str__(self):
        return f"{self.title} ({self.category}) - {self.status}"
