
from rest_framework import serializers
from .models import Contact, ContactCategory, ContactBusiness
from media.serializers import DetailedPhotoSerializer
class ContactCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactCategory
        fields = '__all__'

class ContactBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactBusiness
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    category = ContactCategorySerializer()
    business = ContactBusinessSerializer()
    photos = DetailedPhotoSerializer(many=True, read_only=True, source='contact_photos')  # Ensure the source matches the related_name in Photo model

    class Meta:
        model = Contact
        fields = '__all__'
        depth = 1  # Adjust the depth as necessary


    def create(self, validated_data):
        category_data = validated_data.pop('category')
        business_data = validated_data.pop('business')

        category, _ = ContactCategory.objects.get_or_create(**category_data)
        business, _ = ContactBusiness.objects.get_or_create(**business_data)

        contact = Contact.objects.create(category=category, business=business, **validated_data)
        return contact

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        business_data = validated_data.pop('business')

        # Update basic fields of Contact
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Check if a ContactCategory with the given data exists, or create a new one
        category, _ = ContactCategory.objects.update_or_create(
            defaults=category_data, 
            agent=instance.agent,  # Assuming the agent remains constant
            name=category_data.get('name', instance.category.name)
        )
        instance.category = category

        # Check if a ContactBusiness with the given data exists, or create a new one
        business, _ = ContactBusiness.objects.update_or_create(
            defaults=business_data, 
            agent=instance.agent,  # Assuming the agent remains constant
            business_name=business_data.get('business_name', instance.business.business_name)
        )
        instance.business = business

        instance.save()
        return instance 