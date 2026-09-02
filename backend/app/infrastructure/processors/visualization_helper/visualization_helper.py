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
        self._job = job
        self._feature_state = feature_state
        self._logger = logger

    def create_processing_plan(self) -> ProcessingPlan:
        return self._create_processing_plan()

    @abstractmethod
    def _create_processing_plan(self) -> ProcessingPlan:
        ...
