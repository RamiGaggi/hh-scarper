import logging
from datetime import datetime

from celery import shared_task
from hhscarper.models import Request
from hhscarper.reports import REPORTS, make_report
from hhscarper.scarper import scrape

logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(BaseException,),
    retry_kwargs={'max_retries': 1, 'countdown': 2},
)
def scrape_async(keyword, request_obj_id, start):
    result = False
    try:
        result = scrape(keyword, request_obj_id)
    except BaseException as err:  # noqa: WPS424
        logger.error('f{keyword} with reqest id {request_obj_id}')
        logger.error(err)
        req_obj = Request.objects.get(pk=request_obj_id)
        delta = datetime.now() - start
        time_delta = (datetime.min + delta).time()

        req_obj.time = time_delta
        req_obj.status = 'Resolved'
        req_obj.save()
        make_report(request_obj_id, *REPORTS)
    return result
