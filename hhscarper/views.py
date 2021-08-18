import logging

from django.contrib import messages
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from hhscarper.models import Request, Vacancy
from hhscarper.scarper import scrape

logger = logging.getLogger(__name__)


class DashoardView(ListView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'new_base.html'


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
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Запрос успешно отправлен'),
        )

        keyword = form.cleaned_data['keyword']
        request_obj = form.save(commit=True)
        scrape(keyword, request_obj)
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


class VacancyListView(ListView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'hhscarper/vacancy-list.html'
