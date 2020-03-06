from django.db.models import Q
from rest_framework import generics, mixins

from metrics.models import Info, Category, string_to_list
from .serializers import *
from rest_framework import serializers
from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError
import json
from django import forms



class TagsFieldFilter(filters.Filter):
    def filter(self, qs, value):
        if value:
            filtered_ids = []
            for query in qs:
                if all(tag in query.tags for tag in string_to_list(value)):
                    filtered_ids.append(query.id)
            qs = Info.objects.filter(id__in=filtered_ids)
        return qs

class InfoFilter(filters.FilterSet):
    category = filters.ModelChoiceFilter(field_name='category', to_field_name='name', queryset=Category.objects.all())
    tags = TagsFieldFilter(label='Tags')
    date = filters.DateFromToRangeFilter(field_name='date', label='Date')
    time = filters.TimeRangeFilter(field_name='time', label='Time')

    class Meta:
        model = Info
        fields = ('date','time','category','tags')


# --- INFORMATION ---
class InfoListView(generics.ListAPIView):
    queryset = Info.objects.all().order_by('date','time')
    serializer_class = InfoListSerializer
    filterset_class = InfoFilter

class InfoPostView(generics.CreateAPIView):
    serializer_class = InfoPostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class InfoRudView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InfoPostSerializer

    def get_queryset(self):
        return Info.objects.all()

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

# --- CATEGORY ---
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class CategoryPostView(generics.CreateAPIView):
    serializer_class = CategoryPostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class CategoryRudView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryPostSerializer

    def get_queryset(self):
        return Category.objects.all()
