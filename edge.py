import logging
import asyncio
import aiocoap

from resources.manager import Manager
from services import Config
from aiocoap.resource import Resource

from aiocoap import resource


def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logging.getLogger("coap-server").setLevel(logging.DEBUG)

    config = Config()

    # Start the server
    manager = Manager(config)
    asyncio.Task(aiocoap.Context.create_server_context(manager.root))
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
