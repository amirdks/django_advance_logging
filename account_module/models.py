from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError(_("The username must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = ASCIIUsernameValidator
    username = models.CharField(
        _("User Name"),
        max_length=255,
        unique=True,
        validators=[username_validator],
        error_messages={
            "unique": _("A user with this username already exists"),
        },
    )
    first_name = models.CharField(_("First Name"), null=True, blank=True, max_length=255)
    last_name = models.CharField(_("Last Name"), null=True, blank=True, max_length=255)
    is_superuser = models.BooleanField(_("Super User Status"), default=False)
    is_active = models.BooleanField(_("Active Status"), default=True)

    created_at = models.DateTimeField(_("Registry Date"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last Update Date"), auto_now=True)

    USERNAME_FIELD = "username"
    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        if self.first_name:
            if self.last_name:
                return f"{self.first_name} {self.last_name}"
            return self.first_name
        return self.username

    @property
    def get_full_name(self):
        return self.__str__()
