from django.contrib import admin
from hhscarper.models import Request, SkillReport, User, Vacancy

admin.site.register(User)
admin.site.register(Vacancy)
admin.site.register(Request)
admin.site.register(SkillReport)
