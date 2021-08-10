from django.contrib import admin
from hhscarper.models import Request, User, Vacancy

admin.site.register(User)
admin.site.register(Vacancy)
admin.site.register(Request)
