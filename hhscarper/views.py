import codecs
import csv
import logging
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView
from django.views.generic.list import ListView
from hhscarper.charts import get_dashoard_figure, get_report_figure
from hhscarper.filters import RequestFilter, VacancyFilter
from hhscarper.mixins import MyFilterView, MyLoginRequiredMixin, ReportView
from hhscarper.models import Request, SkillReport, User, Vacancy, WordReport
from hhscarper.reports import REPORTS
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

        dashboard_chart = get_dashoard_figure()

        dashboard_script, dashboard_html = dashboard_chart
        context['dashboard_script'] = dashboard_script
        context['dashboard_html'] = dashboard_html

        return context


class RequestListView(MyFilterView):
    model = Request
    context_object_name = 'request_list'
    template_name = 'hhscarper/request-list.html'
    paginate_by = 20
    filterset_class = RequestFilter


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
            _('???????????? ?????????????? ??????????????????'),
        )
        scrape_async.delay(keyword, request_obj.id, start=datetime.now())
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.debug(f'invalid form {form.data["keyword"]}')
        keyword = form.data['keyword']
        if keyword:
            req_id = Request.objects.get(keyword=keyword).pk
            messages.add_message(
                self.request,
                messages.WARNING,
                _('???????????? ?? ?????????? ???????????????? ???????????? ?????? ????????'),
            )
            return redirect('hhscarper:request-detail', req_id)

        return super().form_invalid(form)


class RequestDetailView(DetailView):
    model = Request
    context_object_name = 'request_detail'
    template_name = 'hhscarper/request-detail.html'

    def dispatch(self, request, *args, **kwargs):
        req_obj = self.get_object()
        if req_obj.status != 'Resolved':
            messages.add_message(
                request,
                messages.WARNING,
                _('????????????????????, ??????????????????, ???????????? ????????????????????????????'),
            )
            return redirect('hhscarper:request-list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        req_obj = self.get_object()

        valuable_skill = req_obj.skillreport.get_most_valuable()
        valuable_word = req_obj.wordreport.get_most_valuable()

        desc_skill_chart = get_report_figure(
            req_obj.skillreport.get_data(items=10),
            title=_('?????????? ???????????????????????????? ???????????? ?????? ?????????????? ??????????????'),
        )
        asc_skill_chart = get_report_figure(
            req_obj.skillreport.get_data(items=10, order='asc'),
            title=_('?????????? ???????????? ???????????? ?????? ?????????????? ??????????????'),
        )

        desc_word_chart = get_report_figure(
            req_obj.wordreport.get_data(items=10),
            title=_('???????????????? ?????????????????????? ?????????? ?????? ?????????????? ??????????????'),
        )
        asc_word_chart = get_report_figure(
            req_obj.wordreport.get_data(items=10, order='asc'),
            title=_('???????????????? ???????????? ?????????? ?????? ?????????????? ??????????????'),
        )

        desc_word_script, desc_word_html = desc_word_chart
        desc_skill_script, desc_skill_html = desc_skill_chart
        asc_word_script, asc_word_html = asc_word_chart
        asc_skill_script, asc_skill_html = asc_skill_chart

        context['valuable_word'] = valuable_word
        context['valuable_skill'] = valuable_skill

        context['desc_skill_script'] = desc_skill_script
        context['desc_skill_html'] = desc_skill_html
        context['asc_skill_script'] = asc_skill_script
        context['asc_skill_html'] = asc_skill_html

        context['desc_word_script'] = desc_word_script
        context['desc_word_html'] = desc_word_html
        context['asc_word_script'] = asc_word_script
        context['asc_word_html'] = asc_word_html

        context['skill_report_id'] = req_obj.skillreport.pk
        context['word_report_id'] = req_obj.wordreport.pk
        return context


class RequestDeleteView(MyLoginRequiredMixin, DeleteView):
    model = Request
    success_url = reverse_lazy('hhscarper:request-list')
    template_name = 'hhscarper/request-delete.html'

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.add_message(
            request,
            messages.SUCCESS,
            _('???????????? ?????????????? ????????????'),
        )
        return response


class SkillReportDetailView(ReportView):
    model = SkillReport
    title = gettext_lazy('???????????????? ????????????')
    report_type = 'skill'


class WordReportDetailView(ReportView):
    model = WordReport
    title = gettext_lazy('???????????????????? ???? ????????????')
    report_type = 'word'


class VacancyListView(MyFilterView):
    model = Vacancy
    context_object_name = 'vacancy_list'
    template_name = 'hhscarper/vacancy-list.html'
    paginate_by = 50
    filterset_class = VacancyFilter


class UserLoginView(SuccessMessageMixin, LoginView):
    model = User
    template_name = 'hhscarper/user-login.html'
    extra_context = {'next': reverse_lazy('hhscarper:request-list')}
    fields = ['username', 'password']
    success_message = gettext_lazy('???????? ?????????????? ????????????????')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('hhscarper:user-login')

    def dispatch(self, request, *args, **kwargs):
        next_page = super().dispatch(request, *args, **kwargs)
        messages.add_message(
            request,
            messages.INFO,
            _('?????????? ?????????????? ????????????????'),
        )
        return next_page


class ExportData(View):

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response.write(codecs.BOM_UTF8)

        query_dict = request.GET

        report = query_dict.get('report')
        requests = query_dict.getlist('request')
        logger.debug(requests)
        if report in REPORTS and requests:
            self.write_csv(requests, report, response)
            response['Content-Disposition'] = (
                f'attachment; filename="{requests[0]}_{report}.csv"'
            )

        return response

    @staticmethod
    def write_csv(requests, report, response):  # noqa: WPS602
        writer = csv.writer(response)
        writer.writerow([_('????????????'), _('????????????????'), _('????????????????????')])
        counter = 0
        for req in requests:
            try:
                req_obj = Request.objects.get(keyword=req)
            except Request.DoesNotExist:
                logger.debug(req)
                continue

            if report == 'skill':
                for key1, val1 in req_obj.skillreport.get_data().items():
                    writer.writerow([req, key1, val1])
                    counter += 1
            elif report == 'word':
                for key2, val2 in req_obj.wordreport.get_data().items():
                    writer.writerow([req, key2, val2])
        return counter
