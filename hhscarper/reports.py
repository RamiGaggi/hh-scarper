from collections import Counter

from hhscarper.models import Request, SkillReport


def make_skill_report(req_id):
    request = Request.objects.get(pk=req_id)
    vacancy_list = request.vacancy_set.all()
    skills = Counter(skill for vacancy in vacancy_list for skill in vacancy.key_skills)
    SkillReport.objects.create(
        data=skills,
        request=request,
    )
