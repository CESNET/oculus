import uuid
from pathlib import Path
from typing import Any, Optional

DEFAULT_NAMESPACE: uuid.UUID = uuid.NAMESPACE_DNS


def calculate_uuid(
        dataset: str,
        feature_id: str,
        namespace: uuid.UUID = DEFAULT_NAMESPACE,
) -> uuid.UUID:
    name = f"{dataset}:{feature_id}"
    return uuid.uuid5(namespace, name)


class FeatureState:
    def __init__(
            self,
            dataset: str,
            feature_id: str,

            data_directory: str,

            files: Optional[list[dict[str, Any]]] = None,
    ):
        self.dataset = dataset
        self.feature_id = feature_id
        self.id = calculate_uuid(
            dataset=dataset,
            feature_id=feature_id
        )

        self.data_directory = data_directory

        self.files: Optional[list[dict[str, Any]]] = files or []

    @classmethod
    def create(
            cls,
            dataset: str,
            feature_id: str,
            data_directory: str,
    ) -> "FeatureState":
        data_directory = str(Path(data_directory) / dataset / feature_id)

        return cls(
            dataset=dataset,
            feature_id=feature_id,

            data_directory=data_directory
        )
