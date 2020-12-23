from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from komax import views as komax_views

admin.site.site_header = "ADMINISTRATOR PAGE"
admin.site.site_title = "T-TECH ACCOUNTING"
admin.site.index_title = "Welcome to ADMIN PAGE"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('komax/', include('komax.urls')),
    path('foiling/', include('foiling.urls')),
    path('acct/', include('acct.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='komax/login.html'), name='login'),
    path('logout/', komax_views.Logout, name='logout'),
    path('auth/', komax_views.autho, name='auth'),
    path('check_group/', komax_views.check_group, name='check_group'),
]