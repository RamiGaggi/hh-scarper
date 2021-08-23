import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from hhscarper.mixins import MyLoginRequiredMixin
from hhscarper.models import Request, Vacancy
from hhscarper.tasks import scrape_async

logger = logging.getLogger(__name__)


class DashoardView(ListView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'hhscarper/dashboard.html'


class RequestListView(ListView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'hhscarper/request-list.html'
    paginate_by = 10


class RequestCreateView(MyLoginRequiredMixin, CreateView):
    model = Request
    context_object_name = 'request_create'
    template_name = 'hhscarper/request-create.html'
    fields = ['keyword']

    def get_success_url(self):
        return reverse('hhscarper:request-list')

    def form_valid(self, form):
        logger.debug(f'valid form {form.cleaned_data}')
        keyword = form.cleaned_data['keyword']
        request_obj = form.save(commit=True)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Запрос успешно отправлен'),
        )
        scrape_async.delay(keyword, request_obj.id)
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.debug(f'invalid form {form.data["keyword"]}')
        keyword = form.data['keyword']
        if keyword:
            req_id = Request.objects.get(keyword=keyword).pk
            messages.add_message(
                self.request,
                messages.INFO,
                _('Запрос с таким ключевым словом уже есть'),
            )
            return redirect('hhscarper:request-detail', req_id)

        return super().form_invalid(form)


class RequestDetailView(DetailView):
    model = Request
    context_object_name = 'request_detail'
    template_name = 'hhscarper/request-detail.html'

    def get_context_data(self, **kwargs):
        logger.debug(self.__dict__)
        context = super().get_context_data(**kwargs)

        valuable_skill = self.get_object().skillreport.get_most_valuable()
        valuable_word = self.get_object().wordreport.get_most_valuable()

        context['valuable_word'] = valuable_word
        context['valuable_skill'] = valuable_skill
        return context


class VacancyListView(ListView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'hhscarper/vacancy-list.html'
    paginate_by = 50
