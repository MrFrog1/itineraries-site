from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)  # For itinerary questions that have been answered

    # Generic foreign key to associate this message with an Itinerary or ItineraryGroup
    # This where we can connect to any one of the models and then the ID connects to any instance of those model;s
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
                                       

    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    read = models.BooleanField(default=False)


    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"
    

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)


# PUT THE FOLLOWING INTO THE VIEWS OR API ENDPOINTS

# from django.http import HttpResponseForbidden

# def get_user_messages(request):
#     if not request.user.is_authenticated:
#         return HttpResponseForbidden("You must be logged in to view messages.")

#     messages = Message.objects.filter(recipient=request.user)
#     # Process and return the messages
    

# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse, HttpResponseForbidden
# from .models import User, Message, Notification

# def send_message(request, recipient_id):
#     if request.method == 'POST' and request.user.is_authenticated:
#         recipient = get_object_or_404(User, pk=recipient_id)
#         content = request.POST.get('content')

#         # Create the message
#         message = Message.objects.create(
#             sender=request.user,
#             recipient=recipient,
#             content=content
#         )

#         # Create a notification for the recipient
#         Notification.objects.create(
#             user=recipient,
#             message=message
#         )

#         return HttpResponse('Message sent')
#     else:
#         return HttpResponseForbidden('Invalid request or not authenticated')