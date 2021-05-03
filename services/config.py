from configparser import ConfigParser

import uuid
import logging


class Config:
    def __init__(self):
        self.config = ConfigParser()
        self._read()

        if not self.config.has_section("CLUSTER"):
            self.config.add_section("CLUSTER")
            self.config.set("CLUSTER", "id", str(uuid.uuid4()))
            logging.info(f"Generated UUID for the current edge device that is {self.config.get('CLUSTER', 'id')}")

        if not self.config.has_section("DATABASE"):
            self.config.add_section("DATABASE")
            self.config.set("DATABASE", "path","local_db.json")

        if not self.config.has_section("CLOUD"):
            self.config.add_section("CLOUD")
            self.config.set("CLOUD", "ip","localhost")

        self._save()

    def _read(self):
        self.config.read("config.ini")

    def _save(self):
        with open("config.ini", "w") as conf:
            self.config.write(conf)

    def get_cluster_id(self):
        return self.config.get("CLUSTER", "id")
