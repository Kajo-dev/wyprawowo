from user_manager import views as user_manager_views
from django.views.generic import TemplateView
from django.urls import path

urlpatterns = [
        path('register', user_manager_views.register_page, name='register_page'),
        path('login', user_manager_views.login_page, name='login_page'),
        path('logout', user_manager_views.logout_page, name='logout_page'),
        path('activate/<uidb64>/<token>', user_manager_views.activate, name='activate_account'),
        path('polityka-prywatnosci/', user_manager_views.policy_privacy, name="policy_privacy"),
        path('regulamin/', user_manager_views.policy_rules, name="policy_rules"),
        path('pytania/<int:question_id>/', user_manager_views.question_view, name="question_view"),
        path('oplata-rejestracyjna', user_manager_views.ini_payment, name="ini_payment_view"),
        path('test/', user_manager_views.test_register, name="test_register"),
    ]