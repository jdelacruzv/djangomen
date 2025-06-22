from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('', views.post_list, name='post_list'),
	path('post/<int:pk>/', views.post_detail, name='post_detail'),
	path('post/new/', views.post_new, name='post_new'),
	path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
	path('drafts/', views.post_draft_list, name='post_draft_list'),
	path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
	path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
  path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
  path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
  path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
  # Rutas para el flujo de restablecimiento de contraseña
  path('password_reset/', 
    auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
  path('password_reset/done/', 
    auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
  path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
  path('reset/done/', 
    auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'
  ),
]