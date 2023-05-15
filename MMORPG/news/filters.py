from django_filters import FilterSet
from .models import Comment


class ProfileFilter(FilterSet):
    class Meta:
        model = Comment
        fields = ('accepted',)
