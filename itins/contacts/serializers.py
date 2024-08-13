
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
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=ContactCategory.objects.all(), required=False)
    business = serializers.PrimaryKeyRelatedField(queryset=ContactBusiness.objects.all(), required=False, allow_null=True)
    photos = DetailedPhotoSerializer(many=True, read_only=True, source='contact_photos')

    class Meta:
        model = Contact
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user:
            if request.user.is_staff or request.user == instance.agent:
                return rep
            elif instance.is_visible_to_others:
                return rep
        return None  # Return None if the contact should not be visible

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        business_data = validated_data.pop('business', None)

        contact = Contact.objects.create(**validated_data)

        for category in categories_data:
            if isinstance(category, ContactCategory):
                contact.categories.add(category)
            else:
                category_obj, _ = ContactCategory.objects.get_or_create(agent=contact.agent, **category)
                contact.categories.add(category_obj)

        if business_data:
            if isinstance(business_data, ContactBusiness):
                contact.business = business_data
            else:
                business, _ = ContactBusiness.objects.get_or_create(agent=contact.agent, **business_data)
                contact.business = business

        contact.save()
        return contact

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', None)
        business_data = validated_data.pop('business', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if categories_data is not None:
            instance.categories.clear()
            for category in categories_data:
                if isinstance(category, ContactCategory):
                    instance.categories.add(category)
                else:
                    category_obj, _ = ContactCategory.objects.get_or_create(agent=instance.agent, **category)
                    instance.categories.add(category_obj)

        if business_data is not None:
            if isinstance(business_data, ContactBusiness):
                instance.business = business_data
            else:
                if instance.business:
                    for attr, value in business_data.items():
                        setattr(instance.business, attr, value)
                    instance.business.save()
                else:
                    business, _ = ContactBusiness.objects.get_or_create(agent=instance.agent, **business_data)
                    instance.business = business

        instance.save()
        return instance