"""raterproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from raterapi.views import register_user, login_user
from raterapi.views import GameView
from raterapi.views import ReviewView
from raterapi.views import RateView
from raterapi.views import GamePictureView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'reviews', ReviewView, 'review')
router.register(r'rates', RateView, 'rate')
router.register(r'gamepictures', GamePictureView, 'gamepicture')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
    path('', include('raterreports.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
