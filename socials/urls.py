from user_manager import views as user_manager_views
from socials import views as socials_views
from django.views.generic import TemplateView
from django.urls import path

urlpatterns = [
        path('uzupelnij', user_manager_views.update_profile, name="update_profile"),
        path('<slug:slug_profile>', socials_views.profile_view, name="profile_view"),
        path('warto-znac/', socials_views.worth_to_know, name="worth_to_know"),
    ]