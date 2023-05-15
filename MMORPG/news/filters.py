from django_filters import FilterSet, ChoiceFilter
from .models import Comment
from django import forms


class ProfileFilter(FilterSet):
    class Meta:
        model = Comment
        fields = ('accepted',)