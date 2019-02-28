"""pol_harvester URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from pol_harvester import views


api_urlpatterns = [
    url(r'^document/(?P<pk>\d+)/content/$', views.DocumentContentView.as_view(), name="document-content"),
    url(r'^document/(?P<pk>\d+)/$', views.DocumentView.as_view(), name="document"),
    url(r'^collection/(?P<pk>\d+)/content/$', views.CollectionContentView.as_view(), name="collection-content"),
    url(r'^collection/(?P<pk>\d+)/$', views.CollectionView.as_view(), name="collection"),
    url(r'^freeze/(?P<pk>\d+)/content/$', views.FreezeContentView.as_view(), name="freeze-content"),
    url(
        r'^freeze/(?P<pk>\d+)/annotate/(?P<annotation_name>[A-Za-z0-9\-_]+)/$',
        views.AnnotationView.as_view(),
        name="freeze-annotation"
    ),
    url(r'^freeze/(?P<pk>\d+)/$', views.FreezeView.as_view(), name="freeze"),
]


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(api_urlpatterns, namespace="api-v1")),
]
