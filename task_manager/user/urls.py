from django.urls import path
from task_manager.user import views

app_name = 'user'

urlpatterns = [
    path('', views.IndexView.as_view(), name='user_index'),
    path('create/', views.UserCreate.as_view(), name='user_create'),
]
