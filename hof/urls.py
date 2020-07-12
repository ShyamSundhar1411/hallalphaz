from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from halls import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name = 'home'),
    path('dashboard',views.dashboard,name = 'dashboard'),
    path('signup',views.Signup.as_view(),name = 'signup'),
    path('login',auth_views.LoginView.as_view(),name = 'login'),
    path('logout',auth_views.LogoutView.as_view(),name = 'logout'),
    path('halloffames/create',views.Create.as_view(),name = 'create'),
    path('halloffames/<int:pk>',views.Detail.as_view(),name = 'detail'),
    path('halloffames/<int:pk>/delete',views.Delete.as_view(),name = 'delete'),
    path('halloffames/<int:pk>/update',views.Update.as_view(),name = 'update'),
    path('halloffames/<int:pk>/addvid',views.video,name = 'video'),
    path('video/search',views.video_search,name = 'video_search'),
    path('video/<int:pk>/delete',views.DelVid.as_view(),name = 'delvid')
]+static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)
