from django.urls import path


from . import views
from . import postg_views as views

app_name = 'programs'

urlpatterns = [


    #URLS DE POSTG
    path('', views.index, name='postg_index'),
    path('logout', views.logout, name='postg_logout'),
    path('home', views.home, name='postg_home'),
    path('programs/<str:program_type>', views.programs, name='programs'),
    path('<str:program_slug>/students/<str:scope>', views.program_students, name='program_students'),
    path('<str:program_slug>/members/<str:scope>', views.program_members, name='program_members'),
    path('<str:program_slug>/statistics', views.program_statistics, name='program_statistics'),
    path('members/', views.members, name='members'),
    path('member/create', views.create_postg_member, name='create_postg_member'),
    path('member/<int:member_id>/picture', views.postg_member_picture, name='postg_member_picture'),
    path('member/<int:member_id>/edit', views.edit_postg_member, name='edit_postg_member'),
    path('lines/', views.lines, name='lines'),
    path('line/<int:line_id>/projects', views.postg_by_line_projects_list, name='line_projects'),
    path('document/create', views.postg_new_document, name='new_document'),
    path('document/<int:document_id>/edit', views.postg_edit_document, name='edit_document'),
    path('document/<int:document_id>/view', views.postg_document_view, name='view_document'),
    path('document/public/<int:document_id>/view', views.postg_public_document_view, name='view_public_document'),
    path('documents/<str:scope>', views.postg_documents, name='documents'),
    path('reports/<str:scope>', views.docx_postg_report, name='reports'),


    path('ajx/user/exists',views.ajx_postg_usr_exists, name='ajx_postg_usr_exists'),
    path('ajx/students/by/phd_programs', views.ajx_postg_phd_students_by_program, name='ajx_postg_phd_students_by_program'),
    path('ajx/students/by/msc_programs', views.ajx_postg_msc_students_by_program, name='ajx_postg_msc_students_by_program'),
    path('ajx/students/by/dip_programs', views.ajx_postg_dip_students_by_program, name='ajx_postg_dip_students_by_program'),
    path('ajx/<str:program_slug>/members/by/grade', views.ajx_members_by_grade, name='ajx_postg_program_members_by_grade'),
    path('ajx/<str:program_slug>/students/by/line', views.ajx_students_by_line, name='ajx_postg_program_students_by_line'),
    path('ajx/<str:program_slug>/students/by/edition', views.ajx_students_by_edition, name='ajx_postg_program_students_by_edition'),
    path('ajx/<str:program_slug>/students/by/gender', views.ajx_students_by_gender, name='ajx_postg_program_students_by_gender'),
    path('ajx/<str:program_slug>/students/by/age', views.ajx_students_by_age, name='ajx_postg_program_students_by_age'),
    path('ajx/<str:program_slug>/graduated/by/edition', views.ajx_graduated_by_edition, name='ajx_postg_program_graduated_by_edition'),
    path('ajx/<str:program_slug>/requests/', views.ajx_postg_program_last_years_requests, name='ajx_postg_program_last_years_requests'),
    path('ajx/<str:program_slug>/by/year/requests/', views.ajx_postg_program_by_year_requests, name='ajx_postg_program_by_years_requests'),
    path('ajx/member/delete', views.ajx_delete_member, name='ajx_delete_member'),
    path('ajx/document/delete', views.ajx_delete_document, name='ajx_delete_document'),


    path('faq/<int:faq_id>/read', views.read_faq, name='read_faq'),
    path('faq/<int:faq_id>/edit', views.edit_faq, name='edit_faq'),
    path('faq/create', views.create_faq, name='create_faq'),
    path('faq/list', views.faq_list, name='faq_list'),

    path('faq/delete/<int:faq_id>/', views.ajx_delete_faq, name='ajx_delete_faq'),


]
