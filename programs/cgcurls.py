from django.urls import path


from . import views
from . import cgc_views as views

app_name = 'programs'

urlpatterns = [


    #URLS DE CGC
    path('home', views.cgc_home, name='cgc_home'),
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

    path('brieffings/create', views.create_cgc_brief, name='create_cgc_brief'),
    path('brieffings/cngc/create', views.create_cngc_brief, name='create_cngc_brief'),
    path('brieffings/cngc/list', views.cngc_brieffings, name='cngc_brieffings'),
    path('brieffings/cngc/<int:brief_id>/view', views.cngc_brief_view, name='cngc_brief_view'),
    path('brieffings/cngc/<int:brief_id>/edit', views.edit_cngc_brief, name='edit_cngc_brief'),
    path('brieffings/cngc/year/<int:year>/list', views.cngc_year_brieffings, name='cngc_year_brieffings'),
    path('brieffings/<int:year>/list', views.cgc_year_brieffings, name='cgc_year_brieffings'),
    path('brieffings/list', views.cgc_brieffings, name='cgc_brieffings'),
    path('brieffings/<int:brief_id>/view', views.cgc_brief_view, name='cgc_brief_view'),
    path('brieffings/<int:brief_id>/edit', views.edit_cgc_brief, name='edit_cgc_brief'),

    path('students/<str:scope>', views.students_list, name='students_list'),
    path('lines/list', views.programs_lines, name='programs_lines'),
    path('projects/list', views.programs_projects, name='programs_projects'),


    path('members/<str:scope>', views.programs_members_list, name='programs_members_list'),

    path('programs/list', views.cgc_programs_list, name='cgc_programs_list'),
    path('program/<str:program_slug>/students/<str:scope>/list', views.program_students_list, name='program_students_list'),
    path('program/<str:program_slug>/members/list', views.program_members_list, name='program_members_list'),
    path('program/<str:program_slug>/statistics', views.cgc_program_statistics, name='cgc_program_statistics'),

    path('statistics', views.cgc_statistics,name='cgc_statistics'),






    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
