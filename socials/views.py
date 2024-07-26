from django.shortcuts import render, get_object_or_404
from user_manager.models import Profile, UserResponse

def profile_view(request, slug_profile):
    profile = get_object_or_404(Profile, slug=slug_profile)
    worth_to_know_profiles = Profile.objects.all()
    user_responses = UserResponse.objects.filter(user=profile.user, question__is_profile=True)
    characteristics = list(map(lambda res: res.answer.text ,user_responses))
    context = {'profile': profile, 'worth_to_know_profiles':worth_to_know_profiles, 'characteristics': characteristics}

    return render(request, 'socials/profile_page.html', context)

def worth_to_know(request):
    worth_to_know_profiles = Profile.objects.all()
    return render(request, 'socials/worth_to_know.html', {'worth_to_know_profiles':worth_to_know_profiles})