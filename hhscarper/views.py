import logging

from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.list import ListView
from hhscarper.models import Request
from hhscarper.scarper import get_vacancy_urls

logger = logging.getLogger(__name__)


class DashoardView(ListView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'hhscarper/dashboard.html'


class CreateRequestView(View):
    def post(self, request, *args, **kwargs):
        logger.info(request.POST)
        logger.info(kwargs)
        return HttpResponse('Hello, World!')


class ListRequestView(ListView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'hhscarper/request-list.html'


def test_view(request):
    page = 'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python&page=0'  # noqa: E501
    example = get_vacancy_urls(page)
    return HttpResponse(example)
