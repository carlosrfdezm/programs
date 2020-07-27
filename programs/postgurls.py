from django.urls import path


from . import views
from . import postg_views as views

app_name = 'programs'

urlpatterns = [


    #URLS DE POSTG
    path('', views.index, name='postg_index'),
    path('home', views.home, name='postg_home'),







    # path('login', views.mylogin, name='my_login'),
    # path('logout/<str:court_slug>/', views.mylogout, name='my_logout'),
    # path('cngc/member/<int:member_id>/pic', views.cngc_member_picture, name='cngc_member_picture'),

]
