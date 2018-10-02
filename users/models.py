import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string

class User(AbstractUser):
    Gender_Male = "male"
    Gender_Female = "female"
    Gender_Others = "other"
    Gender_Choices = ((Gender_Male, "Male"), (Gender_Female, "Female"), (Gender_Others, "Others"))

    LOGIN_EMAIL = "email"
    LOGIN_GITHUB = "github"
    LOGIN_KAKAO = "kakao"
    LOGIN_CHOICES = ((LOGIN_EMAIL, "Email"), (LOGIN_GITHUB, "Github"), (LOGIN_KAKAO, "Kakao"))

    Language_KOREAN = "KR"
    Language_English = "EN"
    Language_Chinese = "CN"
    Language_Japanese = "JP"
    Language_Choices = ((Language_KOREAN, "Korean"), (Language_English, "English"), (Language_Chinese, "Chinese"), (Language_Japanese, "Japanese"))

    Currency_KRW = "KRW"
    Currency_USD = "USD"
    Currency_EUR = "EUR"
    Currency_Choices = ((Currency_KRW, "KRW"), (Currency_USD, "USD"), (Currency_EUR, "EUR"))

    bio = models.TextField(default="")
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(choices=Gender_Choices, max_length=10, blank=True)
    avatar = models.ImageField(upload_to="profile_image", blank=True)
    language = models.CharField(choices=Language_Choices, max_length=50, blank=True, default=Language_KOREAN)
    currency = models.CharField(choices=Currency_Choices, max_length=10, blank=True, default=Currency_KRW)
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=80, default="", blank=True)
    login_method = models.CharField(max_length=50, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex
            self.email_secret = secret
            html_message = render_to_string("emails/verify_email.html", {"secret": secret})
            send_mail(
                "Verify K-Sookbak Account",
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=False,
                html_message=html_message
            )
            self.save()
        return