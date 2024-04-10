import asyncio
import logging
import os
import random
import time

from models import InferenceSettings, InferenceEngine
from typing import Dict, List
from enum import Enum


logger = logging.Logger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)

class InferenceStrategy(Enum):
    DEFAULT = "DEFAULT"
    ROUND_ROBIN = "ROUND_ROBIN"
    #TODO: Add desired strategies here


class InferenceFactory:

    def __init__(self,
                 inference_servers: Dict[str, List[InferenceSettings]], 
                 strategy: InferenceStrategy = InferenceStrategy.DEFAULT):
        
        self.strategy = strategy
        self.settings = inference_servers
        self.inference_managers = {}
        self.round_robin_request = {}
        self.inference_server_health_state = {}
        for hf_slug, inf_list in self.settings.items():
            if hf_slug not in self.inference_managers:
                self.inference_managers[hf_slug] = []
            self.round_robin_request[hf_slug] = 0
            self.inference_server_health_state[hf_slug] = []
            for inf_setting in inf_list:
                self.inference_managers[hf_slug].append(InferenceEngine(hf_slug, inf_setting))
                self.inference_server_health_state[hf_slug].append(True)
        self.default = list(self.settings.keys())[0]

    # checking the first available healthy server of the given llm type if not then of other llm type
    # failover strategy
    def get_healthy_server(self, im_key=None):
        models = [im_key] + [model for model in self.inference_server_health_state if model != im_key]
        for model in models:
            total_servers = len(self.inference_server_health_state[model])
            for _ in range(total_servers):
                server = self.round_robin_request.get(model, 0)
                for _ in range(total_servers):
                    if self.inference_server_health_state[model][server]:
                        return server
                    server = (server + 1) % total_servers
        raise SystemExit("API failed completely and is exiting.")

    def generate(self, prompt, im_key=None):
        #TODO: Failover strategy
        #TODO: Load balancing strategy
        #TODO: Health check strategy

        # This is just a sample code to allow the code to run
        if not im_key:
            print(self.default)
            return self.inference_managers[self.default][0].generate(prompt)
        else:
            # Distribution of load using random function assuming all servers of a given llm type is healthy
            # request_id = random.randint(1, 100)
            # server = request_id % len(self.inference_managers[im_key])
            # print(server)
            # return self.inference_managers[im_key][server].generate(prompt)

            # Even Distribution of load assuming all servers being healthy and equal in capacity
            current_server = self.get_healthy_server(im_key)
            print(current_server)
            self.round_robin_request[im_key] = (current_server + 1) % len(self.inference_managers[im_key])
            return self.inference_managers[im_key][current_server].generate(prompt)


# checking the health of the system
async def check_health(obj):
    while True:
        tasks = []
        for server_type, servers in obj.inference_managers.items():
            for server, inference_manager in enumerate(servers):
                tasks.append(check_server_health(server_type, server, inference_manager))

        results = await asyncio.gather(*tasks)

        for result in results:
            server_type, server, health_state = result
            obj.inference_server_health_state[server_type][server] = health_state

        logger.info("Health checks ongoing")
        await asyncio.sleep(3)


async def check_server_health(server_type, server, inference_manager):
    health_state = await inference_manager.health_check()
    return server_type, server, health_state
