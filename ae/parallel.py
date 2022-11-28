import asyncio
from concurrent.futures import ThreadPoolExecutor

from . import config

async def loop(executor, args_list):
    tasks = []
    loop = asyncio.get_event_loop()
    for args in args_list:
            tasks.append(
                loop.run_in_executor(executor, *args)
            )

    completed, pending = await asyncio.wait(tasks)

    results = [t.result() for t in completed]
    return [item for sublist in results for item in sublist]


def run(args_list):
    executor = ThreadPoolExecutor(
        max_workers=config.get("async.workers", 12)
    )
    event_loop = asyncio.get_event_loop()
    results = event_loop.run_until_complete(
        loop(executor, args_list)
    )
    return results
