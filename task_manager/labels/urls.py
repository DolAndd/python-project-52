from django.urls import path

from task_manager.labels import views

urlpatterns = [
    path('', views.LabelsIndexView.as_view(), name='label_index'),
    path('create/', views.LabelsCreateView.as_view(), name='label_create'),
    path('<int:pk>/update/', views.LabelsUpdateView.as_view(),
         name='label_update'),
    path('<int:pk>/delete/', views.LabelsDeleteView.as_view(),
         name='label_delete'),
]
