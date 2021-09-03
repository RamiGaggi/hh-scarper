import logging
from collections import Counter

from hhscarper.models import DiffReport, Request, SkillReport, WordReport

logger = logging.getLogger(__name__)

REPORTS = ('skill', 'word', 'diff')


def make_report(req_id, *args):
    request = Request.objects.get(pk=req_id)
    vacancy_list = request.vacancy_set.all()
    if 'skill' in args:
        skills = Counter(skill for vacancy in vacancy_list for skill in vacancy.key_skills)  # noqa:E501
        skill_report = SkillReport.objects.update_or_create(
            request=request,
            defaults={
                'data': skills,
            },
        )
    if 'word' in args:
        words = Counter(word for vacancy in vacancy_list for word in vacancy.lemmas)  # noqa:E501
        word_report = WordReport.objects.update_or_create(
            request=request,
            defaults={
                'data': words,
            },
        )
    if 'diff' in args and 'skill' in args and 'word' in args:
        skill_data = {key.upper(): val for key, val in skill_report[0].data.items()}
        word_data = word_report[0].data
        intersection = skill_data.keys() & word_data.keys()

        skill_diff = {key: skill_data[key] for key in intersection}
        word_diff = {key: word_data[key] for key in intersection}
        diff = {
            'skill': skill_diff,
            'word': word_diff,
        }

        DiffReport.objects.update_or_create(
            request=request,
            defaults={
                'data': diff,
            },
        )
