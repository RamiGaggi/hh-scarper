import logging

from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from hhscarper.models import Request
from hhscarper.scarper import construct_hh_page, get_vacancy_urls

logger = logging.getLogger(__name__)


class DashoardView(ListView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'hhscarper/dashboard.html'


class RequestListView(ListView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'hhscarper/request-list.html'


class RequestCreateView(CreateView):
    model = Request
    context_object_name = 'request_create'
    template_name = 'hhscarper/request-create.html'
    fields = ['keyword']

    def get_success_url(self):
        return reverse('hhscarper:request-list')

    def form_valid(self, form):
        logger.debug(f'valid form {form.cleaned_data}')

        keyword = form.cleaned_data['keyword']
        page = construct_hh_page(keyword)
        get_vacancy_urls(page)

        return super().form_valid(form)

    def form_invalid(self, form):
        logger.debug(f'invalid form {form.cleaned_data}')
        messages.add_message(
            self.request,
            messages.ERROR,
            _('Введите ключевое слово в поле запроса'),
        )
        return super().form_invalid(form)


class RequestDetailView(DetailView):
    model = Request
    context_object_name = 'request_detail'
    template_name = 'hhscarper/request-detail.html'


def test_view(request):
    page = 'https://hh.ru/search/vacancy?clusters=true&area=1&ored_clusters=true&enable_snippets=true&salary=&st=searchVacancy&text=python&page=0'  # noqa: E501
    example = get_vacancy_urls(page)
    return HttpResponse(example)
