from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _


class MyLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('hhscarper:request-list')

    def get_login_url(self):  # noqa: WPS615
        denied_message = _('Вы не авторизованы! Пожалуйста, выполните вход.')
        messages.add_message(self.request, messages.ERROR, denied_message)
        return super().get_login_url()
