from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import root_route, open_debug_view, logout_route

urlpatterns = [
    path('', root_route),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  # Login button for restframework CRUD
    path('dj-rest-auth/', include('dj_rest_auth.urls')), # Frontend uses this
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')), # Frontend uses this
    path('accounts/', include('django.contrib.auth.urls')),
    path('open-debug/', open_debug_view, name='open-debug-view'),
    path('', include('goals.urls')),
    path('', include('tasks.urls')),
    path('', include('contact.urls')),
]
