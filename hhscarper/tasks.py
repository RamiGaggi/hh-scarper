from celery import shared_task
from hhscarper.scarper import scrape


@shared_task()
def scrape_async(keyword, request_obj_id):
    return scrape(keyword, request_obj_id)
