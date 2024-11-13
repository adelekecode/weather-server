from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions, authentication
from drf_yasg.views import get_schema_view
from drf_yasg import openapi 
from drf_yasg.generators import OpenAPISchemaGenerator
from django.http import JsonResponse




def welcome(request):

    return JsonResponse(
        {
            "status": 200,
            "message": "Welcome, wetin you dey find "
        }
    )




schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version="v1",
        description="API",
        terms_of_service="",
        contact=openapi.Contact(email="oluwafemiadeleke13@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(authentication.BasicAuthentication,),
)



urlpatterns = [
    # path('', welcome),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('v1/', include('accounts.urls')),
]
