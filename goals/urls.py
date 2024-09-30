from django.urls import path
from goals import views
from .views import serve_cloudinary_image

urlpatterns = [
    path('goals/', views.GoalsList.as_view(), name='goal-list'),
    path('goals/<int:pk>/', views.GoalsDetail.as_view(), name='goal-detail'),
    path('goals/<int:pk>/delete/', views.GoalsDetail.as_view(),
         name='goal-delete'),
    path('media/<path:path>', serve_cloudinary_image, name='serve_cloudinary_image'),
]
