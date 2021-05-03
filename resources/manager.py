from resources.cluster import ClusterSite
from aiocoap.resource import Site, WKCResource


class Manager:
    def __init__(self, config):
        self.root = Site()
        self._config = config

        self.root.add_resource(
            [".well-known", "core"], WKCResource(self.root.get_resources_as_linkheader)
        )

        self.cluster = ClusterSite(self)
        # root.add_resource(["ciao"], Resource())
        self.root.add_resource(["lights"], self.cluster)

    def update_light_resources_of_cluster(self, light):
        self.cluster.add_light_resource(light)
