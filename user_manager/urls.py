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
        path('profile/<slug:slug>/', user_manager_views.profile_view, name='profile_view'),
        path('profile/<int:profile_id>/like/', user_manager_views.like_profile, name='like_profile'),
        path('profile/<int:profile_id>/unlike/', user_manager_views.unlike_profile, name='unlike_profile'),
        path('post/<int:post_id>/like/', user_manager_views.like_post, name='like_post'),
        path('post/<int:post_id>/unlike/', user_manager_views.unlike_post, name='unlike_post'),
        path('post/<int:post_id>/share/', user_manager_views.share_post, name='share_post'),
        path('post/create/', user_manager_views.create_post, name='create_post'),
        path('post/create/comment/<int:post_id>/', user_manager_views.create_post_comment, name='create_post_comment'),
        path('', user_manager_views.home_view, name='home'),
        path('post/<int:post_id>/', user_manager_views.post_view, name='home'),

    ]