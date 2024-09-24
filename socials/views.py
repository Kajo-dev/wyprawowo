from django.shortcuts import render, get_object_or_404
from user_manager.models import Profile, UserResponse
from user_manager.models import Like, PostLike, SharedPost, Question, Post
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import JsonResponse
from django.utils import timezone


# def profile_view(request, slug_profile):
#     profile = get_object_or_404(Profile, slug=slug_profile)
#     worth_to_know_profiles = Profile.objects.all()
#     user_responses = UserResponse.objects.filter(user=profile.user, question__is_profile=True)
#     characteristics = list(map(lambda res: res.answer.text ,user_responses))
#     context = {'profile': profile, 'worth_to_know_profiles':worth_to_know_profiles, 'characteristics': characteristics}
#
#     return render(request, 'socials/profile_page.html', context)


def worth_to_know(request):
    worth_to_know_profiles = Profile.objects.all()
    return render(request, 'socials/worth_to_know.html', {'worth_to_know_profiles':worth_to_know_profiles})


@login_required
@login_required
def profile_view(request, slug_profile):
    user_profile = get_object_or_404(Profile, slug=slug_profile)
    user_posts = list(user_profile.user.posts.all())
    shared_posts = list(SharedPost.objects.filter(user=user_profile.user))

    combined_posts = user_posts + shared_posts
    combined_posts.sort(key=lambda x: x.created_at, reverse=True)

    is_liked_by_user = Like.objects.filter(user=request.user, profile=user_profile).exists()

    posts_with_likes = []
    for item in combined_posts:
        if isinstance(item, Post):
            post = item
            is_shared = False
        else:
            post = item.original_post
            is_shared = True

        is_post_liked_by_user = PostLike.objects.filter(user=request.user, post=post).exists()
        like_count = post.likes.count()
        is_author = post.user == request.user
        posts_with_likes.append((post, is_post_liked_by_user, like_count, is_author, is_shared))

    profile_questions = Question.objects.filter(is_profile=True)
    user_responses = UserResponse.objects.filter(user=user_profile.user, question__in=profile_questions)

    # Get current user's responses
    current_user_responses = UserResponse.objects.filter(user=request.user, question__in=profile_questions)

    # Find common questions answered by both users
    common_questions = set(user_responses.values_list('question_id', flat=True)) & set(current_user_responses.values_list('question_id', flat=True))

    top_profiles = (
        Profile.objects
        .annotate(total_likes=Count('user__posts__likes'))
        .order_by('-total_likes')[:5]
    )

    context = {
        'profile': user_profile,
        'posts_with_likes': posts_with_likes,
        'is_liked_by_user': is_liked_by_user,
        'user_responses': user_responses,
        'common_questions': common_questions,
        'top_profiles': top_profiles,
    }
    return render(request, 'socials/profile_page.html', context)
@login_required
def get_notifications(request):
    notifications = request.user.notifications.filter(is_read=False)
    context = {'notifications': notifications}
    return render(request, 'socials/notifications.html', context)
