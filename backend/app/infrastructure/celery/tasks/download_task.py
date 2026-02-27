from ..celery_app import celery
from ....application.use_cases import UseCase
from ....bootstrap_container import bootstrap_container


@celery.task
def download_task(job_id: str):
    use_case: UseCase = bootstrap_container.download_job()
    return use_case.execute(job_id)
