from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TasksViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('tasks-list/', views.TasksList.as_view(), name='tasks-list'),
]