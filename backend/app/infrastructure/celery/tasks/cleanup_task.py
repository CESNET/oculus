from ..celery_app import celery
from ....application.use_cases import UseCase
from ....bootstrap_container import bootstrap_container


@celery.task
def cleanup_task():
    use_case: UseCase = bootstrap_container.cleanup_job()
    return use_case.execute()
