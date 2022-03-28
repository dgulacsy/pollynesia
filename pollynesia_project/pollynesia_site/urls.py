from django.urls import path

from . import views

app_name = 'pollynesia_site'
urlpatterns = [
    path('', views.LandingPage.as_view(), name='landing_page'),
]