from django.urls import path
from .api import *
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('create_report',create_report,name='report.create'),
    path('create_ads',create_ads,name='create.ads'),
    path('get_publc_ads',get_ads,name='get.ads'),
    path('api/reports/', reports_api, name='reports_api'),
    # path('api/nearest-centers/', nearest_centers_api, name='nearest_centers_api'),


    path('',index,name='index'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('users/', user_list, name='user_list'),
    path('users/add/', add_user, name='add_user'),
    path('users/<int:pk>/edit/', edit_user, name='edit_user'),
    path('users/<int:pk>/delete/', delete_user, name='delete_user'),
    path('users/<int:pk>/toggle/', toggle_user_status, name='toggle_user'),
    path('ads/', ads_list, name='ads_list'),
    path('ads/add/', add_ad, name='add_ad'),
    path('ads/<int:pk>/edit/', edit_ad, name='edit_ad'),
    path('ads/<int:pk>/delete/', delete_ad, name='delete_ad'),
    path('reports',reports_list,name='report_list'),
    path('reports/<int:pk>/', report_detail, name='report_detail'),
    path('reports/<int:pk>/update-status/<int:new_status>/', update_report_status, name='update_report_status'),
    path('report/map',map_reports,name='map_reports'),
    path('dashboard/admin',admin_dashboard,name='admin_dashboard'),
    path('dashboard/subadmin',authority_dashboard,name='subadmin_dashboard'),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register',register_user),
    path('me',me),
    path('fetch_my_reports',get_my_reports),
    path('delete_report/<int:id>',delete_report),
    path('centers/', center_list, name='center_list'),
    path('centers/create/', create_emergency_center, name='create_emergency_center'),
    path('centers/<int:center_id>/edit/', edit_emergency_center, name='edit_emergency_center'),
    path('centers/<int:center_id>/delete/', delete_emergency_center, name='delete_emergency_center'),
    path('emergency-centers/', emergency_centers_map, name='emergency_centers_map'),
        path('center/reports/', center_reports, name='center_reports'),
        path('center/reports/<int:pk>/', center_report_detail, name='center_report_detail'),
path('center/reports/<int:pk>/update-status/', center_update_report_status, name='center_update_report_status'),
path('dashboard/subadmin/', center_dashboard, name='center_dashboard'),

]