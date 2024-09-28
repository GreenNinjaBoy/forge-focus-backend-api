from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings  

@api_view()
@permission_classes([AllowAny])
def root_route(request):
    return Response({
        'message': "Welcome to the Forge Focus API"
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def open_debug_view(request):
    return Response({
        'message': 'Debug view accessible',
        'user': str(request.user),
        'auth': str(request.auth),
        'is_authenticated': request.user.is_authenticated,
        'headers': dict(request.headers),
    })
    
@api_view(['POST'])
def logout_route(request):
    response = Response()
    response.set_cookie(
        key=settings.JWT_AUTH_COOKIE,  
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=settings.JWT_AUTH_SAMESITE,  
        secure=settings.JWT_AUTH_SECURE,  
    )
    response.set_cookie(
        key=settings.JWT_AUTH_REFRESH_COOKIE,  
        value='',
        httponly=True,
        expires='Thu, 01 Jan 1970 00:00:00 GMT',
        max_age=0,
        samesite=settings.JWT_AUTH_SAMESITE,  
        secure=settings.JWT_AUTH_SECURE,  
    )
    return response