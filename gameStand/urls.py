"""gameStand URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from gameSite import views
from django.views.generic import RedirectView
# import registration.backends.default.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.login),
    path('logout/', views.logout),
    path('userinfo/', views.userinfo),
    path('<int:pid>/<str:del_pass>', views.index),
    path('list/', views.listing),
    path('income/', views.income, name='income_create'),
    path('income_list/', views.income_list, name='income_list'),
    path('income_create/', views.income_create, name='income_create'),
    path('income/<pk>/update/', views.income_update, name='income_update'),
    path('income/<pk>/delete/', views.income_delete, name='income_delete'),
    path('post/', views.posting),
    path('contact/', views.contact),
    path('email/', views.email),
    path('line/', views.line),
    path('ELK/', views.ELK),            
    path('post2db/', views.post2db),
    path('', RedirectView.as_view(url='/userinfo/', permanent=True)),   #檢視網站-> 'index/'
    # django-registration
    path('accounts/', include('registration.backends.default.urls')),
]
