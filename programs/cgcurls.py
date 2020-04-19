from django.urls import path


from . import views
from . import cgc as views

app_name = 'programs'

urlpatterns = [


    #URLS DE CGC
    path('home', views.cgc_home, name='cgc_home'),
    path('ajx/recent/requests', views.ajx_cgc_this_year_requests, name='ajx_cgc_this_year_requests'),





    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
