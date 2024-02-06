from django.shortcuts import render
from .models import Contact, ContactBusiness, ContactCategory
from .serializers import ContactSerializer, ContactBusinessSerializer, ContactCategorySerializer
from rest_framework import viewsets
from .permissions import IsOwnerOrAdmin

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsOwnerOrAdmin]


class ContactCategoryViewSet(viewsets.ModelViewSet):
    queryset = ContactCategory.objects.all()
    serializer_class = ContactCategorySerializer

class ContactBusinessViewSet(viewsets.ModelViewSet):
    queryset = ContactBusiness.objects.all()
    serializer_class = ContactBusinessSerializer
    permission_classes = [IsOwnerOrAdmin]
