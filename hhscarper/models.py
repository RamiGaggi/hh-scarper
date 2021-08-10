from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('date of creation'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date of change'),
    )

    class Meta:
        abstract = True


class User(AbstractUser):
    def __str__(self):
        return ' '.join([self.first_name, self.last_name])


class Vacancy(TimeStampMixin, models.Model):
    external_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    request = models.ForeignKey('Request', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('vacancy')
        verbose_name_plural = _('vacancies')

    def __str__(self):
        return self.title[:10]

    def get_absolute_url(self):
        return reverse('vacancy-detail', kwargs={'pk': self.pk})


class Request(TimeStampMixin, models.Model):
    class Status(models.TextChoices):
        pending = 'Pending', _('В процессе')
        resolved = 'Resolved', _('Готово')

    search_value = models.CharField(max_length=100)
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.pending,
    )
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.search_value

    def get_absolute_url(self):
        return reverse('request-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _('запрос')
        verbose_name_plural = _('запросы')
