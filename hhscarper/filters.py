import django_filters
from django.utils.translation import gettext_lazy as _
from hhscarper.models import Request, Vacancy


class RequestFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(lookup_expr='icontains', label=_('Ключевое слово'))

    class Meta:
        model = Request
        fields = ['keyword']


class VacancyFilter(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        """Update filters after creating status/labels."""
        super().__init__(*args, **kwargs)
        self.filters['requests'].extra['choices'] = sorted(
            ((obj.pk, obj.keyword) for obj in Request.objects.all()),
            key=lambda request: request[1].lower(),
        )

    title = django_filters.CharFilter(lookup_expr='icontains', label=_('Название вакансии'))
    requests = django_filters.MultipleChoiceFilter(label=_('Запросы'))

    class Meta:
        model = Vacancy
        fields = ['title', 'requests']
