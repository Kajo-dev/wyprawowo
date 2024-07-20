from django.shortcuts import render, get_object_or_404
from user_manager.models import Profile

def profile_view(request, slug_profile):
    profile = get_object_or_404(Profile, slug=slug_profile)
    context = {'profile': profile}
    return render(request, 'socials/profile_page.html', context)