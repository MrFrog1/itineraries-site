from django.db import models
from django.conf import settings

class ForumCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ForumTopic(models.Model):
    category = models.ForeignKey(ForumCategory, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='topics', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class ForumPost(models.Model):
    topic = models.ForeignKey(ForumTopic, related_name='posts', on_delete=models.CASCADE)
    message = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post in {self.topic.title} by {self.created_by.user.username}"

# Optional Model for Pinned Topics
class PinnedTopic(models.Model):
    topic = models.OneToOneField(ForumTopic, on_delete=models.CASCADE)

    def __str__(self):
        return f"Pinned: {self.topic.title}"