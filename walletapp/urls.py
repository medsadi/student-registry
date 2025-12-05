from django.urls import path
from . import views

app_name = 'blockchain'

urlpatterns = [
    # Page d'accueil (ancien système)
    path('', views.home, name='home'),
    
    # Administration des diplômes NFT
    path('admin/diploma/', views.admin_diploma, name='admin_diploma'),
    path('admin/add-student/', views.add_student_admin, name='add_student_admin'),
    path('admin/mint-diploma/', views.mint_diploma, name='mint_diploma'),
    path('admin/diploma/<int:student_id>/', views.view_diploma, name='view_diploma'),
    
    # Portfolio étudiant
    path('student/portfolio/', views.student_portfolio, name='student_portfolio'),
]