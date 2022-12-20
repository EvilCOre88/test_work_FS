"""test_work_FS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from mailing_management.views import MailingListViewSet, MailingListDetailViewSet, ClientViewSet, MessageViewSet, MessageDetailViewSet, send_mail#, SendMailViewSet

router = DefaultRouter()
router.register('mailing-lists', MailingListViewSet)
router.register('mailing-lists-details', MailingListDetailViewSet, basename='mailing-lists-details')
router.register('clients', ClientViewSet)
router.register('messages', MessageViewSet, basename= 'messages')
router.register('message-detail', MessageDetailViewSet)
# # router.register('send', SendMailViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/send/', send_mail),
    # path('api/messages/', MessageViewSet.as_view({'get': 'list'})),
    # path('api/messages/<pk>/', MessageViewSet.as_view({'get': 'retrieve'})),
    path('api/', include(router.urls))
]
