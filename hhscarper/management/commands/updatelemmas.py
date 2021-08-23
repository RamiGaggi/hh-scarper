from django.core.management.base import BaseCommand
from hhscarper.models import Vacancy
from hhscarper.preprocessor import preprocess_text


class Command(BaseCommand):
    help = 'Updates all lemmas'

    def handle(self, *args, **options):
        vacancies = Vacancy.objects.all()
        for vacancy in vacancies:
            vacancy.lemmas = preprocess_text(vacancy.description)
            vacancy.save()
        self.stdout.write(self.style.SUCCESS('All lemmas have been updated'))
