from celery import chain

from .base_orchestrator import BaseOrchestrator


class CeleryOrchestrator(BaseOrchestrator):
    def run_pipeline(self, job_id: str):
        self._logger.info(f"Running Celery workflow, job id: {job_id}")

        from ...infrastructure.celery.tasks import check_task, download_task, process_task, finalize_task
        workflow = chain(
            download_task.s(job_id),
            check_task.s(),
            process_task.s(),
            check_task.s(),
            finalize_task.s(),
            check_task.s(),
        )
        workflow.apply_async()

    def cleanup(self):
        from ...infrastructure.celery.tasks import cleanup_task
        cleanup_task.delay()
