from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('jobs/', views.jobs, name='jobs'),
    path('materials/', views.materials, name='materials'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('create_post/', views.create_post, name='create_post'),
    path('save_job/<int:job_id>/', views.save_job, name='save_job'),
    path('save_material/<int:material_id>/', views.save_material, name='save_material'),
    path('search/', views.search_posts, name='search_posts'),
    path('profile/<str:username>/', views.profile, name='profile'),
]