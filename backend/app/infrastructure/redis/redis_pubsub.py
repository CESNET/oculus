class RedisPubSub:
    def __init__(self, client):
        self._client = client

    def publish(self, job_id: str, message: str):
        self._client.publish(f"job:{job_id}", message)

    def subscribe(self, job_id: str):
        pubsub = self._client.pubsub()
        pubsub.subscribe(f"job:{job_id}")
        return pubsub
