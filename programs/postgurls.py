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



    path('ajx/students/by/phd_programs', views.ajx_postg_phd_students_by_program, name='ajx_postg_phd_students_by_program'),
    path('ajx/students/by/msc_programs', views.ajx_postg_msc_students_by_program, name='ajx_postg_msc_students_by_program'),
    path('ajx/students/by/dip_programs', views.ajx_postg_dip_students_by_program, name='ajx_postg_dip_students_by_program'),







    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
