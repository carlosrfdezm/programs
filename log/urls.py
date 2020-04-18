from django.urls import path


from . import views

app_name = 'log'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.mylogin, name='my_login'),
    path('cgc/login', views.cgc_login, name='cgc_login'),
    path('cgc/home', views.cgc_home, name='cgc_home'),
    path('cgc/logout', views.cgc_logout, name='cgc_logout'),
    path('<str:program_slug>/logout', views.mylogout, name='my_logout'),
    path('cgc/member/<int:member_id>/pic', views.cgc_member_picture, name='cgc_member_picture'),

]
