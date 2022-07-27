from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.conf import settings


class ShopUser(AbstractUser):
    """Кастомная модель User."""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLES = [
        (USER, 'User'),
        (MODERATOR, 'Moderator'),
        (ADMIN, 'Administrator'),
    ]
    country = models.CharField(blank=False, max_length=35)
    city = models.CharField(blank=False, max_length=50)
    address = models.CharField(blank=False, max_length=500)
    phone_number = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length=254, blank=False)
    role = models.CharField(max_length=100, choices=ROLES, default=USER)

    def send_confirmation_code(self):
        """Подключение отправки почтой."""
        subject = 'Email Verification'
        verification_token = default_token_generator.make_token(self)
        send_mail(
            subject=subject,
            message=f'your confirmation code is {verification_token}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=(self.email,)
        )

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ShopUser.ADMIN

    @property
    def is_moderator(self):
        return self.role == ShopUser.MODERATOR

    @property
    def is_user(self):
        return self.role == ShopUser.USER

    class Meta:
        ordering = ['-username']
