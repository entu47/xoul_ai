from models import InferenceSettings
from inference import InferenceFactory, check_health
import asyncio

# ----- Example of usage ----- #


inf_settings = {
    "70b": [8000, 8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009],
    "13b": [8010, 8011, 8012, 8013, 8014, 8015, 8016, 8017, 8018, 8019],
    "7b": [8020, 8021, 8022, 8023, 8024, 8025, 8026, 8027, 8028, 8029]
}

inf_factory = {}

for llm, engine_list in inf_settings.items():
    if llm not in inf_factory:
        inf_factory[llm] = []

    for port in engine_list:
        inf_factory[llm].append(InferenceSettings(inf_url=f"http://127.0.0.1:{port}/v1"))

factory = InferenceFactory(inf_factory)

health_task = asyncio.ensure_future(check_health(factory))


async def health_check():
    await check_health(factory)


async def prompt_generator():
    res = (await factory.generate(prompt="what is python", im_key="13b"))
    res = (await factory.generate(prompt="what is mobile", im_key="13b"))
    res = (await factory.generate(prompt="how does aeroplain flies", im_key="13b"))


async def main():
    await asyncio.gather(health_check(), prompt_generator())

asyncio.run(main())
