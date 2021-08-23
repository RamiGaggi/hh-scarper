from django.core.management.base import BaseCommand, CommandError
from hhscarper.models import Request
from hhscarper.reports import REPORTS, make_report


class Command(BaseCommand):
    help = 'Updates all reports'

    def add_arguments(self, parser):
        parser.add_argument('reports', nargs='*', type=str, default=REPORTS)

    def handle(self, *args, **options):
        for report in options['reports']:
            if report.lower() not in REPORTS:
                raise CommandError('Report "{0}" does not exist'.format(report))  # noqa: WPS323, E501

        req_ids = set(Request.objects.values_list('pk', flat=True))
        for req in req_ids:
            make_report(req, *options['reports'])

        self.stdout.write(
            self.style.SUCCESS(
                'The following reports have been updated: {0}'.format(', '.join(options['reports'])),  # noqa: E501
            ),
        )  # noqa: E501, WPS221
