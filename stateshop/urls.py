"""stateshop URL Configuration

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
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from state import views

urlpatterns = [
    url(r'^samikeadmin/',include(admin.site.urls)),
    url(r'^$',views.index, name='index'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^state/about/$', views.about, name='about'),
    url(r'^state/add_category/$', views.add_category, name ='add_category'),
    url(r'^state/category/(?P<category_name_slug>[\w\-]+)/(?P<pk>\d+)/add_product/$', views.add_product, name ='add_product'),
    url(r'^state/product_detail_view/(?P<id>\d+)/$', views.product_detail_view, name='product_detail_view'),
    url(r'^state/product_delete/(?P<id>\d+)/$', views.product_delete, name='product_delelte'),
    url(r'^state/search/$', views.search),
    url(r'^state/contact/$', views.contact),
     url(r'^state/delete_product_success/$', views.delete_product_success, name="delete_product_success"),
    url(r'^state/profile/(?P<pk>\d+)/$', views.profile, name= 'profile'),
    url(r'^state/product_added/$', views.add_sucess, name ='add_sucess'),
    url(r'^state/email_sent/$', views.email_success, name ='email_success'),
    url(r'^state/delete/(?P<pk>\d+)/$', views.account_delete, name='account_delete'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'session_security/', include('session_security.urls')),
    ]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)