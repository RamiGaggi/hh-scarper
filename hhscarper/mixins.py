import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic.detail import DetailView

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page')
        data = Paginator(tuple(self.get_object().get_data().items()), self.paginate_by)
        context['page_obj'] = data.get_page(page)

        context['report_data'] = self.get_object().get_data()
        context['title'] = self.title
        return context
