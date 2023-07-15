from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request: any) -> HttpResponse:
    return HttpResponse('Hello World !') 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
] 