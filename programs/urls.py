from django.urls import path


from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
