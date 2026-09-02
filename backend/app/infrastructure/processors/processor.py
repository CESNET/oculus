import logging
import time
from abc import ABC, abstractmethod
from typing import Optional

from .visualization_helper import ProcessingPlan
from .visualization_helper import VisualizationHelper
from ...domain import FeatureState, Job, ProcessorOutput
from ...settings import settings


class Processor(ABC):

    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            visualization_helper: VisualizationHelper,
            logger: Optional[logging.Logger] = None,
    ):
        self._job: Job = job
        self._feature_state: FeatureState = feature_state
        self._visualization_helper: VisualizationHelper = visualization_helper

        self._logger: logging.Logger = logger or logging.getLogger(settings.APP_NAME)

    def process(self) -> None:
        start = time.perf_counter()

        processing_plan: ProcessingPlan = self._visualization_helper.create_processing_plan()

        if not processing_plan.visualizations:
            self._logger.info(f"No visualizations to process for job {self._job.id}.")
            return

        self._logger.info(f"Processing {len(processing_plan.visualizations)} visualizations for job {self._job.id}.")

        outputs: list[ProcessorOutput] = self._process(processing_plan)

        elapsed = time.perf_counter() - start

        self._logger.info(f"Processing finished in {elapsed:.3f}s.")

    @abstractmethod
    def _process(self, processing_plan) -> list[ProcessorOutput]:
        ...
