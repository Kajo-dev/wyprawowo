from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from .models import User, Question, Answer, UserResponse, Profile, Like, Post, PostLike, SharedPost, EventPost, Comment
from django.contrib.auth.decorators import login_required
import requests
import json
import smtplib, ssl
from email.message import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Count
from django.utils import timezone
from socials.utils import create_notification
from django.urls import reverse

def activate(request, uidb64, token):
    error_list = []
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        first_question = Question.objects.first()
        if first_question:
            return redirect('question_view', question_id=first_question.id)
        else:
            error_list.append('Brak pytań w bazie')
            data_front = {
                'error_list': error_list
            }
            return render(request, 'starter/home.html', data_front)
    else:
        error_list.append('Link jest niepoprawny')
        data_front = {
            'error_list': error_list
        }
        return render(request, 'starter/home.html', data_front)


def activate_email(request, user, to_email):
    msg = EmailMessage()
    message = render_to_string("user_manager/acctive_account.html", {
        'first_name': user.first_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    msg.set_content(message)
    msg["Subject"] = "Aktywacja Konta."
    msg["From"] = settings.EMAIL_HOST_USER
    msg["To"] = to_email

    context = ssl.create_default_context()
    with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp:
        smtp.starttls(context=context)
        smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        smtp.send_message(msg)



def register_page(request):
    error_list = []
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if not email:
            error_list.append('Adres e-mail jest wymagany ')
        if password1 != password2:
            error_list.append('Hasła nie są takie same ')
        if len(password1) < 6:
            error_list.append('Hasło jest zbyt krótkie ')
        data_front = {
            'error_list': error_list
        }

        if len(error_list) == 0:
            newUser = User.objects.create_user(email=email, first_name=first_name, password=password1, last_name=last_name)
            newUser.save()
            activate_email(request, newUser, email)
            data_front = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email
            }
            return render(request, 'user_manager/confirmation_email.html', data_front)
        else:
            return render(request, 'user_manager/register.html', data_front)
    return render(request, 'user_manager/register.html', {})

def policy_privacy(request):
    return render(request, 'static/policy-privacy.html',{})

def policy_rules(request):
    return render(request, 'static/policy-rules.html',{})


def login_page(request):
    error_list = []
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home') # Policy rules just for testing purposes

        else:
            error_list.append('Dane do logowania są nieprawidłowe')
            data_front = {
                'error_list': error_list
            }
            return render(request, 'user_manager/login.html', data_front)

    return render(request, 'user_manager/login.html', {})


@login_required(login_url='login_page')
def question_view(request, question_id):
    previous_question_id = question_id - 1 if question_id > 1 else 1
    try:
       question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        next_question = Question.objects.filter(id__gt=question_id).order_by('id').first()

        if next_question:
            return redirect('question_page', question_id = next_question.id)
        else:
            return redirect('update_profile')

    answers = Answer.objects.filter(question_id=question.id)

    if request.method=='POST':
        post_answers = request.POST.getlist('answer')
        user = request.user
        if not post_answers:
            return render(request, 'user_manager/questions.html', {
               'question': question,
               'answers': answers,
               'previous_question_id': previous_question_id,
               'error_message': 'Prosze zaznaczyć odpowiedź!'})

        for user_answer_id in post_answers:
            user_response = UserResponse(user=user, question=question, answer_id=user_answer_id)
            user_response.save()

        next_question_id = question_id + 1

        return redirect('question_view', question_id = next_question_id)



    return render(request, 'user_manager/questions.html', {'question': question, 'answers': answers, 'current_number': question_id, 'previous_question_id': previous_question_id})


def upload_photo_to_cloudflare(image):
    account_id = settings.ACCOUNT_ID
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/images/v1'
    headers = {
        'Authorization': f'Bearer {settings.API_KEY}',
    }
    if image:
        files = {'file': image}
        response = requests.post(url.format(ACCOUNT_ID=account_id), headers=headers, files=files)
        if response.status_code == 200:
            result = json.loads(response.text)['result']['variants'][0]
            result = result[:result.rfind('/')]
            return result


@login_required(login_url=login_page)
def update_profile(request):
    profile = Profile.objects.get_or_create(user=request.user)[0]
    if request.method == 'POST':
        description = request.POST.get('description')
        avatar = request.FILES.get('avatar')
        if avatar and description:
            try:
                avatar_link = upload_photo_to_cloudflare(avatar)
                if avatar_link:
                    profile.avatar = avatar_link
                    profile.description = description
                    profile.save()
                    return redirect('ini_payment_view')
            except Exception as e:
                return render(request, 'user_manager/update_profile.html',{
                        'profile_avatar': profile.avatar,
                        'profile_description': profile.description,
                        'error_message': 'Skontaktuj się z administratorem błąd podczas ładowania avataru'}
                )
        else:
            return render(request, 'user_manager/update_profile.html', {'profile_avatar': profile.avatar,
            'profile_description': profile.description, 'error_message':'Wybierz zdjęcie profilowe, oraz Opis!'})

    return render(request, 'user_manager/update_profile.html', {'profile_avatar': profile.avatar, 'profile_description': profile.description})

@login_required(login_url='login_page')
def logout_page(request):
    logout(request)
    return render(request, 'user_manager/logout.html', {})

@login_required(login_url='login_page')
def ini_payment(request):
    return render(request, 'user_manager/ini_payment_process.html', {})

def create_post(request):
    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        content = request.POST.get('content')
        hashtags = request.POST.get('hashtags')
        title = request.POST.get('title')
        event_type = request.POST.get('event_type')
        when = request.POST.get('when')
        where = request.POST.get('where')
        price = request.POST.get('price')

        post = Post.objects.create(
            user=request.user,
            post_type=post_type,
            content=content,
            hashtags=hashtags
        )

        if post_type == 'event':
            EventPost.objects.create(
                post=post,
                title=title,
                event_type=event_type,
                when=when,
                where=where,
                price=price
            )
        followers = Like.objects.filter(profile=request.user.profile)
        for follower in followers:
            print("follower", follower)
            create_notification(follower.user, f'{request.user.first_name} {request.user.last_name} added a new post.')
        return redirect(reverse('profile_view', kwargs={'slug_profile': request.user.profile.slug}))

def create_post_comment(request, post_id):
    if request.method == 'POST':
        content = request.POST.get('content_comment')
        post = get_object_or_404(Post, id=post_id)

        Comment.objects.create(
            user=request.user,
            content=content,
            post=post,
        )

        return redirect('home')


@login_required
def home_view(request):
    posts = Post.objects.all().annotate(comment_count=Count('comments')).order_by('-created_at')

    new_users = Profile.objects.all().order_by('-user__created_at')[:5]

    posts_with_likes = []
    for post in posts:
        is_post_liked_by_user = PostLike.objects.filter(user=request.user, post=post).exists()
        like_count = post.likes.count()
        comment_count = post.comment_count
        is_author = post.user == request.user
        is_shared = False
        posts_with_likes.append((post, is_post_liked_by_user, like_count,comment_count, is_author, is_shared))


    popular_events = (
        EventPost.objects
        .filter(when__gte=timezone.now())
        .annotate(total_likes=Count('post__likes'))
        .order_by('-total_likes')[:4]
    )

    context = {
        'posts': posts_with_likes,
        'new_users': new_users,
        'popular_events': popular_events,
    }
    return render(request, 'user_manager/home.html', context)


def post_view(request, post_id):
    posts = Post.objects.filter(id=post_id).annotate(comment_count=Count('comments'))

    posts_with_likes = []
    for post in posts:
        is_post_liked_by_user = PostLike.objects.filter(user=request.user, post=post).exists()
        like_count = post.likes.count()
        comment_count = post.comment_count
        is_author = post.user == request.user
        is_shared = False
        posts_with_likes.append((post, is_post_liked_by_user, like_count,comment_count, is_author, is_shared))


    context = {
        'posts': posts_with_likes,
    }


    return render(request, 'user_manager/post_view.html', context)

  
@login_required
@require_POST
def like_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    if profile.like(request.user):
        create_notification(profile.user, f'{request.user.username} liked your profile.')
        return JsonResponse({'status': 'liked'})
    else:
        return JsonResponse({'status': 'already liked'})

@login_required
@require_POST
def unlike_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    profile.unlike(request.user)
    return JsonResponse({'status': 'unliked'})

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    PostLike.objects.get_or_create(user=request.user, post=post)
    return JsonResponse({'status': 'liked'})

@login_required
@require_POST
def unlike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    PostLike.objects.filter(user=request.user, post=post).delete()
    return JsonResponse({'status': 'unliked'})

@login_required
def share_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    SharedPost.objects.get_or_create(user=request.user, original_post=post)
    return redirect('profile_view', slug=request.user.profile.slug)