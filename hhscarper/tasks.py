

import logging
from json import JSONDecodeError

from celery import shared_task
from hhscarper.models import Request
from hhscarper.scarper import scrape

logger = logging.getLogger(__name__)


@shared_task(
    autoretry_for=(JSONDecodeError,),
    retry_kwargs={'max_retries': 5, 'countdown': 2},
)
def scrape_async(keyword, request_obj_id):
    try:
        result = scrape(keyword, request_obj_id)
    except JSONDecodeError:
        logger.error('f{keyword} with reqest id {request_obj_id}')
        req_obj = Request.objects.get(pk=request_obj_id)
        req_obj.status = 'Error'
        req_obj.save()
    return result
