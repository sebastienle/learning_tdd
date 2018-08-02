"""tdd_01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

from lists.views import home_page, list_view, new_list, add_item

urlpatterns = [
    url(r'^$', home_page, name='home'),
    #url(r'^lists/the-only-list-in-the-world/$', list_view, name='list_view'),
    url(r'^lists/(\d+)/$', list_view, name='list_view'),
    url(r'^lists/new$', new_list, name='new_list'),
    url(r'^lists/(\d+)/add$', add_item, name='add_item'),
    url(r'^admin/', include(admin.site.urls)),
]
