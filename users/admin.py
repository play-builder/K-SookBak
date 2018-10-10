from django.contrib            import admin
from django.contrib.auth.admin import UserAdmin
from .                         import models

@admin.register(models.User)      #데코레이터와 마찬가지로 동이할게 작동 = admin.site.register(models.User, CustomUserAdmin)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Profile",
            {
                "fields":
                    ("language",
                    "birthday",
                    "gender",
                    "currency",
                    "bio",
                    "avatar",
                    "superhost",
                    "login_method",
                    )
            },
        ),
    )

    list_filter = UserAdmin.list_filter + ("superhost",)

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "language",
        "currency",
        "superhost",
        "is_staff",
        "is_superuser",
        "email_verified",
        "email_secret",
        "login_method",
    )

