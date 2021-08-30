import django_filters
from django.utils.translation import gettext_lazy as _
from hhscarper.models import Request, Vacancy


class RequestFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(lookup_expr='icontains', label=_('Ключевое слово'))

    class Meta:
        model = Request
        fields = ['keyword']


class VacancyFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label=_('Название вакансии'))

    class Meta:
        model = Vacancy
        fields = ['title']
