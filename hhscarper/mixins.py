import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView
from django_filters.views import FilterView

logger = logging.getLogger(__name__)


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('hhscarper:request-list')

    def get_login_url(self):  # noqa: WPS615
        denied_message = _('Вы не авторизованы! Пожалуйста, выполните вход.')
        messages.add_message(self.request, messages.ERROR, denied_message)
        return super().get_login_url()


class ReportView(DetailView):
    template_name = 'hhscarper/report-detail.html'
    context_object_name = 'report'
    title = None
    paginate_by = 50
    report_type = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page')
        prep_data = tuple(self.get_object().get_data().items())
        data = Paginator(prep_data, self.paginate_by)
        context['page_obj'] = data.get_page(page)

        context['report_data'] = self.get_object().get_data()
        context['report_data_len'] = len(prep_data)
        context['title'] = self.title
        context['report_type'] = self.report_type
        return context


class MyFilterView(FilterView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = dict(self.request.GET)
        query.pop('page', None)
        if query:
            query_string = '&'.join(f'{key}={val[0]}' for key, val in query.items())
            context['saved_qs'] = '&' + query_string  # noqa: WPS336
        return context
