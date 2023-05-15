from django.urls import path
from .views import NewsList, NewsDetail, Search, NewsAdd, NewsUpgrade, NewsDelete, Accept, Cans, UserView

urlpatterns = [
    path('', NewsList.as_view(), name='index'),
    path('<int:pk>', NewsDetail.as_view(), name='news'),
    path('search/', Search.as_view(), name='search_results'),
    path('add/', NewsAdd.as_view(), name='add'),
    path('<int:pk>/edit', NewsUpgrade.as_view(), name='edit'),
    path('<int:pk>/delete', NewsDelete.as_view(), name='delete'),
    path('profile/', UserView.as_view(), name='profile'),
    path('accept/<int:pk>/', Accept.as_view(), name='accept'),
    path('cancel/<int:pk>/', Cans.as_view(), name='cancel'),

]
