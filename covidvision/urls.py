# covidvision URL Configuration
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from detection.views import upload_image, check_covid_api, get_csrf_token

urlpatterns = [
    path('', upload_image, name='upload_image'),
    path('api/csrf_token/', get_csrf_token, name='get_csrf_token'),
    path("api/covid", check_covid_api, name="check_covid_api"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



