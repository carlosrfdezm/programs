from django.urls import path


from . import views
from . import cgc_views as views

app_name = 'programs'

urlpatterns = [


    #URLS DE CGC
    path('', views.cgc_index, name='cgc_index'),
    path('home', views.cgc_home, name='cgc_home'),
    path('members/create', views.cgc_create_cgc_member, name='cgc_create_cgc_member'),
    path('members/list', views.cgc_members_list, name='cgc_members_list'),
    path('members/<int:member_id>/edit', views.cgc_edit_member, name='cgc_edit_member'),
    path('members/<int:member_id>/profile/view', views.view_cgc_member_profile, name='view_cgc_member_profile'),
    path('members/self/profile/view', views.view_self_profile, name='view_self_profile'),
    path('members/profile/edit', views.autoedit_member_profile, name='autoedit_member_profile'),

    path('ajx/recent/requests', views.ajx_cgc_this_year_requests, name='ajx_cgc_this_year_requests'),
    path('ajx/recent/years/req_vs_grad', views.ajx_last_years_requests_vs_graduated, name='ajx_last_years_requests_vs_graduated'),
    path('ajx/students/state', views.ajx_students_by_state, name='ajx_students_by_state'),
    path('ajx/program/<str:program_slug>/students/by_gender', views.ajx_program_students_by_sex, name='ajx_program_students_by_sex'),
    path('ajx/program/<str:program_slug>/students/by_line', views.ajx_program_students_by_line, name='ajx_program_students_by_line'),
    path('ajx/program/<str:program_slug>/students/by_age', views.ajx_program_students_by_age, name='ajx_program_students_by_age'),
    path('ajx/brieffing/delete', views.ajx_delete_cgc_brieffing, name='ajx_delete_cgc_brieffing'),
    path('ajx/cngc/brieffing/delete', views.ajx_delete_cngc_brieffing, name='ajx_delete_cngc_brieffing'),
    path('ajx/program/<str:program_slug>/req_vs_init', views.ajx_program_this_year_requests, name='ajx_program_this_year_requests'),
    path('ajx/program/<str:program_slug>/by_year_req', views.ajx_program_by_year_requests, name='ajx_program_by_year_requests'),
    path('ajx/program/<str:program_slug>/last_year_req', views.ajx_program_last_years_requests, name='ajx_program_last_years_requests'),
    path('ajx/program/<str:program_slug>/members/by_grade', views.ajx_program_members_by_grade, name='ajx_program_members_by_grade'),
    path('ajx/program/<str:program_slug>/members/by_age', views.ajx_program_members_by_age, name='ajx_program_members_by_age'),
    path('ajx/cgc/last_year_requests', views.ajx_cgc_last_years_requests, name='ajx_cgc_last_years_requests'),
    path('ajx/cgc/by_year_requests', views.ajx_cgc_by_year_requests, name='ajx_cgc_by_year_requests'),
    path('ajx/cgc/students_by_gender', views.ajx_cgc_students_by_gender, name='ajx_cgc_students_by_gender'),
    path('ajx/cgc/students_by_line', views.ajx_cgc_students_by_line, name='ajx_cgc_students_by_line'),
    path('ajx/cgc/students_by_age', views.ajx_cgc_students_by_age, name='ajx_cgc_students_by_age'),
    path('ajx/cgc/students_by_program', views.ajx_cgc_students_by_program, name='ajx_cgc_students_by_program'),
    path('ajx/cgc/members_by_grade', views.ajx_cgc_program_members_by_grade, name='ajx_cgc_program_members_by_grade'),
    path('ajx/cgc/members_by_age', views.ajx_cgc_program_members_by_age, name='ajx_cgc_program_members_by_age'),
    path('ajx/cgc/members_massive_message', views.ajx_cgc_member_massive_msg, name='ajx_cgc_member_massive_msg'),
    path('ajx/cgc/students_massive_message', views.ajx_cgc_students_massive_msg, name='ajx_cgc_students_massive_msg'),
    path('ajx/cgc/all_massive_message', views.ajx_cgc_everybody_massive_msg, name='ajx_cgc_everybody_massive_msg'),
    path('ajx/member/exists', views.ajx_cgc_usr_exists, name='ajx_cgc_usr_exists'),
    path('ajx/member/delete', views.ajx_cgc_delete_member, name='ajx_cgc_delete_member'),
    path('ajx/document/delete', views.ajx_delete_document, name='ajx_delete_document'),
    path('ajx/user/exists', views.ajx_usr_exists, name='ajx_usr_exists'),

    path('brieffings/create', views.create_cgc_brief, name='create_cgc_brief'),
    path('brieffings/download', views.cgc_brief_zip_download, name='cgc_brief_zip_download'),
    path('brieffings/cngc/create', views.create_cngc_brief, name='create_cngc_brief'),
    path('brieffings/cngc/list', views.cngc_brieffings, name='cngc_brieffings'),
    path('brieffings/cngc/download', views.cngc_brief_zip_download, name='cngc_brief_zip_download'),
    path('brieffings/cngc/<int:brief_id>/view', views.cngc_brief_view, name='cngc_brief_view'),
    path('brieffings/cngc/<int:brief_id>/edit', views.edit_cngc_brief, name='edit_cngc_brief'),
    path('brieffings/cngc/year/<int:year>/list', views.cngc_year_brieffings, name='cngc_year_brieffings'),
    path('brieffings/cngc/year/<int:year>/download', views.cngc_by_year_brief_zip_download, name='cngc_by_year_brief_zip_download'),
    path('brieffings/<int:year>/list', views.cgc_year_brieffings, name='cgc_year_brieffings'),
    path('brieffings/<int:year>/download', views.cgc_by_year_brief_zip_download, name='cgc_by_year_brief_zip_download'),
    path('brieffings/list', views.cgc_brieffings, name='cgc_brieffings'),
    path('brieffings/<int:brief_id>/view', views.cgc_brief_view, name='cgc_brief_view'),
    path('brieffings/<int:brief_id>/edit', views.edit_cgc_brief, name='edit_cgc_brief'),

    path('documents/create', views.cgc_new_document, name='cgc_new_document'),
    path('documents/list/<str:scope>', views.cgc_documents, name='documents'),
    path('documents/<int:document_id>/view', views.cgc_document_view, name='view_document'),
    path('documents/<int:document_id>/edit', views.cgc_edit_document, name='edit_document'),


    path('students/<str:scope>', views.students_list, name='students_list'),
    path('lines/list', views.programs_lines, name='programs_lines'),
    path('lines/<int:line_id>/students/list', views.cgc_line_students_list, name='cgc_line_students_list'),
    path('lines/<int:line_id>/projects/list', views.cgc_by_line_projects_list, name='cgc_by_line_projects_list'),
    path('projects/list', views.programs_projects, name='programs_projects'),
    path('projects/<int:project_id>/students/list', views.cgc_project_students_list, name='cgc_project_students_list'),


    path('programs/members/<str:scope>', views.programs_members_list, name='programs_members_list'),
    path('programs/list', views.cgc_programs_list, name='cgc_programs_list'),
    path('program/<str:program_slug>/students/<str:scope>/list', views.program_students_list, name='program_students_list'),
    path('program/<str:program_slug>/members/list', views.program_members_list, name='program_members_list'),
    path('program/<str:program_slug>/statistics', views.cgc_program_statistics, name='cgc_program_statistics'),

    path('statistics', views.cgc_statistics,name='cgc_statistics'),
    path('report', views.docx_cgc_report,name='docx_cgc_report'),






    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
