from datetime import datetime, timezone, timedelta

from pymongo import ReturnDocument
from pymongo.collection import Collection

from ...domain import FeatureState, FeatureStateId, FeatureStateRepository, FeatureStateNotFound


class MongoFeatureStateRepository(FeatureStateRepository):

    def __init__(self, collection: Collection):
        self.collection = collection

    # -------------------------
    # MAPPING
    # -------------------------

    def _to_doc(self, state: FeatureState) -> dict:
        return {
            "_id": str(state.id),
            "dataset": state.dataset,
            "feature_id": state.feature_id,
            "feature_root_directory": str(state.feature_root_directory),

            "downloaded_files": state.downloaded_files,
            "processed_files": state.processed_files,

            "downloading_locks": state.downloading_locks,
            "processing_locks": state.processing_locks,
        }

    def _from_doc(self, doc: dict) -> FeatureState:
        return FeatureState(
            dataset=doc["dataset"],
            feature_id=doc["feature_id"],
            feature_root_directory=doc["feature_root_directory"],

            downloaded_files=doc.get("downloaded_files", []),
            processed_files=doc.get("processed_files", []),

            downloading_locks=doc.get("downloading_locks", {}),
            processing_locks=doc.get("processing_locks", {}),
        )

    # -------------------------
    # READ
    # -------------------------

    def get(self, feature_state_id: FeatureStateId) -> FeatureState:
        doc = self.collection.find_one({"_id": str(feature_state_id)})

        if not doc:
            raise FeatureStateNotFound(str(feature_state_id))

        return self._from_doc(doc)

    def insert(self, feature_state: FeatureState) -> None:
        self.collection.insert_one(self._to_doc(feature_state))

    def get_or_create(
            self,
            dataset: str,
            feature_id: str,
            root_directory: str,
    ) -> FeatureState:
        state_id = FeatureStateId.from_parts(dataset, feature_id)

        doc = self.collection.find_one_and_update(
            filter={"_id": str(state_id)},
            update={
                "$setOnInsert": {
                    "_id": str(state_id),
                    "dataset": dataset,
                    "feature_id": feature_id,
                    "feature_root_directory": str(root_directory),

                    "downloaded_files": [],
                    "processed_files": [],

                    "downloading_locks": {},
                    "processing_locks": {},
                }
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )

        return self._from_doc(doc)

    # -------------------------
    # DOWNLOAD LOCKING
    # -------------------------

    def reserve_download(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
            timeout_seconds: int = 3600,
    ) -> bool:
        now = datetime.now(timezone.utc)

        result = self.collection.find_one_and_update(
            filter={
                "_id": str(feature_state_id),

                "downloaded_files": {"$ne": file},

                "$or": [
                    {f"downloading_locks.{file}": {"$exists": False}},
                    {
                        f"downloading_locks.{file}.expires_at": {
                            "$lt": now
                        }
                    },
                ],
            },
            update={
                "$set": {
                    f"downloading_locks.{file}": {
                        "job_id": job_id,
                        "reserved_at": now,
                        "expires_at": now + timedelta(seconds=timeout_seconds),
                    }
                }
            },
            return_document=ReturnDocument.AFTER,
        )

        return result is not None

    def complete_download(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
    ) -> bool:
        result = self.collection.update_one(
            {
                "_id": str(feature_state_id),
                f"downloading_locks.{file}.job_id": job_id,
            },
            {
                "$unset": {f"downloading_locks.{file}": ""},
                "$addToSet": {"downloaded_files": file},
            },
        )

        return result.modified_count > 0

    def release_download(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
    ) -> None:
        self.collection.update_one(
            {
                "_id": str(feature_state_id),
                f"downloading_locks.{file}.job_id": job_id,
            },
            {
                "$unset": {f"downloading_locks.{file}": ""},
            },
        )

    # -------------------------
    # PROCESSING LOCKING
    # -------------------------

    def reserve_processing(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
            timeout_seconds: int = 3600,
    ) -> bool:
        now = datetime.now(timezone.utc)

        result = self.collection.find_one_and_update(
            filter={
                "_id": str(feature_state_id),

                "processed_files": {"$ne": file},

                "$or": [
                    {f"processing_locks.{file}": {"$exists": False}},
                    {
                        f"processing_locks.{file}.expires_at": {
                            "$lt": now
                        }
                    },
                ],
            },
            update={
                "$set": {
                    f"processing_locks.{file}": {
                        "job_id": job_id,
                        "reserved_at": now,
                        "expires_at": now + timedelta(seconds=timeout_seconds),
                    }
                }
            },
            return_document=ReturnDocument.AFTER,
        )

        return result is not None

    def complete_processing(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
    ) -> bool:
        result = self.collection.update_one(
            {
                "_id": str(feature_state_id),
                f"processing_locks.{file}.job_id": job_id,
            },
            {
                "$unset": {f"processing_locks.{file}": ""},
                "$addToSet": {"processed_files": file},
            },
        )

        return result.modified_count > 0

    def release_processing(
            self,
            feature_state_id: FeatureStateId,
            file: str,
            job_id: str,
    ) -> None:
        self.collection.update_one(
            {
                "_id": str(feature_state_id),
                f"processing_locks.{file}.job_id": job_id,
            },
            {
                "$unset": {f"processing_locks.{file}": ""},
            },
        )
