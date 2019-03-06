import requests
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.core.files.base import ContentFile
from users.forms import LoginForm, SignUpForm
from users.models import User
from my_settings import Github_ID, Github_SECRET, KAKAO_REST_API_KEY

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", {"form": form})

def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))

class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
        user.verify_email()
        return super().form_valid(form)

def complete_verification(request, key):
    try:
        user = User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
    except User.DoesNotExist:
        pass
    return redirect(reverse("core:home"))

def github_login(request):
    client_id = Github_ID
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user")

class GithubException(Exception): pass

def github_callback(request):
    try:
        client_id = Github_ID
        client_secret = Github_SECRET
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            if "error" in token_json:
                raise GithubException("Cannot get access token")
            
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"token {access_token}", "Accept": "application/json"},
            )
            profile_json = profile_request.json()
            username = profile_json.get('login')
            if username:
                name = profile_json.get('name') or username
                github_link = profile_json.get('html_url')
                bio = profile_json.get('bio') or ""
                try:
                    user = User.objects.get(email=github_link)
                    if user.login_method != User.LOGIN_GITHUB:
                        raise GithubException(f"Please log in with: {user.login_method}")
                except User.DoesNotExist:
                    user = User.objects.create(
                        username=github_link, email=github_link, first_name=name, bio=bio,
                        login_method=User.LOGIN_GITHUB, email_verified=True
                    )
                    user.set_unusable_password()
                    user.save()
                login(request, user)
                return redirect(reverse("core:home"))
            else:
                raise GithubException("Cannot get profile")
        else:
            raise GithubException()
    except GithubException:
        return redirect(reverse("users:login"))

def kakao_login(request):
    client_id = KAKAO_REST_API_KEY
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code")

class KakaoException(Exception): pass

def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = KAKAO_REST_API_KEY
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}")
        token_json = token_request.json()
        
        if "error" in token_json:
            raise KakaoException("Cannot get authorization code")
        
        access_token = token_json.get("access_token")
        profile_request = requests.get("https://kapi.kakao.com/v1/user/me", headers={"Authorization": f"Bearer {access_token}"})
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email") if kakao_account else None
        
        if not email:
            raise KakaoException("Please provide email")
            
        properties = profile_json.get("properties")
        nickname = properties.get("nickname")
        profile_image = properties.get("profile_image")
        
        try:
            user = User.objects.get(email=email)
            if user.login_method != User.LOGIN_KAKAO:
                raise KakaoException(f"Please log in with: {user.login_method}")
        except User.DoesNotExist:
            user = User.objects.create(
                email=email, username=email, first_name=nickname,
                login_method=User.LOGIN_KAKAO, email_verified=True
            )
            user.set_unusable_password()
            user.save()
            if profile_image:
                photo_request = requests.get(profile_image)
                user.avatar.save(f"{nickname}-avatar.jpg", ContentFile(photo_request.content))
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("users:login"))