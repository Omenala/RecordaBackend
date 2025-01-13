from django.urls import path
from . import views
from .views import GlobalSearchView


urlpatterns = [
    path('global-search/', GlobalSearchView.as_view(), name='GlobalSearchView'),
]