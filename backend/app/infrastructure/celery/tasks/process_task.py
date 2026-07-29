from ..celery_app import celery
from ....application.use_cases import UseCase
from ....bootstrap_container import bootstrap_container
from ....domain import FeatureStateLockError


@celery.task(
    queue='process_task_queue',
    autoretry_for=(FeatureStateLockError,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=None,
)
def process_task(job_id: str):
    use_case: UseCase = bootstrap_container.process_job()
    return use_case.execute(job_id)
