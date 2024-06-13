from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name='home'),
    path('login',views.login,name='login'),
    path('register',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('submit_contact_form',views.contact_form_submission,name='submit_contact_form'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('admin_dashboard/user/<int:user_id>/',views.user_services, name='user_services'),
    path('admin_dashboard/service/<int:service_id>/update/',views.update_service_status, name='update_service_status'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)