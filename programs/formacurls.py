from django.urls import path, include


from . import views
from . import formac_views as views
from .formac_views import ajx_students_by_center, program_statistics

app_name = 'programs'

urlpatterns = [


    #URLS DE POSTG
    path('', views.index, name='formac_index'),
    path('logout', views.logout, name='formac_logout'),
    path('home', views.home, name='formac_home'),
    path('programs/<str:program_type>', views.programs, name='programs'),
    path('<str:program_slug>/students/<str:scope>', views.program_students, name='program_students'),
    path('<str:program_slug>/members/<str:scope>', views.program_members, name='program_members'),
    path('<str:program_slug>/statistics', views.program_statistics, name='program_statistics'),
    path('members/', views.members, name='members'),
    path('member/create', views.create_formac_member, name='create_formac_member'),
    path('member/<int:member_id>/picture', views.formac_member_picture, name='formac_member_picture'),
    path('member/<int:member_id>/edit', views.edit_formac_member, name='edit_formac_member'),
    path('lines/', views.lines, name='lines'),
    #path('line/<int:line_id>/projects', views.formac_by_line_projects_list, name='line_projects'),
    path('document/create', views.formac_new_document, name='new_document'),
    path('document/<int:document_id>/edit', views.formac_edit_document, name='edit_document'),
    path('document/<int:document_id>/view', views.formac_document_view, name='view_document'),
    path('document/public/<int:document_id>/view', views.formac_public_document_view, name='view_public_document'),
    path('documents/<str:scope>', views.formac_documents, name='documents'),
    path('reports/<str:scope>', views.docx_formac_report, name='reports'),


    path('ajx/user/exists',views.ajx_formac_usr_exists, name='ajx_formac_usr_exists'),
    path('ajx/students/by/curs_programs', views.ajx_formac_curs_students_by_program, name='ajx_formac_curs_students_by_program'),
    path('ajx/students/by/coleg_programs', views.ajx_formac_coleg_students_by_program, name='ajx_formac_coleg_students_by_program'),
    path('ajx/<str:program_slug>/members/by/grade', views.ajx_members_by_grade, name='ajx_formac_program_members_by_grade'),
    path('ajx/<str:program_slug>/students/by/edition', views.ajx_students_by_edition, name='ajx_formac_program_students_by_edition'),
    path('ajx/<str:program_slug>/students/by/gender', views.ajx_students_by_gender, name='ajx_formac_program_students_by_gender'),
    path('ajx/<str:program_slug>/students/by/age', views.ajx_students_by_age, name='ajx_formac_program_students_by_age'),
    path('ajx/<str:program_slug>/graduated/by/edition', views.ajx_graduated_by_edition, name='ajx_formac_program_graduated_by_edition'),
    path('ajx/<str:program_slug>/requests/', views.ajx_formac_program_last_years_requests, name='ajx_formac_program_last_years_requests'),
    path('ajx/<str:program_slug>/by/year/requests/', views.ajx_formac_program_by_year_requests, name='ajx_formac_program_by_years_requests'),
    path('ajx/member/delete', views.ajx_delete_member, name='ajx_delete_member'),
    path('ajx/document/delete', views.ajx_delete_document, name='ajx_delete_document'),

    
    path('<str:program_slug>/statistics/', program_statistics, name='program_statistics'),
    path('ajax/stats/students-by-center/<slug:program_slug>/', ajx_students_by_center, name='ajx_students_by_center'),
    # ... otras URLs específicas de formac ...

    path('faq/<int:faq_id>/read', views.read_faq, name='read_faq'),
    path('faq/<int:faq_id>/edit', views.edit_faq, name='edit_faq'),
    path('faq/create', views.create_faq, name='create_faq'),
    path('faq/list', views.faq_list, name='faq_list'),

    path('faq/delete/<int:faq_id>/', views.ajx_delete_faq, name='ajx_delete_faq'),
    path('new/delete/<int:new_id>/', views.ajx_delete_new, name='ajx_delete_new'),
    #path('ajx/new/delete', views.ajx_delete_new, name='ajx_delete_new'),
    #path('formac/', include(('programs.formacurls', 'formac'), namespace='formac')),

    #path('new/<int:new_id>/picture', views.program_new_picture, name='new_img'),
    path('new/<int:new_id>/read', views.read_new, name='read_new'),
    path('new/<int:new_id>/edit', views.edit_new, name='edit_new'),
    path('new/create', views.create_new, name='create_new'),
    path('news/list', views.news_list, name='news_list'),

]
