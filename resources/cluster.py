from aiocoap.resource import Resource, Site
from resources.light import LightResource

import logging
import aiocoap
import utils
import json

from tinydb import TinyDB

db = TinyDB("temp_db.json")


class ClusterResource(Resource):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        # TODO remove this fake data
        self.lights = [LightResource(manager, 1, 1, "192.168.0.1")]

    def find_subsequents(self, k, ip):
        # Under the assumption that the list is always ordered!

        index = -1
        for index, light in enumerate(self.lights):
            if light.ip == ip:
                return self.lights[index + 1 : index + 1 + k]

        return []

    async def render_get(self, request):
        # TODO maybe remove if from arduino the port is always the same
        lights = [
            l.to_dict()
            for l in self.find_subsequents(
                2, utils.get_ip_from_socket_address(request.remote.hostinfo)
            )
        ]
        print(self.find_subsequents(2, request.remote.hostinfo))

        return aiocoap.Message(
            payload=json.dumps(lights).encode("utf-8"), token=request.token
        )

    async def render_post(self, request):
        new_light = LightResource(
            self.manager,
            len(self.lights) + 1,
            len(self.lights) + 1,
            utils.get_ip_from_socket_address(request.remote.hostinfo),
        )
        self.lights.append(new_light)
        self.manager.update_light_resources_of_cluster(new_light)

        logging.info(
            f"The IP address {utils.get_ip_from_socket_address(request.remote.hostinfo)} just registered"
        )

        return aiocoap.Message(
            code=aiocoap.CHANGED,
            payload=self.lights[-1].to_json().encode("utf-8"),
            token=request.token,
        )


class ClusterSite(Site):
    def __init__(self, manager):
        super().__init__()
        self.cluster = ClusterResource(manager)

        for light in self.cluster.lights:
            self.add_resource([str(light.id)], light)

        self.add_resource([], self.cluster)

    def add_light_resource(self, light):
        self.add_resource([str(light.id)], light)

    def get_link_description(self):
        # Publish additional data for the Cluster resource, ct=51 is application/json
        return dict(
            **super().get_link_description(),
            title=f"The cluster of street lightings managed by this edge",
            ct="51",
        )
