from django.urls import path


from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('students/create', views.create_student, name='create_student'),
    path('students/list/<str:scope>', views.students_list, name='students_list'),
    path('students/<int:student_id>/edit', views.edit_student, name='edit_student'),
    path('professors/create', views.create_professor, name='create_professor'),
    path('professors/<int:member_id>/edit', views.edit_member, name='edit_member'),
    path('professors/<str:scope>/list', views.members_list, name='members_list'),


    path('ajx/user/exists', views.ajx_usr_exists, name='ajx_usr_exists'),


    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
