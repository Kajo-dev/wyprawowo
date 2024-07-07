from user_manager import views as user_manager_views
from django.urls import path
urlpatterns = [
        path('register', user_manager_views.register_page, name='register_page'),
        path('login', user_manager_views.login_page, name='login_page'),
        path('logout', user_manager_views.logout_page, name='logout_page'),
        path('activate/<uidb64>/<token>', user_manager_views.activate, name='activate_account'),
    ]