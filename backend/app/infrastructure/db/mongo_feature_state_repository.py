from pathlib import Path

from pymongo import ReturnDocument
from pymongo.collection import Collection

from ...domain import (
    FeatureState,
    FeatureStateId,
    FeatureStateRepository,
    FeatureStateNotFound,
    FileState,
    TileGroup,
    OutputFormat
)


class MongoFeatureStateRepository(FeatureStateRepository):

    def __init__(self, collection: Collection):
        self.collection = collection

    # -------------------------
    # mapping
    # -------------------------

    def _to_doc(
            self,
            state: FeatureState,
    ) -> dict:
        doc = state.to_dict()
        doc["_id"] = str(state.id)
        return doc

    def _from_doc(
            self,
            doc: dict,
    ) -> FeatureState:
        return FeatureState.from_dict(doc)

    # -------------------------
    # read
    # -------------------------

    def get(
            self,
            feature_state_id: FeatureStateId,
    ) -> FeatureState:

        doc = self.collection.find_one(
            {
                "_id": str(feature_state_id),
            }
        )

        if doc is None:
            raise FeatureStateNotFound(str(feature_state_id))

        return self._from_doc(doc)

    # -------------------------
    # write
    # -------------------------

    def save(
            self,
            feature_state: FeatureState,
    ) -> FeatureState:

        self.collection.replace_one(
            {
                "_id": str(feature_state.id)
            },
            self._to_doc(
                feature_state
            ),
            upsert=True
        )

        return feature_state

    def mark_files_downloaded(
            self,
            feature_state_id: FeatureStateId,
            downloaded_files: list[str],
    ) -> FeatureState:

        feature_state = self.get(feature_state_id)

        for file_path in downloaded_files:

            file_path = Path(file_path)

            filename = file_path.stem

            file_state = feature_state.get_file_state(filename)

            if file_state is None:

                feature_state.files[filename] = FileState(
                    filename=filename,
                    download_path=file_path,
                )

            else:
                file_state.download_path = file_path

        return self.save(feature_state)

    def mark_files_processed(
            self,
            feature_state_id: FeatureStateId,
            processed_files: dict[str, str | Path],
            group: TileGroup,
            format_name: OutputFormat,
    ) -> FeatureState:

        feature_state = self.get(feature_state_id)

        for filename, path in processed_files.items():

            file_state = feature_state.get_file_state(filename)

            if file_state is None:
                raise ValueError(f"Cannot mark {filename} as processed because it does not exist")

            file_state.set_processed_path(
                group=group,
                format_name=format_name,
                path=Path(path),
            )

        return self.save(feature_state)

    # -------------------------
    # create
    # -------------------------

    def get_or_create(
            self,
            dataset: str,
            feature_id: str,
            root_directory: str,
    ) -> FeatureState:

        state_id = FeatureStateId(
            dataset=dataset,
            feature_id=feature_id,
        )

        doc = self.collection.find_one_and_update(
            filter={
                "_id": str(state_id),
            },
            update={
                "$setOnInsert": {
                    "_id": str(state_id),
                    "dataset": dataset,
                    "feature_id": feature_id,
                    "feature_root_directory": str(Path(root_directory) / dataset / feature_id),
                    "files": [],
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        return self._from_doc(doc)
