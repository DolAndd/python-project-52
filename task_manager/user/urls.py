from django.urls import path
from task_manager.user import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='user_index'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
