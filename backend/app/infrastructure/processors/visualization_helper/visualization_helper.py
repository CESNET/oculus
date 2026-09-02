import logging
from abc import ABC, abstractmethod

from .processing_plan import ProcessingPlan
from ....domain import FeatureState, Job


class VisualizationHelper(ABC):

    def __init__(
            self,
            job: Job,
            feature_state: FeatureState,
            logger=None,
    ):
        self._job: Job = job
        self._feature_state: FeatureState = feature_state
        self._logger: logging.Logger = logger

    def create_processing_plan(self) -> ProcessingPlan:
        return self._create_processing_plan()

    @abstractmethod
    def _create_processing_plan(self) -> ProcessingPlan:
        ...
