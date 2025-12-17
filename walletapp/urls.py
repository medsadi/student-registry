from django.urls import path
from . import views

app_name = 'blockchain'

urlpatterns = [
    path('', views.home, name='home'),
    path('admin_diploma/', views.admin_diploma, name='admin_diploma'),
    path('add_student_admin/', views.add_student_admin, name='add_student_admin'),
    path('mint_diploma/', views.mint_diploma, name='mint_diploma'),
    path('view_diploma/<int:student_id>/', views.view_diploma, name='view_diploma'),
    path('diploma_metadata/<int:student_id>/', views.diploma_metadata_api, name='diploma_metadata_api'),
    path('portfolio/', views.student_portfolio, name='student_portfolio'),
]
