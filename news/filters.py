import django_filters
from django_filters import FilterSet, ModelMultipleChoiceFilter
from .models import Post, Category
from django.forms import DateInput
from django import forms


class PostFilter(FilterSet):

    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='gte',
                                        widget=DateInput(attrs={'type': 'date'}), label='Дата (позже)')
    category = ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                        widget=forms.CheckboxSelectMultiple(
                                                            attrs={'category': 'category'}), label='Категория')

    class Meta:
        model = Post

        fields = {
            'title': ['icontains'],
            'author': ['exact']

        }

