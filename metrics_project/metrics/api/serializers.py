from rest_framework import serializers
from metrics.models import Info, Category
from rest_framework.decorators import authentication_classes, permission_classes
import json


# --- INFORMATION ---
class InfoListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset = Category.objects.all())
    time = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M%p', '%I:%M %p'])

    class Meta:
        model = Info
        fields = ('id','category','tags','value','date','time')


class InfoPostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name',
                                            queryset = Category.objects.all())
    tags = serializers.CharField(required=False,allow_blank= True,)
    time = serializers.TimeField(format='%I:%M %p', input_formats=['%I:%M%p', '%I:%M %p'])

    class Meta:
        model = Info
        fields = ('category','tags','value','date','time')

    def __init__(self, *args, **kwargs):
        super(InfoPostSerializer, self).__init__(*args, **kwargs)

        available_categories = ', '.join([category for category in Category.objects.values_list('name', flat=True)])
        if len(available_categories.split(',')) > 1:
            self.fields['category'].error_messages['does_not_exist'] =  'The category doesn\'t exists. Available categories: ' + available_categories
        else:
            self.fields['category'].error_messages['does_not_exist'] =  'No categories available'


    def validate_tags(self, value):
        if value.find(',') != -1:
            for tag in value.split(','):
                if tag == '' or tag ==' ':
                    raise serializers.ValidationError('Can\'t have an empty element as a tag!')
        return value


# --- CATEGORY ---
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]


class CategoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name',]
