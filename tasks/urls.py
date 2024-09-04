from django.urls import path
from tasks import views

urlpatterns = [
    path('tasks/', views.TasksList.as_view()),
    path('tasks/<int:pk>', views.UserTasksDetails.as_view(),)
]