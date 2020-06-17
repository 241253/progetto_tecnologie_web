from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, email, nome, cognome, password=None):
        if not email:
            raise ValueError("L'utente deve avere un indirizzo email.")
        if not nome:
            raise ValueError("L'utente deve avere un nome")
        if not cognome:
            raise ValueError("L'utente deve avere un cognome")

        user = self.model(
            email = self.normalize_email(email),
            nome = nome,
            cognome = cognome
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, cognome, password):
        user = self.create_user(
            email = self.normalize_email(email),
            nome = nome,
            cognome = cognome,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    nome = models.CharField(max_length=30)
    cognome = models.CharField(max_length=30)
    foto = models.FileField()
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nome", "cognome"]

    objects = MyAccountManager()

    def __str__(self):
        return self.email + " " + self.nome + " " + self.cognome

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True