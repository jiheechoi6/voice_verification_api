"""VoiceVerifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view 
from drf_yasg import openapi
from VoiceVerifier.views.streams import HttpStreamViewSet
from VoiceVerifier.views.verifier import VerifierViewSet

schema_url_patterns = [ 
    path('admin/', admin.site.urls),
    path('vv/enroll', VerifierViewSet.as_view({
        "post": "enroll"
    })),
    path('vv/verify', VerifierViewSet.as_view({
        "post": "verify"
    })),
    path('vv/get_voiceprint/<str:id>', VerifierViewSet.as_view({
        "get": "get_voiceprint"
    })),
    path('vv/list_enrollments', VerifierViewSet.as_view({
        "get": "list_enrollments"
    })),
    path('vv/delete_all_enrollment', VerifierViewSet.as_view({
        "delete": "delete_all_enrollment"
    })),
    path('vv/delete_enrollment/<str:id>', VerifierViewSet.as_view({
        "delete": "delete_enrollment"
    })),
    path('start_stream', HttpStreamViewSet.as_view({
        "post": "start_stream"
    })),
    path('upload_stream_data/<str:uuid>', HttpStreamViewSet.as_view({
        "post": "upload_stream_data"
    })),
    path('get_all_streams', HttpStreamViewSet.as_view({
        "get": "get_all_streams"
    })),
]

schema_view = get_schema_view( 
    openapi.Info( title="Django API", 
        default_version='v1', 
        terms_of_service="https://www.google.com/policies/terms/", 
        ), 
        public=True, 
        permission_classes=(permissions.AllowAny,), 

        patterns=schema_url_patterns, 
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vv/enroll', VerifierViewSet.as_view({
        "post": "enroll"
    })),
    path('vv/verify', VerifierViewSet.as_view({
        "post": "verify"
    })),
    path('vv/delete_all_enrollment', VerifierViewSet.as_view({
        "delete": "delete_all_enrollment"
    })),
    path('vv/delete_enrollment/<str:id>', VerifierViewSet.as_view({
        "delete": "delete_enrollment"
    })),
    path('vv/get_voiceprint/<str:id>', VerifierViewSet.as_view({
        "get": "get_voiceprint"
    })),
    path('vv/list_enrollments', VerifierViewSet.as_view({
        "get": "list_enrollments"
    })),
    path('start_stream', HttpStreamViewSet.as_view({  ####
        "post": "start_stream"
    })),
    path('upload_stream_data/<str:uuid>', HttpStreamViewSet.as_view({
        "post": "upload_stream_data"
    })),
    path('get_all_streams', HttpStreamViewSet.as_view({
        "get": "get_all_streams"
    })),
    # path('http_stream/')
    
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), 
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
