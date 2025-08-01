"""
URL configuration for renovators project.

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
from general.views import ImportantLinksListView
from technical_information.views import SyntheticEventsListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tools/', include('general.urls')),
    path('api/important-links/', ImportantLinksListView.as_view(), name='important-links'),
    path('api/testing-accounts/', include('technical_information.urls')),
    path('api/synthetic-events/', SyntheticEventsListView.as_view(), name='synthetic-events'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
