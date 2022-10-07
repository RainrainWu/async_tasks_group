import asyncio
from random import random
import logging
from typing import Coroutine, Iterable

logging.basicConfig(level=logging.INFO)


class TaskErrorAlpha(BaseException):

    def __repr__(self) -> str:
        return f"TaskErrorAlpha: {super().__repr__()}"


class TaskErrorBeta(BaseException):

    def __repr__(self) -> str:
        return f"TaskErrorBeta: {super().__repr__()}"


async def my_async_task():

    delay = random()
    await asyncio.sleep(delay)

    if delay < 0.5:
        logging.info(f"delay {delay}")
    elif delay < 0.8:
        raise TaskErrorAlpha(f"error {delay}")
    else:
        raise TaskErrorBeta(f"error {delay}")


async def high_level_exec(tasks: Iterable[Coroutine]):

    results = await asyncio.gather(
        *tasks,
        return_exceptions=True,
    )

    for result in results:
        if isinstance(result, BaseException):
            logging.error(f"catch {str(result)}")


async def low_level_exec(tasks: Iterable[Coroutine]):

    finished, pending = await asyncio.wait(
        map(lambda t: asyncio.create_task(t), tasks),
        timeout=None,
        return_when=asyncio.FIRST_EXCEPTION,
    )
    map(lambda x: x.cancel(), pending)

    for result in finished:
        if not (exception := result.exception()):
            continue

        if isinstance(exception, TaskErrorAlpha):
            logging.error(f"catch alpha {exception}")
        if isinstance(exception, TaskErrorBeta):
            logging.error(f"catch beta {exception}")

async def main():

    tasks = [my_async_task() for _ in range(10)]
    await high_level_exec(tasks)
    # await low_level_exec(tasks)


asyncio.run(main())
