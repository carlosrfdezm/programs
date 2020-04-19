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

    path('students/<str:scope>', views.students_list, name='students_list')





    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
