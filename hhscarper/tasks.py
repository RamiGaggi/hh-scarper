from celery import shared_task
from hhscarper.scarper import scrape


@shared_task(ignore_result=True)
def scrape_async(keyword, request_obj_id):
    scrape(keyword, request_obj_id)
