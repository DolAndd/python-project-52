from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.StatusIndexView.as_view(), name='status_index'),

]