from django.contrib import admin
from hhscarper import models

admin.site.register(
    (
        models.User,
        models.Vacancy,
        models.Request,
        models.SkillReport,
        models.WordReport,
        models.VacancyRequest,
    ),
)
