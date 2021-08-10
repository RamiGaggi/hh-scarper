import logging

from django.http import HttpResponse
from django.views.generic.list import ListView
from hhscarper.models import Vacancy
from hhscarper.scarper import get_vacancy_urls

logger = logging.getLogger(__name__)


class VacancyListView(ListView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'hhscarper/dashboard.html'


def test_view(request):
    page = 'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python&page=0'  # noqa: E501
    example = get_vacancy_urls(page)
    return HttpResponse(example)
