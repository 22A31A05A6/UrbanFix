from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.report_issue, name='report_issue'),
    path('complaints/', views.my_complaints, name='my_complaints'),
    path('complaints/<int:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/complaints/<int:complaint_id>/', views.admin_complaint_detail, name='admin_complaint_detail'),
]
