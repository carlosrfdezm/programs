from django.urls import path


from . import views
from . import cgc_views as cgc_views

app_name = 'programs'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('background/<int:background_id>', views.program_background, name='program_background'),
    #Path de estudiantes de doctorados, excepto la lista
    path('students/create', views.create_student, name='create_student'),
    path('students/list/<str:scope>', views.students_list, name='students_list'),
    path('students/<int:student_id>/edit', views.edit_student, name='edit_student'),
    path('students/<int:student_id>/picture', views.program_student_picture, name='program_student_picture'),
    #Paths de estudiantes de maestria
    path('msc/<int:edition_id>/students/create', views.create_msc_student, name='create_msc_student'),
    path('msc/<int:edition_id>/students/<int:student_id>/edit', views.edit_msc_student, name='edit_msc_student'),
    path('msc/edition/<int:edition_id>/students/<str:scope>/list', views.msc_edition_students_list, name='msc_edition_students_list'),
    path('msc/students/<str:scope>/list', views.msc_all_students_list, name='msc_all_students_list'),

    path('professors/create', views.create_professor, name='create_professor'),
    path('professors/<int:member_id>/edit', views.edit_member, name='edit_member'),
    path('professors/<int:member_id>/picture', views.program_member_picture, name='program_member_picture'),
    path('professors/<str:scope>/list', views.members_list, name='members_list'),

    path('lines/create', views.create_line, name='create_line'),
    path('lines/list', views.program_lines, name='program_lines'),
    path('lines/<int:line_id>/students', views.students_by_line, name='students_by_line'),
    path('lines/<int:line_id>/edit', views.edit_line, name='edit_line'),

    path('projects/create', views.create_project, name='create_project'),
    path('projects/<int:project_id>/edit', views.edit_project, name='edit_project'),
    path('projects/list', views.projects_list, name='projects_list'),

    path('editions/create',views.create_program_edition, name='create_program_edition'),
    path('editions/list',views.editions_list, name='editions_list'),
    path('editions/<int:edition_id>/edit',views.edit_program_edition, name='edit_program_edition'),


    path('ajx/user/exists', views.ajx_usr_exists, name='ajx_usr_exists'),
    path('ajx/member/exists', views.ajx_program_member_tuthor, name='ajx_program_member_tuthor'),
    path('ajx/student/delete', views.ajx_delete_student, name='ajx_delete_student'),
    path('ajx/member/delete', views.ajx_delete_member, name='ajx_delete_member'),
    path('ajx/tuthor/delete', views.ajx_delete_tuthor, name='ajx_delete_tuthor'),
    path('ajx/student/<int:student_id>/tuthor/create', views.ajx_create_tuthor, name='ajx_create_tuthor'),
    path('ajx/line/delete', views.ajx_delete_line, name='ajx_delete_line'),
    path('ajx/project/delete', views.ajx_delete_project, name='ajx_delete_project'),
    path('ajx/statistics/thisyear/requests', views.ajx_this_year_requests, name='ajx_this_year_requests'),
    path('ajx/statistics/byyear/requests', views.ajx_by_year_requests, name='ajx_by_year_requests'),
    path('ajx/statistics/lastyear/requests', views.ajx_last_years_requests, name='ajx_last_years_requests'),
    path('ajx/statistics/students/status', views.ajx_students_by_state, name='ajx_students_by_state'),
    path('ajx/statistics/students/gender', views.ajx_students_by_sex, name='ajx_students_by_sex'),
    path('ajx/statistics/students/line', views.ajx_students_by_line, name='ajx_students_by_line'),
    path('ajx/statistics/students/age', views.ajx_students_by_age, name='ajx_students_by_age'),
    path('ajx/statistics/students/editions', views.ajx_students_by_edition, name='ajx_students_by_edition'),
    path('ajx/statistics/students/graduated/editions', views.ajx_graduated_by_edition, name='ajx_graduated_by_edition'),
    path('ajx/statistics/members/degree', views.ajx_members_by_grade, name='ajx_members_by_grade'),
    path('ajx/statistics/members/age', views.ajx_members_by_age, name='ajx_members_by_age'),
    path('ajx/messages/members/personal', views.ajx_member_personal_msg, name='ajx_member_personal_msg'),
    path('ajx/messages/members/massive', views.ajx_member_massive_msg, name='ajx_member_massive_msg'),
    path('ajx/messages/students/personal', views.ajx_student_personal_msg, name='ajx_student_personal_msg'),
    path('ajx/messages/students/massive', views.ajx_students_massive_msg, name='ajx_students_massive_msg'),
    path('ajx/messages/everybody/massive', views.ajx_everybody_massive_msg, name='ajx_everybody_massive_msg'),


    path('statistics', views.program_statistics, name='program_statistics'),


    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
