from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_LIBRARIAN = 'librarian'
    ROLE_MEMBER = 'member'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Admin'),
        (ROLE_LIBRARIAN, 'Librarian'),
        (ROLE_MEMBER, 'Member'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    def is_librarian(self):
        return self.role == self.ROLE_LIBRARIAN or self.role == self.ROLE_ADMIN

    def is_admin(self):
        return self.role == self.ROLE_ADMIN
