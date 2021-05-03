from aiocoap.resource import Resource

import aiocoap
import json
import datetime

class Metric():

    def __init__():
        self

class LightResource(Resource):
    """Resource that represents the street light"""

    def __init__(self, manager, id, order, ip, registered_at=None, last_seen_at=None):
        super().__init__()
        self.id = id
        self.manager = manager
        self.registered_at = registered_at
        self.last_seen_at = last_seen_at
        self.order = order
        self.ip = ip
        self.metrics = []

    async def render_get(self, request):
        return aiocoap.Message(payload=self.to_json().encode("utf-8"), token=request.token)

    async def render_put(self, request):
        self.metrics.append(json.loads(request.payload))
        self.seen()

        return aiocoap.Message(code=aiocoap.CHANGED, token=request.token)

    def seen(self):
        self.last_seen_at = datetime.datetime.utcnow().isoformat()

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {"id": self.id, "registered_at": self.registered_at, "last_seen_at": self.last_seen_at, "order": self.order, "ip": self.ip, "metrics": self.metrics}

    def get_link_description(self):
        # Publish additional data for the Light resource, ct=51 is application/json
        return dict(
            **super().get_link_description(),
            title=f"The light with ID: {self.id}, IP: {self.ip}",
            ct="51",
        )
