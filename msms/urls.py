"""msms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from lessons import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('profile/', views.profile, name='profile'),
    path('password/', views.password, name='password'),
    path('log_out/', views.log_out, name='log_out'),

    path('administrator/lessons', views.admin_lessons, name='admin_lessons'),
    path('administrator/lessons/<int:lesson_id>', views.admin_lesson, name="admin_lesson"),
    path('administrator/delete_lesson/<int:lesson_id>', views.admin_lesson_delete, name='admin_lesson_delete'),
    path('administrator/approved_requests', views.admin_approved_requests, name='admin_approved_requests'),
    path('administrator/unapproved_requests', views.admin_unapproved_requests, name='admin_unapproved_requests'),
    path('administrator/delete_request/<int:request_id>', views.admin_request_delete, name='admin_request_delete'),
    path('administrator/requests/<int:request_id>', views.admin_request, name='admin_request'),
    path('administrator/manage_students', views.manage_students, name='manage_students'),
    path('administrator/delete_user/<int:user_id>', views.manage_user_delete, name='manage_user_delete'),
    path('administrator/change_balance/<int:user_id>', views.change_balance, name='change_balance'),

    path('director/create_admin', views.create_admin, name='create_admin'),
    path('director/manage_admins', views.manage_admins, name='manage_admins'),
    path('delete_account/<int:account_id>', views.delete_account, name='delete_account'),
    path('edit_account/<int:account_id>', views.edit_account, name='edit_account'),

    path('administrator/term/create', views.term_create, name='term_create'),
    path('administrator/term/update/<int:term_id>', views.term_update, name='term_update'),
    path('administrator/term/delete/<int:term_id>', views.term_delete, name='term_delete'),

    path('student/requests', views.student_requests, name='student_requests'),
    path('requests/create', views.student_request_create, name='student_request_create'),
    path('requests/<int:request_id>', views.student_request_update, name='student_request_update'),
    path('delete_request/<int:request_id>', views.student_request_delete, name='student_request_delete'),
    path('student/lessons', views.student_lessons, name='student_lessons'),
    path('student/add_child', views.add_child, name='add_child'),

    path('transaction_history/', views.transaction_history, name='transaction_history'),
]

