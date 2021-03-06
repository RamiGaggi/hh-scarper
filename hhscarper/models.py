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


class ReportMixin(models.Model):
    data = models.JSONField()
    request = models.OneToOneField(
        'Request',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.request.keyword}'

    def get_most_valuable(self):
        data = {**self.data, **{_('Отсутствует'): 0}}
        return max(data, key=data.get)

    def get_data(self, items=None, order='desc'):  # noqa: WPS615
        order_flag = -1
        if order == 'asc':
            order_flag = 1
        data = sorted(self.data.items(), key=lambda item: order_flag * item[1])[:items]
        return dict(data)

    class Meta:
        abstract = True


class User(AbstractUser):
    def __str__(self):
        return ' '.join([self.first_name, self.last_name])


class Vacancy(TimeStampMixin):
    external_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    description = models.TextField(max_length=3000)
    key_skills = models.JSONField(null=True)
    lemmas = models.JSONField()
    requests = models.ManyToManyField('Request', through='VacancyRequest')
    is_missing = models.BooleanField(default=False)

    def __str__(self):
        return self.title[:10]

    def get_absolute_url(self):
        return reverse('vacancy-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-created_at']


class RequestManager(models.Manager):

    def group_by_date(self):

        return (
            self
            .extra({'date_created': 'date(created_at)'})
            .values('date_created')
            .annotate(total=models.Count('id'))
            .order_by('date_created')
        )


class Request(TimeStampMixin):
    class Status(models.TextChoices):
        pending = 'Pending', _('В процессе')
        resolved = 'Resolved', _('Готово')
        error = 'Error', _('Ошибка')

    objects = RequestManager()

    keyword = models.CharField(
        unique=True,
        max_length=100,
        verbose_name=_('ключевое слово'),
    )
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
        ordering = ['-created_at']


class VacancyRequest(TimeStampMixin):
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.request.keyword} {self.vacancy.title[:10]}'

    class Meta:
        db_table = 'hhscarper_vacancy_request'


class SkillReport(ReportMixin, TimeStampMixin):
    def __str__(self):
        return f'SkillReport {self.request.keyword}'

    class Meta:
        db_table = 'hhscarper_skill_report'


class WordReport(ReportMixin, TimeStampMixin):
    def __str__(self):
        return f'WordReport {self.request.keyword}'

    class Meta:
        db_table = 'hhscarper_word_report'
