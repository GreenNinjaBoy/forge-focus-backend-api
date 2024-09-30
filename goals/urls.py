from django.urls import path
from goals import views


urlpatterns = [
    path('goals/', views.GoalsList.as_view(), name='goal-list'),
    path('goals/<int:pk>/', views.GoalsDetail.as_view(), name='goal-detail'),
    path('goals/<int:pk>/delete/', views.GoalsDetail.as_view(),
         name='goal-delete'),
]
