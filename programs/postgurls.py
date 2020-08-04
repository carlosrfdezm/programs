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
    path('lines/', views.lines, name='lines'),
    path('line/<int:line_id>/projects', views.postg_by_line_projects_list, name='line_projects'),



    path('ajx/students/by/phd_programs', views.ajx_postg_phd_students_by_program, name='ajx_postg_phd_students_by_program'),
    path('ajx/students/by/msc_programs', views.ajx_postg_msc_students_by_program, name='ajx_postg_msc_students_by_program'),
    path('ajx/students/by/dip_programs', views.ajx_postg_dip_students_by_program, name='ajx_postg_dip_students_by_program'),
    path('ajx/<str:program_slug>/members/by/grade', views.ajx_members_by_grade, name='ajx_postg_program_members_by_grade'),
    path('ajx/<str:program_slug>/students/by/line', views.ajx_students_by_line, name='ajx_postg_program_students_by_line'),
    path('ajx/<str:program_slug>/students/by/edition', views.ajx_students_by_edition, name='ajx_postg_program_students_by_edition'),
    path('ajx/<str:program_slug>/students/by/gender', views.ajx_students_by_gender, name='ajx_postg_program_students_by_gender'),
    path('ajx/<str:program_slug>/students/by/age', views.ajx_students_by_age, name='ajx_postg_program_students_by_age'),
    path('ajx/<str:program_slug>/graduated/by/edition', views.ajx_graduated_by_edition, name='ajx_postg_program_graduated_by_edition'),







    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
