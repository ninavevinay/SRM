from django.contrib import admin
from django.urls import path
from resultapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('admin-login/', admin_login, name='admin_login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('create_class/', create_class, name='create_class'),
    path('create_subject/', create_subject, name='create_subject'),
    path('manage_subject/', manage_subject, name='manage_subject'),
    path('admin_logout/', admin_logout, name='admin_logout'),
    path('manage_classes/', manage_classes, name='manage_classes'),
    path('edit_class/<int:class_id>', edit_class, name='edit_class'),
    path('edit_subject/<int:subject_id>', edit_subject, name='edit_subject'),
    path('add_subject_combination/', add_subject_combination, name='add_subject_combination'),
    path('manage_subject_combination/', manage_subject_combination, name='manage_subject_combination'),
    path('add_student/', add_student, name='add_student'),
    path('manage_student/', manage_student, name='manage_student'),
    path('edit_student/<int:student_id>', edit_student, name='edit_student'),
    path('add_notice/', add_notice, name='add_notice'),
    path('manage_notice/', manage_notice, name='manage_notice'),
    path('edit_notice/<int:notice_id>', edit_notice, name='edit_notice'),
    path('add_result/', add_result, name='add_result'),
    path('get_student_subjects/',get_student_subjects,name='get_student_subjects/'),
    path('manage_result/', manage_result, name='manage_result'),
    path("edit-result/<int:student_id>/",edit_result, name="edit_result"),
    path('change_password/', change_password, name='change_password'),
    path('search_result/',search_result, name='search_result'),
    path('check_result/',check_result, name='check_result'),
    path('notice_detail/<int:notice_id>/',notice_detail, name='notice_detail'),


    
]
