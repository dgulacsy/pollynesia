from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('user/<str:username>', views.UserIndexView.as_view(), name='user-polls'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('new/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/update', views.UpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.DeleteView.as_view(), name='delete'),
    path('<int:poll_id>/vote/', views.vote, name='vote'),
]