import logging

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from hhscarper.charts import get_figure
from hhscarper.mixins import MyLoginRequiredMixin
from hhscarper.models import Request, Vacancy
from hhscarper.tasks import scrape_async

logger = logging.getLogger(__name__)


class DashoardView(ListView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'hhscarper/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        vacancy_count = Vacancy.objects.count()
        vacancy_last = Vacancy.objects.last()
        request_count = Request.objects.count()
        request_last = Request.objects.last()

        context['vacancy_last'] = vacancy_last
        context['request_last'] = request_last
        context['vacancy_count'] = vacancy_count
        context['request_count'] = request_count
        return context


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
        context = super().get_context_data(**kwargs)
        req_obj = self.get_object()
        try:  # noqa: WPS229
            valuable_skill = req_obj.skillreport.get_most_valuable()
            valuable_word = req_obj.wordreport.get_most_valuable()
        except ObjectDoesNotExist:
            valuable_skill = valuable_word = _('Запрос в обработке')
        try:  # noqa: WPS229
            skill_chart = get_figure(
                req_obj.skillreport.get_sorted_data(items=10),
                title=_('Самые востребованные навыки для данного запроса'),
            )
            word_chart = get_figure(
                req_obj.wordreport.get_sorted_data(items=10),
                title=_('Наиболее упоминаемое слово для данного запроса'),
            )
        except ObjectDoesNotExist:
            info = ('', _('Пожалуйста подождите'))
            word_chart = info
            skill_chart = info

        word_script, word_html = word_chart
        skill_script, skill_html = skill_chart

        context['valuable_word'] = valuable_word
        context['valuable_skill'] = valuable_skill

        context['skill_script'] = skill_script
        context['skill_html'] = skill_html

        context['word_script'] = word_script
        context['word_html'] = word_html
        return context


class VacancyListView(ListView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'hhscarper/vacancy-list.html'
    paginate_by = 50
