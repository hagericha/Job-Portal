"""
URL configuration for jobsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from jobs import views as jobs_views


urlpatterns = [
    path('admin/', admin.site.urls),

     # root home page — job list
    path('', jobs_views.job_list, name='home'), 

    path('accounts/', include('accounts.urls')),
    path('jobs/', include('jobs.urls')),  # homepage -> jobs.job_list
]


# append static/media URL only after urlpatterns exists
# 2️⃣ Only after urlpatterns exists, append static/media URLs
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)