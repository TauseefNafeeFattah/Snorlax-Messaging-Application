from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.signup, name="signup"),
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html", success_url=reverse_lazy('accounts:password_reset_done'), email_template_name='accounts/password_reset_email.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html", success_url=reverse_lazy('accounts:password_reset_complete')), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_complete"),
]
