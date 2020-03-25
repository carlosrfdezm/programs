from django.urls import path


from . import views

app_name = 'log'

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.mylogin, name='my_login'),
    path('<str:program_slug>/logout', views.mylogout, name='my_logout'),
    path('cgc/member/<int:member_id>/pic', views.cgc_member_picture, name='cgc_member_picture'),

]
