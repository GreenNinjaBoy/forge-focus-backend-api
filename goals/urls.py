from django.urls import path
from goals import views

urlpatterns = [
    path('goals/', views.GoalsList.as_view()),
    path('goals/<int:pk>', views.GoalsListl.as_view()),
]