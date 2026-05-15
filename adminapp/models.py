from django.db import models
from django.contrib.auth.models import User  # Importing built-in User model
from django.utils import timezone
from django.contrib.auth import get_user_model

class WishList(models.Model):
    product_name = models.CharField(max_length=255)  # Product name
    modified_date = models.DateTimeField(auto_now=True)  # Auto updates on modification
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to User model
    is_flipkart_lower = models.IntegerField(default=0)  # 1 = Flipkart has lower price, 0 = No
    status = models.CharField(max_length=50)  # Status field
    lowest_price = models.FloatField()  # Lowest price among platforms

User = get_user_model()

class Notification(models.Model):
    # Notification types
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SUCCESS = 'success'
    NOTIFICATION_TYPES = [
        (INFO, 'Information'),
        (WARNING, 'Warning'),
        (ERROR, 'Error'),
        (SUCCESS, 'Success'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=10,
        choices=NOTIFICATION_TYPES,
        default=INFO
    )
    is_read = models.BooleanField(default=False)  # Add this field
    created_date = models.DateTimeField(default=timezone.now)
    url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.user.username} - {self.message[:50]}..."

    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save()

