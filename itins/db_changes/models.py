from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DbChange(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    changed_model = models.CharField(max_length=100, default=None)  # To store the model name that was changed

    def __str__(self):
        return f"Change by {self.user.username} on {self.timestamp}"