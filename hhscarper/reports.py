import logging
from collections import Counter

from hhscarper.models import Request, SkillReport, WordReport

logger = logging.getLogger(__name__)

REPORTS = ('skill', 'word')


def make_report(req_id, *args):
    request = Request.objects.get(pk=req_id)
    vacancy_list = request.vacancy_set.all()
    if 'skill' in args:
        skills = Counter(skill for vacancy in vacancy_list for skill in vacancy.key_skills)  # noqa:E501
        SkillReport.objects.update_or_create(
            request=request,
            defaults={
                'data': skills,
            },
        )
    if 'word' in args:
        words = Counter(word for vacancy in vacancy_list for word in vacancy.lemmas)  # noqa:E501
        WordReport.objects.update_or_create(
            request=request,
            defaults={
                'data': words,
            },
        )
