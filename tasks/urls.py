from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register the TasksViewSet
router = DefaultRouter()
router.register(r'tasks', views.TasksViewSet, basename='task')

# Define the URL patterns for the tasks app
urlpatterns = [
    path('', include(router.urls)),
    path('tasks-list/', views.TasksList.as_view(), name='tasks-list'),
    path('tasks/<int:pk>/toggle-complete/', views.TasksViewSet.as_view(
        {'patch': 'toggle_complete'}), name='task-toggle-complete'),
    path('tasks/<int:pk>/reuse/', views.TasksViewSet.as_view(
        {'post': 'reuse'}), name='task-reuse'),
    path('tasks/<int:pk>/reset/', views.TasksViewSet.as_view(
        {'patch': 'reset'}), name='task-reset'),
]
