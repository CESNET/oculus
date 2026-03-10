from ...bootstrap_container import bootstrap_container


class RedisPubSub:
    def __init__(self, client=None):
        self._client = client or bootstrap_container.redis

    def publish(self, job_id: str, message: str):
        self._client.publish(f"job:{job_id}", message)

    def subscribe(self, job_id: str):
        pubsub = self._client.pubsub()
        pubsub.subscribe(f"job:{job_id}")
        return pubsub


redis_pubsub = RedisPubSub()
