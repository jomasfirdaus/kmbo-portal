from django.urls import path

from . import views_jeral
from .import views_rejistuuzuariu
from . import views
from .views import set_language
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [  
  
    path('home/', views_jeral.home, name="home"),
    path('', views_jeral.dashboardkmbo, name="dashboardkmbo"),
    path('set_language/', set_language, name='set_language'),
    path('dashboard/', views_rejistuuzuariu.main, name="main"),
    path('kmbokudaulun/', views_jeral.dashboard, name="kmbokudaulun"),
    path('informasaun/', views_jeral.master, name="info"),
    path('main/logout/', views_jeral.logout, name="logout"),
    path('main/perfil/', views_rejistuuzuariu.perfil, name="perfil"),
    path('main/updatepassword/', views_rejistuuzuariu.update_password, name="updatepassword"),
    path('main/updatedadus/', views_rejistuuzuariu.updatedadus, name="updatedadus"),
    path('main/uzuariu/', views_rejistuuzuariu.uzuariu, name="uzuariu"),
    path('main/uzuariu/rejistu/', views_rejistuuzuariu.rejistuuzuariu, name="rejistuuzuariu"),
    path('main/uzuariu/hamos/<int:id>', views_rejistuuzuariu.hamosuzuariu, name="hamosuzuariu"),
    path('main/', views_rejistuuzuariu.login, name="login"),
   
]


