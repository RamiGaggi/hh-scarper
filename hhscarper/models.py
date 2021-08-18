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
    external_id = models.IntegerField()
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    description = models.TextField(max_length=3000)
    key_skills = models.JSONField()
    lemmas = models.JSONField()
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

    keyword = models.CharField(max_length=100, verbose_name=_('ключевое слово'))
    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.pending,
        editable=False,
    )
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.keyword

    def get_absolute_url(self):
        return reverse('hhscarper:request-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _('запрос')
        verbose_name_plural = _('запросы')
