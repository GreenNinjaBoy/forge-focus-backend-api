from django.urls import path
from contact import views

urlpatterns = [
    path('contact/', views.ContactCreate.as_view(), name='contact-create'),
    path('contact/list/', views.ContactListView.as_view(), name='contact-list'),
]