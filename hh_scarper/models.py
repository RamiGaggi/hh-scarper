from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return ' '.join([self.first_name, self.last_name])
