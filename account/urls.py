from django.urls import path

from . import views


# this is for resetting the password
from django.contrib.auth import views as auth_views


urlpatterns=[
    
    path("register", views.register, name='register'),

    # email-verification
    path("email-verification/<str:uidb64>/<str:token>", views.email_verification, name='email-verification'),

    # #email-verification-sent
     path("email-verification-sent", views.email_verification_sent, name='email-verification-sent'),
     
     # #email-verification-failed
     path("email-verification-failed", views.email_verification_failed, name='email-verification-failed'),

     # #email-verification-success
     path("email-verification-success", views.email_verification_success, name='email-verification-success'),

    # login and logout urls
    path('my-login', views.my_login, name='my-login'),

    path('user-logout', views.user_logout, name='user-logout'),

    # dashboard and profile maangement
    path('dashboard', views.dashboard, name='dashboard'),

    path("profile-manage", views.profile_manage, name='profile-manage'),

    path("delete-account", views.delete_account, name='delete-account'),

    path('track-order', views.track_order, name='track-order'),



    # password management urls/views
    # ayushjain1139@gmail.com

    # 1:) submit email form
    path("reset_password", auth_views.PasswordResetView.as_view(template_name="account/password/password-reset.html"), name="password_reset"),

    # success message stating that password reset message is send
    path("reset_password_sent", auth_views.PasswordResetDoneView.as_view(template_name="account/password/password-reset-sent.html"), name="password_reset_done"),

    # password rest link
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="account/password/password-reset-form.html"), name="password_reset_confirm"),

    # Success Message stating that our password is reset successfully
    path("reset_password_complete", auth_views.PasswordResetCompleteView.as_view(template_name="account/password/password-reset-complete.html"), name="password_reset_complete"),

    # shipping management
    path('manage-shipping', views.manage_shipping, name='manage-shipping'),



]
