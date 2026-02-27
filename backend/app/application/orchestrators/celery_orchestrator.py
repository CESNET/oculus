from celery import chain

from . import BaseOrchestrator
from ...tasks import download_task, process_task, finalize_task, cleanup_task


class CeleryOrchestrator(BaseOrchestrator):

    def run_pipeline(self, job_id: str):
        import logging
        logging.getLogger("oculus").info(f"Running job_id: {job_id}")
        workflow = chain(
            download_task.s(job_id),
            process_task.s(),
            finalize_task.s()
        )
        workflow.apply_async()

    def cleanup(self):
        cleanup_task.delay()
